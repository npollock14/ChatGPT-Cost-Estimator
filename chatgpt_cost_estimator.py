import json
from datetime import datetime
import tiktoken
import pandas as pd

# Constants
INPUT_TOKEN_PRICE_PER_THOUSAND = 0.03
OUTPUT_TOKEN_PRICE_PER_THOUSAND = 0.06
CHATGPT_PLUS_MONTHLY_COST = 20.0


def load_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


def extract_text_content(message):
    if message["content"]["content_type"] == "text":
        return "".join(message["content"]["parts"])
    elif message["content"]["content_type"] in [
        "execution_output",
        "code",
        "tether_quote",
        "system_error",
    ]:
        return message["content"]["text"]
    elif message["content"]["content_type"] == "tether_browsing_display":
        return message["content"]["result"]
    print(f"Unknown content type: {message['content']['content_type']}")
    return None


def calculate_monthly_cost(conversations):
    enc = tiktoken.encoding_for_model("gpt-4")
    data = []

    for convo in conversations:
        # Since GPT-4 uses previous chats as input tokens, we'll consider the rolling_sum
        rolling_sum = 0

        for _, value in convo["mapping"].items():
            message = value.get("message")
            if not message or message["author"]["role"] == "system":
                continue

            time_stamp = datetime.utcfromtimestamp(message["create_time"])
            date = datetime(time_stamp.year, time_stamp.month, 1)
            text_content = extract_text_content(message)
            if not text_content:
                continue

            tokens = len(enc.encode(text_content))

            # Add tokens to the rolling sum for input tokens
            rolling_sum += tokens

            # If rolling_sum exceeds 8,000, set it to 8,000 (the maximum allowed by GPT-4)
            if rolling_sum > 8000:
                rolling_sum = 8000

            if message["author"]["role"] == "user":
                # here use rolling_sum as input tokens
                data.append([date, rolling_sum, 0])
            else:
                # here use tokens as output tokens - not dependent on rolling_sum
                data.append([date, 0, tokens])

    df = pd.DataFrame(data, columns=["Date", "Input Tokens", "Output Tokens"])
    df_grouped = df.groupby("Date").sum().reset_index()

    df_grouped["Input Cost"] = round(
        df_grouped["Input Tokens"] / 1000 * INPUT_TOKEN_PRICE_PER_THOUSAND, 2
    )
    df_grouped["Output Cost"] = round(
        df_grouped["Output Tokens"] / 1000 * OUTPUT_TOKEN_PRICE_PER_THOUSAND, 2
    )
    df_grouped["Total Cost"] = round(
        df_grouped["Input Cost"] + df_grouped["Output Cost"], 2
    )

    # Sort the dataframe by date (in descending order)
    df_grouped = df_grouped.sort_values(by="Date", ascending=False)

    # Convert the date to the string format for display after sorting
    df_grouped["Date"] = df_grouped["Date"].dt.strftime("%B %Y")

    return df_grouped


def display_costs(df_monthly):
    # Setting the display format for float types
    pd.options.display.float_format = "${:,.2f}".format

    print(df_monthly.to_string(index=False))

    total_input_tokens = df_monthly["Input Tokens"].sum()
    total_output_tokens = df_monthly["Output Tokens"].sum()
    total_input_cost = df_monthly["Input Cost"].sum()
    total_output_cost = df_monthly["Output Cost"].sum()
    total_cost = df_monthly["Total Cost"].sum()

    df_totals = pd.DataFrame(
        [
            [
                total_input_tokens,
                total_output_tokens,
                total_input_cost,
                total_output_cost,
                total_cost,
            ]
        ],
        columns=[
            "Input Tokens",
            "Output Tokens",
            "Input Cost",
            "Output Cost",
            "Total Cost",
        ],
    )

    print("\nAggregate Costs:")
    print(df_totals.to_string(index=False))

    # Resetting the display format after use
    pd.options.display.float_format = None

    print(
        f"\nTotal cost for ChatGPT Plus: ${CHATGPT_PLUS_MONTHLY_COST * df_monthly.shape[0]:.2f}"
    )


if __name__ == "__main__":
    conversations = load_json_file("conversations.json")
    df_monthly = calculate_monthly_cost(conversations)
    display_costs(df_monthly)
