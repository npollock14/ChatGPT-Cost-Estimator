# ChatGPT Cost Estimator

`ChatGPT-Cost-Estimator` is a tool designed to estimate the costs of ChatGPT sessions as if they were executed using the OpenAI API. It uses the `conversations.json` file, which is an export of your ChatGPT sessions, and calculates the monthly costs based on token count.

Use this tool to estimate if it may be more cost effective to use ChatGPT Plus or the OpenAI API.

**Note:** This tool assumes GPT-4 api pricing for all conversations.

## Pricing constants:
* Input @ $0.03 / 1K tokens	 
* Output @ $0.06 / 1K tokens

## Example Output

```
         Date  Input Tokens  Output Tokens  Input Cost  Output Cost  Total Cost
  August 2023         60162         169996       $1.80       $10.20      $12.00
    July 2023         79789         182852       $2.39       $10.97      $13.36
    June 2023         63254         134461       $1.90        $8.07       $9.97
     May 2023         29316         129164       $0.88        $7.75       $8.63
   April 2023         38386          74385       $1.15        $4.46       $5.61
   March 2023         28042         108606       $0.84        $6.52       $7.36
February 2023         41835          76011       $1.26        $4.56       $5.82
 January 2023         12497          21323       $0.37        $1.28       $1.65
December 2022          4216          43087       $0.13        $2.59       $2.72

Aggregate Costs:
 Input Tokens  Output Tokens  Input Cost  Output Cost  Total Cost
       357497         939885      $10.72       $56.40      $67.12

Total cost for ChatGPT Plus: $180.00
```

## Prerequisites

- Python (tested with Python 3.11)

## Installation

1. Clone this repository to your local machine.

2. Navigate to the cloned directory:

3. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Obtaining the conversations.json file

1. https://chat.openai.com/
2. Click on the user icon or the three dots in the bottom left corner.
3. Settings > Data Controls > Export data
4. Download the data from the link provided in the email.
5. Rename the downloaded file to `conversations.json` and place it in the repo root.

## How to use ChatGPT Cost Estimator

1. Ensure that the conversations.json file is in the root of the repository folder.

2. Run the `chatgpt_cost_estimator.py` script.

    The script will display the monthly token counts and costs for both input and output, as well as the total estimated costs for using the ChatGPT API vs. ChatGPT Plus.

## License

This project is open source and available under the MIT License.

## Contributions

Contributions are welcome! Feel free to submit a pull request.

## Disclaimer

The costs estimated by this tool are approximations and might not reflect the actual costs you would incur using the OpenAI API. Always refer to OpenAI's official documentation for accurate pricing details.