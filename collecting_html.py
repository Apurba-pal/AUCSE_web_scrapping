import requests

URL = "https://www.aucse.in/people/student/btech/cse-batch-2023-2027"

r = requests.get(URL)

with open("23_27.html", "w") as f:
    f.write(r.text)