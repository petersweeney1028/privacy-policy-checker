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
   - Share your Google Sheet with the email address of the service account (found in the credentials.json file)

## Usage
1. Prepare a Google Sheet with URLs in the first column.
2. Make sure the Google Sheet is either public or shared with the email address of your Google Cloud service account.
3. Run the script:
   ```
   python privacy_policy_checker.py
   ```
4. Enter the Google Sheet URL when prompted.
5. Optionally enter additional terms to check for, separated by commas.
6. Choose whether to write results back to the Google Sheet when prompted.

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
10 cells updated successfully in the Google Sheet.
Results have been successfully written back to the Google Sheet.

Thank you for using the Privacy Policy Checker!
```

## Writing Results Back to Google Sheet
When prompted, you can choose to write the results back to the Google Sheet. This feature will:
1. Create a new sheet named "Results" in your Google Sheet.
2. Write the URLs and their corresponding SSN status to this new sheet.
3. Overwrite any existing data in the "Results" sheet.

To use this feature:
1. Ensure your `credentials.json` file is set up correctly.
2. Make sure the service account email has edit access to the Google Sheet.
3. When prompted, enter 'y' to write results back to the sheet.

## Troubleshooting
- If you encounter issues accessing the Google Sheet, make sure it's set to public or shared with the email address associated with your Google Cloud service account.
- Ensure that the `credentials.json` file is present in the project root directory and contains valid Google Cloud credentials.
- If the script fails to scrape a website, try running it again as some websites may have temporary access issues.
- If you're unable to write results back to the Google Sheet, check that the service account has edit permissions for the sheet.
- For any other issues, check the error messages in the console output and refer to the comments in the code for additional guidance.
