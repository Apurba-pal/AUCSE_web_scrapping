# for 23-27

import os
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
        if course == "NA":
            course = "B.Tech. CSE (Core)"
        area_of_interest = children[6].get_text(strip=True)
        
        student_info = {
            "name": name,
            "roll_no": roll_no,
            "sec": section,
            "course": course,
            "aoi": area_of_interest,
            "year": 2023,
            "status":1
        }
        students.append(student_info)
    
    return students

def write_to_excel(students, filename="college_data_2023_27.xlsx"):
    # Convert the list of student dictionaries to a DataFrame
    df = pd.DataFrame(students)
    # Write the DataFrame to an Excel file without the index
    df.to_excel(filename, index=False)
    print(f"Data successfully written to {filename}")

def update_student_info_from_csv(students, csv_files):
    # Create a mapping of Roll Number to Registration No, Mobile, and Email
    roll_to_info = {}
    for csv_file in csv_files:
        df = pd.read_excel(csv_file) if csv_file.endswith('.xlsx') else pd.read_csv(csv_file)
        for _, row in df.iterrows():
            email = row['Email'] if 'Email' in df.columns else None
            roll_to_info[row['Roll No.']] = {
                'Registration No': row['Registration ID.'],
                'Mobile': row['Mobile'],
                'Email': email
            }

    # Update the student information with the data from the CSV files
    for student in students:
        roll_no = student['roll_no']
        if roll_no in roll_to_info:
            student.update(roll_to_info[roll_no])

    return students

if __name__ == '__main__':
    url = "https://www.aucse.in/people/student/btech/cse-batch-2023-2027"
    student_data = scrape_students(url)
    
    # Optionally print out the scraped student data for verification
    for student in student_data:
        print(student)
    
    # CSV files containing additional student information
    csv_files = [
        "23_27_csv/23_sec_A.xlsx",
        "23_27_csv/23_sec_B.xlsx",
        "23_27_csv/23_sec_C.xlsx",
        "23_27_csv/23_sec_D.xlsx",
        "23_27_csv/23_sec_E.xlsx"
    ]
    
    # Update student data with information from CSV files
    updated_student_data = update_student_info_from_csv(student_data, csv_files)
    
    # Write the updated data to the Excel file
    write_to_excel(updated_student_data)
