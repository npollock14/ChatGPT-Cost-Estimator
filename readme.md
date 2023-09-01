# ChatGPT Cost Estimator

`ChatGPT-Cost-Estimator` is a tool designed to estimate the costs of your ChatGPT Plus conversation history as if it were executed using the OpenAI API. It uses the `conversations.json` file exported from ChatGPT and estimates OpenAI API monthly costs based on token count.

Use this tool to estimate if it may be more cost effective to use ChatGPT Plus or the OpenAI API.

**Note:** This tool assumes GPT-4 8k context api pricing for all conversations.

## Pricing constants:
* Input @ $0.03 / 1K tokens	 
* Output @ $0.06 / 1K tokens

## Example Output

```
         Date  Input Tokens  Output Tokens  Input Cost  Output Cost  Total Cost
  August 2023       1626585         169996      $48.80       $10.20      $59.00
    July 2023       1473313         182852      $44.20       $10.97      $55.17
    June 2023       1239789         166160      $37.19        $9.97      $47.16
     May 2023        788586         244757      $23.66       $14.69      $38.35
   April 2023        382448          74385      $11.47        $4.46      $15.93
   March 2023        431761         108606      $12.95        $6.52      $19.47
February 2023        676726          76011      $20.30        $4.56      $24.86
 January 2023         82320          21323       $2.47        $1.28       $3.75
December 2022        580324          43087      $17.41        $2.59      $20.00

Aggregate Costs:
 Input Tokens  Output Tokens  Input Cost  Output Cost  Total Cost
      7281852        1087177     $218.45       $65.24     $283.69

Total cost for ChatGPT Plus: $180.00
```

## Prerequisites

- Python (tested with Python 3.11)

## Installation

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/npollock14/ChatGPT-Cost-Estimator.git
    ```

2. Navigate to the cloned directory.

    ```bash
    cd ChatGPT-Cost-Estimator
    ```

3. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Obtaining the conversations.json file

1. Open [ChatGPT](https://chat.openai.com/)
2. Click on the user icon or the three dots in the bottom left corner.
3. Settings > Data Controls > Export data.
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
