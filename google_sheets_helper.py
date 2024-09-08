import gspread
from typing import List, Dict

def open_google_sheet(sheet_url: str) -> gspread.Spreadsheet:
    """
    Open a Google Sheet using its URL.
    """
    client = gspread.service_account(filename='credentials.json')
    return client.open_by_url(sheet_url)

def read_urls_from_sheet(sheet: gspread.Spreadsheet) -> List[str]:
    """
    Read URLs from Column A of the first worksheet.
    """
    worksheet = sheet.get_worksheet(0)
    return worksheet.col_values(1)[1:]  # Exclude header row

def update_sheet_with_results(sheet: gspread.Spreadsheet, results: List[Dict[str, str]]):
    """
    Update the sheet with the results for multiple phrases.
    """
    worksheet = sheet.get_worksheet(0)
    
    # Update header row
    header = ["URL", "Social Security Number", "Credit Card", "Bank Account"]
    worksheet.update('A1:D1', [header])
    
    # Update results
    for i, result in enumerate(results, start=2):  # Start from row 2 (exclude header)
        url = result['url']
        status = result['status']
        
        # Parse the status string to get individual phrase results
        phrase_results = dict(item.split(": ") for item in status.split(", "))
        
        row = [
            url,
            'Y' if phrase_results.get("Social Security Number") == "Mentioned" else 'N',
            'Y' if phrase_results.get("Credit Card") == "Mentioned" else 'N',
            'Y' if phrase_results.get("Bank Account") == "Mentioned" else 'N'
        ]
        
        worksheet.update(f'A{i}:D{i}', [row])

