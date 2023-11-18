import json
from datetime import datetime
import tiktoken
import pandas as pd
from vision_cost_estimator import calculate_vision_cost
import argparse

enc = tiktoken.encoding_for_model("gpt-4")

# GPT-4 Turbo 128k context:
INPUT_TOKEN_PRICE_PER_THOUSAND = 0.01
OUTPUT_TOKEN_PRICE_PER_THOUSAND = 0.03
CHATGPT_PLUS_MONTHLY_COST = 20.0
MAX_CONTEXT_TOKENS = 128_000

# DALL-E 3 1024x1024:
DALLE_3_1024X1024_IMAGE_PRICE = 0.040


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


def classify_message(message):
    classifications = []
    content_type = message["content"]["content_type"]
    # map the content type to the different billing models dall-e (output), vision (input) and text (either)
    # if text, output number of tokens and whether it is input or output

    # text output check:
    if content_type in [
        "execution_output",
        "code",
        "tether_quote",
        "system_error",
        "tether_browsing_display",
    ] or (content_type == "text" and message["author"]["role"] != "user"):
        text_content = extract_text_content(message)
        classifications.append(
            {
                "type": "text",
                "input": False,
                "tokens": len(enc.encode(text_content, disallowed_special=())),
            }
        )

    # text input check:
    if content_type == "text" and message["author"]["role"] == "user":
        text_content = extract_text_content(message)
        classifications.append(
            {
                "type": "text",
                "input": True,
                "tokens": len(enc.encode(text_content, disallowed_special=())),
            }
        )

    # dall-e output check:
    if (
        message["author"]["name"] == "dalle.text2im"
        and content_type == "multimodal_text"
    ):
        # find out how many images were generated - message -> content -> parts length
        for part in message["content"]["parts"]:
            classifications.append(
                {
                    "type": "dall-e",
                    "input": False,
                    "cost": DALLE_3_1024X1024_IMAGE_PRICE,
                    "tokens": 0,  # TODO: verify this ie do dalle generated outputs get consumed as input tokens?
                }
            )

    # vision input check:
    if message["author"]["role"] == "user" and content_type == "multimodal_text":
        # need to check parts for images and prompt text
        for part in message["content"]["parts"]:
            if type(part) == dict:
                width = part["width"]
                height = part["height"]
                classifications.append(
                    {
                        "type": "vision",
                        "input": True,
                        "cost": calculate_vision_cost(width, height),
                        "tokens": 0,  # TODO: verify this ie do your vision inputs get later consumed as input tokens after this message?
                    }
                )
            else:
                classifications.append(
                    {
                        "type": "text",
                        "input": True,
                        "tokens": len(enc.encode(part, disallowed_special=())),
                    }
                )

    # return the classifications
    return classifications


def calculate_monthly_cost(conversations):
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
            message_type = classify_message(message)

            tokens = 0
            for m in message_type:
                tokens += m["tokens"]
            rolling_sum += tokens
            if rolling_sum > MAX_CONTEXT_TOKENS:
                rolling_sum = MAX_CONTEXT_TOKENS

            for m in message_type:
                if m["type"] == "text":
                    if m["input"]:
                        data.append(
                            [
                                date,
                                rolling_sum,
                                0,
                                0,
                                0,
                                0,
                                0,
                            ]
                        )
                    else:
                        data.append(
                            [
                                date,
                                0,
                                tokens,
                                0,
                                0,
                                0,
                                0,
                            ]
                        )
                elif m["type"] == "dall-e":
                    data.append(
                        [
                            date,
                            0,
                            0,
                            0,
                            1,
                            0,
                            m["cost"],
                        ]
                    )
                elif m["type"] == "vision":
                    data.append(
                        [
                            date,
                            0,
                            0,
                            1,
                            0,
                            m["cost"],
                            0,
                        ]
                    )

    df = pd.DataFrame(
        data,
        columns=[
            "Date",
            "Input Tokens",
            "Output Tokens",
            "Vision Images Sent",
            "Dall-E Images Received",
            "Vision Cost",
            "Dall-E Cost",
        ],
    )
    df_grouped = df.groupby("Date").sum().reset_index()

    # Additional cost calculations
    df_grouped["Input Cost"] = round(
        df_grouped["Input Tokens"] / 1000 * INPUT_TOKEN_PRICE_PER_THOUSAND, 2
    )
    df_grouped["Output Cost"] = round(
        df_grouped["Output Tokens"] / 1000 * OUTPUT_TOKEN_PRICE_PER_THOUSAND, 2
    )
    df_grouped["Total Cost"] = round(
        df_grouped["Input Cost"]
        + df_grouped["Output Cost"]
        + df_grouped["Vision Cost"]
        + df_grouped["Dall-E Cost"],
        2,
    )

    # Sorting and formatting
    df_grouped = df_grouped.sort_values(by="Date", ascending=False)
    df_grouped["Date"] = df_grouped["Date"].dt.strftime("%B %Y")

    return df_grouped


def display_costs(df_monthly):
    # Setting the display format for float types
    pd.options.display.float_format = "${:,.2f}".format

    # Display the monthly costs with the new columns
    print(df_monthly.to_string(index=False))

    # Calculate the aggregate totals for the new columns
    total_input_tokens = df_monthly["Input Tokens"].sum()
    total_output_tokens = df_monthly["Output Tokens"].sum()
    total_vision_images_sent = df_monthly["Vision Images Sent"].sum()  # New
    total_dalle_images_received = df_monthly["Dall-E Images Received"].sum()  # New
    total_input_cost = df_monthly["Input Cost"].sum()
    total_output_cost = df_monthly["Output Cost"].sum()
    total_vision_cost = df_monthly["Vision Cost"].sum()  # Include vision cost in totals
    total_dalle_cost = df_monthly["Dall-E Cost"].sum()  # Include DALL-E cost in totals
    total_cost = df_monthly["Total Cost"].sum()

    # Creating a dataframe for the aggregate totals including the new statistics
    df_totals = pd.DataFrame(
        [
            [
                total_input_tokens,
                total_output_tokens,
                total_vision_images_sent,  # New
                total_dalle_images_received,  # New
                total_input_cost,
                total_output_cost,
                total_vision_cost,  # New
                total_dalle_cost,  # New
                total_cost,
            ]
        ],
        columns=[
            "Input Tokens",
            "Output Tokens",
            "Vision Images Sent",
            "Dall-E Images Received",
            "Input Cost",
            "Output Cost",
            "Vision Cost",
            "Dall-E Cost",
            "Total Cost",
        ],
    )

    # Print the aggregate totals
    print("\nAggregate Costs:")
    print(df_totals.to_string(index=False))

    # Calculating and printing the total cost for ChatGPT Plus including the monthly subscription cost
    total_plus_cost = CHATGPT_PLUS_MONTHLY_COST * df_monthly.shape[0]
    print(
        f"\nTotal cost for ChatGPT Plus including subscription: ${total_plus_cost:.2f}"
    )

    # Resetting the display format after use
    pd.options.display.float_format = None


def main():
    parser = argparse.ArgumentParser(description="ChatGPT Cost Estimator")
    # Set the default value for file_path to './conversations.json'
    parser.add_argument(
        "file_path",
        type=str,
        nargs="?",
        default="./conversations.json",
        help="Path to the JSON file containing conversations data (default: ./conversations.json)",
    )

    args = parser.parse_args()
    conversations = load_json_file(args.file_path)
    df_monthly = calculate_monthly_cost(conversations)
    display_costs(df_monthly)


if __name__ == "__main__":
    main()
