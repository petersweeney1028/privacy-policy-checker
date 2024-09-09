import re
import time
import csv
from typing import List, Dict
import trafilatura
from requests.exceptions import RequestException
import requests
from google_sheets_helper import read_urls_from_sheet, write_results_to_sheet
from tqdm import tqdm

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
                print(f"Warning: No content downloaded from {url}")
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
    privacy_paths = ['/privacy', '/privacy-policy', '/privacy-notice']
    
    for url in tqdm(urls, desc="Processing URLs", unit="URL"):
        try:
            content = ""
            privacy_url = ""
            for path in privacy_paths:
                privacy_url = url.rstrip('/') + path
                content = get_website_text_content(privacy_url)
                if content:
                    break
            
            if content:
                phrase_results = check_for_phrases(content, phrases)
                results.append({"url": url, "ssn_status": "Y" if phrase_results.get("Social Security Number", False) else "N"})
            else:
                results.append({"url": url, "ssn_status": "NA"})
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            results.append({"url": url, "ssn_status": "NA"})
        time.sleep(1)  # Add a delay to avoid overwhelming the servers
    return results

def output_results_to_csv(results: List[Dict[str, str]]):
    with open('output_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['url', 'ssn_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print("Results have been written to output_results.csv")

def main():
    print("Welcome to the Privacy Policy Checker!")
    sheet_url = input("Please enter the public Google Sheet URL: ")
    additional_terms = input("Enter additional terms to check for, separated by commas (press Enter if none): ").split(',')
    additional_terms = [term.strip() for term in additional_terms if term.strip()]
    phrases_to_check = ["Social Security Number"] + additional_terms

    print("\nReading URLs from the Google Sheet...")
    urls = read_urls_from_sheet(sheet_url)
    
    if not urls:
        print("Error: No valid URLs found in the Google Sheet. Please check the sheet and try again.")
        return

    print(f"\nFound {len(urls)} URLs to process.")
    print("\nProcessing URLs and checking for phrase mentions...")
    results = process_urls(urls, phrases_to_check)

    print("\nWriting results to CSV file...")
    output_results_to_csv(results)

    write_back = input("\nDo you want to write results back to the Google Sheet? (y/n): ").lower().strip()
    if write_back == 'y':
        try:
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
            success = write_results_to_sheet(sheet_id, results)
            if success:
                print("Results have been successfully written back to the Google Sheet.")
            else:
                print("Failed to write results back to the Google Sheet. Please check the error messages above.")
        except IndexError:
            print("Error: Invalid Google Sheet URL. Unable to extract sheet ID.")
        except Exception as e:
            print(f"An unexpected error occurred while writing results to the Google Sheet: {str(e)}")

    print("\nThank you for using the Privacy Policy Checker!")

if __name__ == "__main__":
    main()
