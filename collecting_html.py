import requests

URL = "https://www.aucse.in/people/student/mca-batch-2022-2024"

r = requests.get(URL)

with open("mca_22_24.html", "w") as f:
    f.write(r.text)