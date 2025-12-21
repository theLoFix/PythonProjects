from openai import OpenAI
from pprint import pprint
import json
import urllib.parse

import requests


def my_add_two_numbers(a, b):
    a = int(a)
    b = int(b)
    return str(a + b)

"""
curl -v "https://nominatim.openstreetmap.org/search?city=Bydgoszcz&format=json"
[{"place_id":161642361,"licence":"Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright","osm_type":"relation","osm_id":358688,"lat":"53.1219648","lon":"18.0002529","class":"boundary","type":"administrative","place_rank":12,"importance":0.665760702976138,"addresstype":"city","name":"Bydgoszcz","display_name":"Bydgoszcz, województwo kujawsko-pomorskie, Polska","boundingbox":["53.0501096","53.2093439","17.8741716","18.2025912"]}]%           



curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m" 

{"latitude":52.52,"longitude":13.419998,"generationtime_ms":0.029206275939941406,"utc_offset_seconds":0,"timezone":"GMT","timezone_abbreviation":"GMT","elevation":38.0,"current_units":{"time":"iso8601","interval":"seconds","temperature_2m":"°C"},"current":{"time":"2025-12-21T19:30","interval":900,"temperature_2m":5.6}}%


"""
def city_to_latlon(city_name):
    
    headers = {
        "User-Agent":"DemoAppForPythonAPIService",
    }


    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json",
        headers = headers
        
        )
    print(f"city_to_latlon response.text: {response.text}")

    body = response.json()
    lat = body[0]["lat"]
    lon = body[0]["lon"]
    return {
        "lat": lat,
        "lon": lon
    }

def get_weather(lat, lon):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={float(lat)}&longitude={float(lon)}&current=temperature_2m"
    )
    print(f"get_weather response.text: {response.text}")

    body = response.json()
    return {
        "current_weather": str(body["current"]["temperature_2m"]) + body["current_units"]["temperature_2m"]
    }

tools = [
    {
        "type" : "function",
        "name" : "add_two_numbers",
        "description" : "Adds two intigers as decimal strings and returns the result as a decimal string.",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "a" : {"type" : "string", "description" : "The first number to add as decimal string."},
                "b" : {"type" : "string", "description" : "The second number to add as decimal string."}
            },
            "required" : ["a", "b"]
        }
    },
    {
        "type" : "function",
        "name" : "city_to_latitute_longitute",
        "description" : "Returns the latitude and longitude of a city name.",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "city_name" : {"type" : "string", "description" : "The name of the city to get latitude and longitude for."}
            },
            "required" : ["city_name"]
        }
    },
    {
        "type" : "function",
        "name" : "get_weather",
        "description" : "Returns the current temperature for a given latitude and longitude.",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "lat" : {"type" : "string", "description" : "The latitude of the location."},
                "lon" : {"type" : "string", "description" : "The longitude of the location."}
            },
            "required" : ["lat", "lon"]
        }
    }
]

client = OpenAI()

chatlog = []

chatlog.append({
    "role": "developer", "content": "You are a helpful home assistant named Jan. Help the user in what they want."
    })


skip_users_input = False 

while True:
    if not skip_users_input:
        user_msg = input("? ")
        chatlog.append({"role": "user", "content": user_msg})
    else:
        skip_users_input = False

    response = client.responses.create(
        model = "gpt-5.1",
        input = chatlog,
        tools = tools
    )

    # pprint(response.to_dict())


    for output_msg in response.output:
        chatlog.append(output_msg)

    if output_msg.type == "message":
        for msg in output_msg.content:
            if msg.type == "output_text":
                print(f"\x1b[1;33m{msg.text}\x1b[m")
            else:
                print("UNKNOWN CONTENT TYPE", msg)
    
    elif output_msg.type == "function_call":
        print(f"\x1b[1;31m[Function Call: {output_msg.name}]\x1b[m")
        if output_msg.name == "add_two_numbers":
            arg = json.loads(output_msg.arguments)
            res = my_add_two_numbers(arg["a"], arg["b"])
            chatlog.append(
            {   
                    "type": "function_call_output",
                    "call_id": output_msg.call_id,
                    "output": json.dumps({
                        "results": res
                    })
            })
            skip_users_input = True
        elif output_msg.name == "city_to_latitute_longitute":
            arg = json.loads(output_msg.arguments)
            res = city_to_latlon(arg["city_name"])
            chatlog.append(
            {   
                    "type": "function_call_output",
                    "call_id": output_msg.call_id,
                    "output": json.dumps({
                        "results": res
                    })
            })
            skip_users_input = True
        elif output_msg.name == "get_weather":
            arg = json.loads(output_msg.arguments)
            res = get_weather(arg["lat"], arg["lon"])
            chatlog.append(
            {   
                    "type": "function_call_output",
                    "call_id": output_msg.call_id,
                    "output": json.dumps({
                        "results": res
                    })
            })
            skip_users_input = True
        else: 
            print("UNKNOWN FUNCTION NAME", output_msg)
    else:
        print("UNKNOWN OUTPUT TYPE", output_msg) 