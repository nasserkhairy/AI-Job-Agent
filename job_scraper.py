import requests
from bs4 import BeautifulSoup

def extract_job_text(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text(" ", strip=True)