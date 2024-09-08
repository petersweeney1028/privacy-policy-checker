import re
import time
from typing import List, Dict
import trafilatura
from requests.exceptions import RequestException
import requests
from google_sheets_helper import open_google_sheet, read_urls_from_sheet, update_sheet_with_results

def get_website_text_content(url: str, max_retries: int = 3) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    It includes retry logic for robustness.
    """
    for attempt in range(max_retries):
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                return text if text else ""
            else:
                print(f"No content downloaded from {url}")
                return ""
        except RequestException as e:
            print(f"Request error fetching content from {url} (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                return ""
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"Error fetching content from {url}: {str(e)}")
            return ""

def check_for_phrases(text: str, phrases: List[str]) -> Dict[str, bool]:
    """
    Check if any of the given phrases are mentioned in the text.
    """
    results = {}
    for phrase in phrases:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        results[phrase] = bool(re.search(pattern, text, re.IGNORECASE))
    return results

def process_urls(urls: List[str], phrases: List[str]) -> List[Dict[str, str]]:
    """
    Process the list of URLs and check for phrase mentions.
    """
    results = []
    for url in urls:
        try:
            print(f"Processing: {url}")
            content = get_website_text_content(url)
            if content:
                phrase_results = check_for_phrases(content, phrases)
                status = ", ".join([f"{phrase}: {'Mentioned' if mentioned else 'Not Mentioned'}" for phrase, mentioned in phrase_results.items()])
            else:
                status = "Error: Unable to fetch content"
            results.append({"url": url, "status": status})
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            results.append({"url": url, "status": f"Error: {str(e)}"})
        time.sleep(1)  # Add a delay to avoid overwhelming the servers
    return results

def main():
    sheet_url = input("Please enter the Google Sheet URL: ")
    phrases_to_check = ["Social Security Number", "Credit Card", "Bank Account"]

    try:
        # Open Google Sheet
        sheet = open_google_sheet(sheet_url)

        # Read URLs from Google Sheet
        urls = read_urls_from_sheet(sheet)
        
        if not urls:
            print("No URLs found in the Google Sheet.")
            return

        # Process URLs
        results = process_urls(urls, phrases_to_check)

        # Update Google Sheet with results
        update_sheet_with_results(sheet, results)

        print("\nResults have been written to the Google Sheet.")

        # Print results
        print("\nResults:")
        for result in results:
            print(f"{result['url']}: {result['status']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
