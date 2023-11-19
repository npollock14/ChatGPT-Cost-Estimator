# ChatGPT Cost Estimator

**Note:** Updated for GPT-4 Turbo 128k + Vision + DALL·E!

`ChatGPT-Cost-Estimator` is a tool designed to estimate the costs of your ChatGPT Plus conversation history as if it were executed using the OpenAI API. It uses the `conversations.json` file exported from ChatGPT and estimates OpenAI API monthly costs based on token count.

Use this tool to estimate if it may be more cost effective to use ChatGPT Plus or the OpenAI API.

**Note:** This tool assumes GPT-4 Turbo 128k context api pricing for all conversations. See the pricing constants in use below.

## Pricing constants:

Source: [OpenAI API Pricing](https://openai.com/pricing)

- Input @ $0.01 / 1K tokens
- Output @ $0.03 / 1K tokens
- DALL·E 3 @ $0.040 / image
- Vision (computed from dimensions) - see [Vision Cost Calculator](https://github.com/npollock14/ChatGPT-Cost-Estimator/blob/main/vision_cost_estimator.py)

## Example Output

```
          Date  Input Tokens  Output Tokens  Vision Images Sent  Dall-E Images Received  Vision Cost  Dall-E Cost  Input Cost  Output Cost  Total Cost
 November 2023        141211          48604                   3                       4        $0.03        $0.16       $1.41        $1.46       $3.06
  October 2023       1494391         186593                  41                      32        $0.29        $1.28      $14.94        $5.60      $22.11
September 2023       1406768         207387                   0                       0        $0.00        $0.00      $14.07        $6.22      $20.29
   August 2023       2644863         184873                   0                       0        $0.00        $0.00      $26.45        $5.55      $32.00
     July 2023       1914384         182852                   0                       0        $0.00        $0.00      $19.14        $5.49      $24.63
     June 2023       1652295         166160                   0                       0        $0.00        $0.00      $16.52        $4.98      $21.50
      May 2023        948845         244757                   0                       0        $0.00        $0.00       $9.49        $7.34      $16.83
    April 2023        431607          74385                   0                       0        $0.00        $0.00       $4.32        $2.23       $6.55
    March 2023        431761         108606                   0                       0        $0.00        $0.00       $4.32        $3.26       $7.58
 February 2023        849088          76011                   0                       0        $0.00        $0.00       $8.49        $2.28      $10.77
  January 2023         82320          21323                   0                       0        $0.00        $0.00       $0.82        $0.64       $1.46
 December 2022        640070          43087                   0                       0        $0.00        $0.00       $6.40        $1.29       $7.69

Aggregate Costs:
 Input Tokens  Output Tokens  Vision Images Sent  Dall-E Images Received  Input Cost  Output Cost  Vision Cost  Dall-E Cost  Total Cost
     12637603        1544638                  44                      36     $126.37       $46.34        $0.32        $1.44     $174.47

Total cost for ChatGPT Plus including subscription: $240.00
```

## Prerequisites

- Python3 (tested with Python 3.11)

## Usage

### From PyPi package

1. Install the package.

   ```bash
   pip install chatgpt-cost-estimator
   ```

2. Run the `chatgpt-cost-estimator` command with the conversations.json file path as an optional argument.

   ```bash
   chatgpt-cost-estimator conversations.json
   ```

   **Note:** If no argument is provided, the script will look for a "conversations.json" file in the current directory.

### From source

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

4. Run the run_script.py script with the conversations.json file path as an optional argument.

   ```bash
   python run_script.py conversations.json
   ```

   **Note:** If no argument is provided, the script will look for a "conversations.json" file in the current directory.

## Obtaining the conversations.json file

1. Open [ChatGPT](https://chat.openai.com/)
2. Click on the user icon or the three dots in the bottom left corner.
3. Settings > Data Controls > Export data.
4. Download the data from the link provided in the email.
5. Extract `conversations.json` and place it in the repo root.

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
