import pandas as pd
from typing import List, Tuple
from urllib.parse import urlparse

def read_urls_from_sheet(sheet_url: str) -> Tuple[List[str], str]:
    try:
        # Extract the sheet ID from the URL
        parsed_url = urlparse(sheet_url)
        path_parts = parsed_url.path.split('/')
        sheet_id = path_parts[3]

        # Construct the CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        # Read the CSV data
        df = pd.read_csv(csv_url)
        urls = df.iloc[:, 0].tolist()

        # Remove any empty strings or None values
        urls = [url for url in urls if url and isinstance(url, str)]

        if not urls:
            return [], "Warning: No valid URLs found in the input source."

        return urls, ""
    except Exception as e:
        return [], f"An unexpected error occurred: {str(e)}"

def write_results_to_csv(results: List[dict], output_file: str = 'output_results.csv'):
    """
    Write results to a local CSV file.
    """
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"Results have been successfully written to {output_file}")
        return True
    except Exception as e:
        print(f"An error occurred while writing results to the CSV file: {str(e)}")
        return False
