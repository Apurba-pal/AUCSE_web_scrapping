import os
import re
import requests
from bs4 import BeautifulSoup

def scrape_images(url, folder="images_23_27", resume_from="UG/02/BTCSEAIML/2023/040"):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching the page:", response.status_code)
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    # Using a list of classes to filter student sections
    student_sections = soup.find_all('section', class_=["yaqOZd", "cJgDec", "tpmmCb", "C9DxTc"])
    print(f"Found {len(student_sections)} student sections.")
    
    # Regex to match roll numbers of the forms:
    # UG/02/BTCSE/2023/XXX  (standard)
    # UG/02/BTCSE<extra>/2023/XXX (with extra letters, e.g., BTCSEAIML, BTCSECSF, BTCSEDA, etc.)
    roll_pattern = re.compile(r"UG/02/BTCSE(?:([A-Z]+))?/2023/(\d+)")
    
    # Headers to bypass potential 403 errors
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': url}
    
    resume_mode = False  # This flag will be set once we encounter the resume roll number

    for student in student_sections:
        try:
            # Get the image URL from the first <img> tag in the student section
            img_tag = student.find("img")
            if not img_tag or not img_tag.get("src"):
                print("No image tag found for a student; skipping.")
                continue
            image_url = img_tag.get("src")
            
            # Find a tag (usually a <p>) that contains a roll number matching our pattern
            roll_no_tag = student.find(lambda tag: tag.name == "p" and roll_pattern.search(tag.get_text()))
            if not roll_no_tag:
                print("No roll number found for a student; skipping.")
                continue
            
            roll_no_text = roll_no_tag.get_text(strip=True)
            match = roll_pattern.search(roll_no_text)
            if not match:
                print("Roll number pattern not found in text; skipping.")
                continue
            
            # Check for our resume point.
            # Until we hit the resume_from roll number, skip all sections.
            if not resume_mode:
                if roll_no_text.strip() == resume_from:
                    print(f"Reached resume point: {roll_no_text}. Skipping this one and resuming from next.")
                    resume_mode = True
                    continue
                else:
                    print(f"Skipping roll number {roll_no_text} (before resume point).")
                    continue
            
            # Remove "/" characters for the filename
            roll_no_clean = roll_no_text.replace("/", "")
            
            # Download the image using headers
            img_response = requests.get(image_url, headers=headers)
            if img_response.status_code == 200:
                image_path = os.path.join(folder, f"{roll_no_clean}.jpg")
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded image for roll number {roll_no_text}")
            else:
                print(f"Error downloading image for roll number {roll_no_text}: {img_response.status_code}")
        except Exception as e:
            print(f"Error processing a student section: {e}")

if __name__ == '__main__':
    url = "https://www.aucse.in/people/student/btech/cse-batch-2023-2027"
    scrape_images(url, resume_from="UG/02/BTCSECSF/2023/013")
