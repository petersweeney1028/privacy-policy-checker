import pandas as pd
from typing import List, Dict
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from urllib.parse import urlparse, parse_qs
from googleapiclient.errors import HttpError

def read_urls_from_sheet(sheet_url: str) -> List[str]:
    """
    Read URLs from Column A of the first worksheet of a public Google Sheet.
    """
    try:
        # Parse the Google Sheet URL
        parsed_url = urlparse(sheet_url)
        if parsed_url.netloc != 'docs.google.com':
            raise ValueError("Invalid Google Sheets URL")
        
        # Extract sheet ID from the URL
        path_parts = parsed_url.path.split('/')
        if len(path_parts) < 4 or path_parts[1] != 'd':
            raise ValueError("Invalid Google Sheets URL format")
        sheet_id = path_parts[3]
        
        # Convert sheet URL to CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        # Read CSV data
        response = requests.get(csv_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        df = pd.read_csv(pd.compat.StringIO(response.text))
        
        if df.empty:
            print("Warning: The Google Sheet is empty.")
            return []
        
        urls = df.iloc[:, 0].tolist()
        
        # Remove any empty strings or None values
        urls = [url for url in urls if url and isinstance(url, str)]
        
        if not urls:
            print("Warning: No valid URLs found in the Google Sheet.")
        
        return urls
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except requests.exceptions.RequestException as re:
        print(f"Error accessing the Google Sheet: {str(re)}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the Google Sheet: {str(e)}")
    
    return []

def write_results_to_sheet(sheet_id: str, results: List[Dict[str, str]]):
    """
    Write results back to the Google Sheet.
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )

        service = build('sheets', 'v4', credentials=creds)

        # Prepare the data to write
        values = [['URL', 'SSN Status']] + [[result['url'], result['ssn_status']] for result in results]

        body = {
            'values': values
        }

        # Write to the sheet
        sheet = service.spreadsheets()
        result = sheet.values().update(
            spreadsheetId=sheet_id,
            range='Sheet1!A1',  # Assuming we're writing to Sheet1, starting from A1
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"{result.get('updatedCells')} cells updated successfully in the Google Sheet.")
        return True
    except FileNotFoundError:
        print("Error: credentials.json file not found. Please make sure you have set up the Google Sheets API credentials.")
    except HttpError as error:
        print(f"An error occurred while accessing the Google Sheet: {error}")
        if error.resp.status == 403:
            print("Make sure the service account email has edit access to the Google Sheet.")
    except Exception as e:
        print(f"An unexpected error occurred while writing results to the Google Sheet: {str(e)}")
    return False

