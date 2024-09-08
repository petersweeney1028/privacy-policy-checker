# Privacy Policy Scraper

## Project Description
This project is a Python-based tool that scrapes privacy policies from URLs provided in a Google Sheet. It checks for mentions of specific phrases, such as "Social Security Number" and any additional user-defined terms. The results are saved to a CSV file and can optionally be written back to the Google Sheet.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up Google Sheets API credentials:
   - Go to the Google Cloud Console (https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API for your project
   - Create credentials (Service Account Key) and download the JSON file
   - Rename the JSON file to `credentials.json` and place it in the project root directory

## Usage
1. Prepare a Google Sheet with URLs in the first column.
2. Run the script:
   ```
   python privacy_policy_checker.py
   ```
3. Enter the public Google Sheet URL when prompted.
4. Optionally enter additional terms to check for, separated by commas.
5. Choose whether to write results back to the Google Sheet.

## Example
```
Welcome to the Privacy Policy Checker!
Please enter the public Google Sheet URL: https://docs.google.com/spreadsheets/d/your_sheet_id/edit#gid=0
Enter additional terms to check for, separated by commas (press Enter if none): personal information, data collection

Reading URLs from the Google Sheet...
Found 5 URLs to process.
Processing URLs and checking for phrase mentions...
...
Results have been written to output_results.csv

Do you want to write results back to the Google Sheet? (y/n): y
Results have been written back to the Google Sheet.

Thank you for using the Privacy Policy Checker!
```

## Troubleshooting
- If you encounter issues accessing the Google Sheet, make sure it's set to public or shared with the email address associated with your Google Cloud service account.
- Ensure that the `credentials.json` file is present in the project root directory and contains valid Google Cloud credentials.
- If the script fails to scrape a website, try running it again as some websites may have temporary access issues.
- For any other issues, check the error messages in the console output and refer to the comments in the code for additional guidance.
