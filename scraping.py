import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_students(url):
    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching the page:", response.status_code)
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate all student sections by the common classes
    student_sections = soup.find_all('section', class_=["yaqOZd","cJgDec","tpmmCb","C9DxTc"])
    students = []
    
    for student in student_sections:
        # Find the container with student details (using a class that is common among them)
        container = student.find("div", class_=lambda c: c and "LS81yb" in c)
        if not container:
            continue

        # Get the immediate child div tags only (ignoring nested divs deeper in the tree)
        children = [child for child in container.find_all("div", recursive=False)]
        
        # We expect at least 7 children:
        # index 0: Serial number (ignore)
        # index 1: Image container (ignore)
        # index 2: Roll number
        # index 3: Section
        # index 4: Name
        # index 5: Course
        # index 6: Area of interest
        if len(children) < 7:
            continue
        
        roll_no = children[2].get_text(strip=True)
        section = children[3].get_text(strip=True)
        name = children[4].get_text(strip=True)
        course = children[5].get_text(strip=True)
        area_of_interest = children[6].get_text(strip=True)
        
        student_info = {
            "name": name,
            "roll_no": roll_no,
            "section": section,
            "course": course,
            "area_of_interest": area_of_interest,
        }
        students.append(student_info)
    
    return students

def write_to_excel(students, filename="college_data_2023_27.xlsx"):
    # Convert the list of student dictionaries to a DataFrame
    df = pd.DataFrame(students)
    # Write the DataFrame to an Excel file without the index
    df.to_excel(filename, index=False)
    print(f"Data successfully written to {filename}")

if __name__ == '__main__':
    url = "https://www.aucse.in/people/student/btech/cse-batch-2023-2027"
    student_data = scrape_students(url)
    
    # Optionally print out the scraped student data for verification
    for student in student_data:
        print(student)
    
    # Write the scraped data to the Excel file
    write_to_excel(student_data)
