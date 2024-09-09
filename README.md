# Privacy Policy Scraper

## Project Description
This project is a Python-based tool that scrapes privacy policies from URLs provided in a public Google Sheet. It checks for mentions of specific phrases, such as "Social Security Number" and any additional user-defined terms. The results are saved to a CSV file.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the script:
   ```
   python privacy_policy_checker.py
   ```
2. When prompted, enter the public Google Sheet URL containing the list of websites to check.
3. Optionally enter additional terms to check for, separated by commas.

## Example
```
Welcome to the Privacy Policy Checker!
Please enter the public Google Sheet URL: https://docs.google.com/spreadsheets/d/your_sheet_id/edit#gid=0
Enter additional terms to check for, separated by commas (press Enter if none): personal information, data collection

Reading URLs...
Found 5 URLs to process.
Processing URLs and checking for phrase mentions...
...
Results have been written to output_results.csv

Thank you for using the Privacy Policy Checker!
```

## Input Format
- The URLs should be in the first column of the Google Sheet.
- Make sure the Google Sheet is set to public or "Anyone with the link can view".

## Output
The script generates an `output_results.csv` file with the following columns:
- `url`: The URL of the website
- `ssn_status`: 'Y' if "Social Security Number" is mentioned, 'N' if not, 'NA' if the page couldn't be accessed

## Troubleshooting
- If the script fails to scrape a website, try running it again as some websites may have temporary access issues.
- Ensure that the Google Sheet is accessible and contains valid URLs.
- For any other issues, check the error messages in the console output and refer to the comments in the code for additional guidance.
