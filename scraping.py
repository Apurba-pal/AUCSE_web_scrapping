import os
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

URL = "https://www.aucse.in/people/student/btech/cse-batch-2022-2026"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# Send GET request with error handling
try:
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Error fetching the URL: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# Create an Excel workbook
wb = Workbook()
sheet = wb.active
sheet.title = "Scraped Data"
sheet.append(["Sl No.", "Roll No.", "Name", "Specialization", "Batch", "Area of Interest", "Phone no.", "Status"])

# Extracting data from HTML
sections = soup.find_all("section", {"class": ["yaqOZd", "cJgDec", "tpmmCb"]})
for section in sections:
    paragraphs = section.find_all("p", class_="zfr3Q CDt4Ke")
    sl_no = paragraphs[0].text.strip() if len(paragraphs) > 0 else "N/A"
    roll_number = paragraphs[1].text.strip() if len(paragraphs) > 1 else "N/A"
    name = paragraphs[2].text.strip() if len(paragraphs) > 2 else "N/A"
    specialization = paragraphs[3].text.strip() if len(paragraphs) > 3 else "N/A"
    area_of_interest = paragraphs[4].text.strip() if len(paragraphs) > 4 else "N/A"
    
    # Replace "NA" with "B.Tech. CSE (Core)" in Specialization
    if specialization == "NA":
        specialization = "B.Tech. CSE (Core)"
    
    batch = "2022"  
    phone_no = "00"
    status = 1
    
    sheet.append([sl_no, roll_number, name, specialization, batch, area_of_interest, phone_no, status])

# Save the data to an Excel file
wb.save("college_data.xlsx")
print("Data successfully scraped and saved to college_data.xlsx")
