from openai import OpenAI
from pprint import pprint

client = OpenAI()

chatlog = []

chatlog.append({
    "role": "developer", "content": "You are a helpful home assistant named Jan. Help the user in what they want."
    })


NUM_A = 234123412342134213421341234213421341234
NUM_B = 42342342342342344234234234234234
#GPT : 234123412342134255663575468447655575468
    

while True:
    user_msg = input("? ")
    chatlog.append({"role": "user", "content": user_msg})

    response =client.responses.create(
        model="gpt-5.1",
        input=chatlog
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
    else:
        print("UNKNOWN OUTPUT TYPE", output_msg) 