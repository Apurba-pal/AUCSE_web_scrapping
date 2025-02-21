import os
import requests
from bs4 import BeautifulSoup
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

# Create a folder for images
image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

# Extracting image URLs from HTML
sections = soup.find_all("section", {"class": ["yaqOZd", "cJgDec", "tpmmCb"]})
for section in sections:
    roll_number = section.find("p", class_="zfr3Q CDt4Ke").text.strip() if section.find("p", class_="zfr3Q CDt4Ke") else "N/A"
    image_url = section.find("img")["src"] if section.find("img") else None

    # Download and save the image
    if image_url:
        try:
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                image_path = os.path.join(image_folder, f"{roll_number}.jpg")
                with open(image_path, "wb") as img_file:
                    for chunk in image_response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Downloaded image for {roll_number}")
            else:
                print(f"Failed to download image for {roll_number}: {image_response.status_code}")
        except Exception as e:
            print(f"Error downloading image for {roll_number}: {e}")