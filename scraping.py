import requests
from bs4 import BeautifulSoup
import csv

def scrape_students(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    # Find each student record (each enclosed in a <section> with class "yaqOZd")
    sections = soup.find_all("section", class_="yaqOZd")
    student_data = []

    for section in sections:
        # Get all span elements with class "C9DxTc" inside this section
        spans = section.find_all("span", class_="C9DxTc")
        # Look for the span that starts with "AU/" (registration id)
        reg_index = None
        for i, span in enumerate(spans):
            text = span.get_text(strip=True)
            if text.startswith("AU/"):
                reg_index = i
                break
        # Ensure we found a registration id and that there are enough spans following it
        if reg_index is not None and len(spans) >= reg_index + 4:
            registration_id = spans[reg_index].get_text(strip=True)
            name = spans[reg_index + 1].get_text(strip=True)
            course = spans[reg_index + 2].get_text(strip=True)
            aoi = spans[reg_index + 3].get_text(strip=True)
            
            # Replace "NA" in course with "MCA"
            if course.upper() == "NA":
                course = "MCA"
            
            student_data.append({
                "registration_id": registration_id,
                "name": name,
                "course": course,
                "aoi": aoi
            })
    return student_data

if __name__ == "__main__":
    url = "https://www.aucse.in/people/student/mca-batch-2022-2024"
    students = scrape_students(url)

    if students:
        with open("students.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["registration_id", "name", "course", "aoi"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        print("Scraping complete. Data saved to students.csv")
    else:
        print("No student data found.")
