import requests
from dotenv import load_dotenv
import os   

load_dotenv()
URL=os.getenv("URL_2_2")

def travel_resqursive_call(url,data=None):
    response = requests.post(
        f"{url}",
        data=data
    )
    print(f"travel_resqursive_call response.text: {response.text}")
    
    body = response.json()
    if "next_secret" in body:
        return travel_resqursive_call(URL, data=body["next_secret"])
    else:
        return body["flag"]

travel_resqursive_call(URL)