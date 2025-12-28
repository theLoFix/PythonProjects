from wsgiref import headers
import requests
from dotenv import load_dotenv
import os   

load_dotenv()
URL=os.getenv("URL_2_3")


def travel_resqursive_call(url,headers={"X-Secret": None}):
    response = requests.get(
        f"{url}",
        headers=headers
    )
    print(f"travel_resqursive_call response.text: {response.text}")
    
    body = response.json()
    if "next_secret" in body:
        return travel_resqursive_call(URL, headers={"X-Secret" : body["next_secret"]})
    else:
        return body["flag"]


travel_resqursive_call(URL)