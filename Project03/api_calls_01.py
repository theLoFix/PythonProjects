import requests
from dotenv import load_dotenv
import os   

load_dotenv()
URL=os.getenv("URL_2_1")

def travel_resqursive_call(url):
    response = requests.get(
        f"{url}"
    )
    print(f"travel_resqursive_call response.text: {response.text}")
    
    body = response.json()
    if "next_url" in body:
        return travel_resqursive_call(body["next_url"])
    else:
        return body["flag"]

travel_resqursive_call(URL)
