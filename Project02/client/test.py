import requests
from pprint import pprint

MY_MATH_API = "http://127.0.0.1:8000"

def my_sum_api (lst):
    headers_content = {
        "api-key":"TAJNEHASLO",
    }

    r = requests.post(
        f"{MY_MATH_API}/sum",
        headers=headers_content,     
        json=lst,
    )
    body = r.json()
    pprint (body)
    return body["result"]

print(my_sum_api([1, 2, 3.5]))  # Should print 15
