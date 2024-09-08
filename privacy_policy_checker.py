import re
import time
import csv
from typing import List, Dict
import trafilatura

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text
    except Exception as e:
        print(f"Error fetching content from {url}: {str(e)}")
        return ""

def check_for_ssn_mention(text: str) -> bool:
    """
    Check if the phrase "Social Security Number" is mentioned in the text.
    """
    pattern = r'\bSocial Security Number\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def process_urls(urls: List[str]) -> List[Dict[str, str]]:
    """
    Process the list of URLs and check for SSN mentions.
    """
    results = []
    for url in urls:
        try:
            print(f"Processing: {url}")
            content = get_website_text_content(url)
            has_ssn_mention = check_for_ssn_mention(content)
            status = "SSN Mentioned" if has_ssn_mention else "SSN Not Mentioned"
            results.append({"url": url, "status": status})
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            results.append({"url": url, "status": "Error"})
        time.sleep(1)  # Add a delay to avoid overwhelming the servers
    return results

def read_urls_from_csv(file_path: str) -> List[str]:
    """
    Read URLs from a CSV file.
    """
    urls = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                urls.append(row[0])  # Assume URLs are in the first column
    return urls

def write_results_to_csv(results: List[Dict[str, str]], file_path: str):
    """
    Write results to a CSV file.
    """
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['url', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def main():
    input_file = 'input_urls.csv'
    output_file = 'output_results.csv'

    try:
        # Read URLs from CSV file
        urls = read_urls_from_csv(input_file)
        
        if not urls:
            print(f"No URLs found in the input file: {input_file}")
            return

        # Process URLs
        results = process_urls(urls)

        # Write results to CSV file
        write_results_to_csv(results, output_file)

        print(f"\nResults have been written to: {output_file}")

        # Print results
        print("\nResults:")
        for result in results:
            print(f"{result['url']}: {result['status']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
