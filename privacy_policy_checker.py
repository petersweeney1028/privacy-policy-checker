import re
import time
from typing import List, Dict
import trafilatura
from requests.exceptions import RequestException
from google_sheets_helper import read_urls_from_sheet, write_results_to_csv
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

def main():
    print("Welcome to the Privacy Policy Checker!")
    sheet_url = input("Please enter the public Google Sheet URL: ")

    urls, error_message = read_urls_from_sheet(sheet_url)
    if error_message:
        print(error_message)
        return

    additional_terms = input("Enter additional terms to check for, separated by commas (press Enter if none): ").split(',')
    additional_terms = [term.strip() for term in additional_terms if term.strip()]
    phrases_to_check = ["Social Security Number"] + additional_terms

    print("\nReading URLs...")
    
    if not urls:
        print("Error: No valid URLs found. Please check the input source and try again.")
        return

    print(f"\nFound {len(urls)} URLs to process.")
    print("\nProcessing URLs and checking for phrase mentions...")
    results = process_urls(urls, phrases_to_check)

    print("\nWriting results to CSV file...")
    output_file = "output_results.csv"
    write_results_to_csv(results, output_file)

    print(f"\nResults have been written to {output_file}")
    print("\nThank you for using the Privacy Policy Checker!")

if __name__ == "__main__":
    main()
