import os
import requests
from dotenv import load_dotenv
import os   

load_dotenv()
URL=os.getenv("URL_2_5")

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


# travel_resqursive_call(URL)

def get_tables():
    response = requests.get(
        f"{URL}/ex5/get-tables"
    )
    
    # print(f"get_tables response.text: {response.text}")
    return response.json()

def get_table_columns_number(table_name):
    response = requests.post(
        f"{URL}/ex5/get-columns",
        json={"table": table_name}
    )
        
    print(f"get_table_columns_number response.text: {response.text}")
    return response.json()


def get_tables_row_numbers(table_name):
    response = requests.post(
        f"{URL}/ex5/get-row-count",
        json={"table": table_name}
    )
        
    # print(f"get_tables_row_numbers response.text: {response.text}")
    return response.json()


def get_table_entry_data(table_name, row, column):
    response = requests.post(
        f"{URL}/ex5/get-entry",
        json={"table": table_name,
              "row": int(row),
              "column": column
             }
    )
        
    # print(f"get_table_data response.text: {response.text}")
    return response.json()



tables = get_tables()
print(tables)

for table in tables:
    if table == "flag":
        columns_number = get_table_columns_number(table)
        print(f"Table {table} has columns names: {columns_number} .")
        row_numbers = get_tables_row_numbers(table)
        print(f"Table {table} has rows numbers: {row_numbers} .")
        print ()

        content_together = {}
        for row_number in range(int(row_numbers["row_count"])):
            index = None
            character = None

            for column_name in columns_number:
            # print (f"ROW: {row_number} COLUMN: {column_name}")
                for column_name in columns_number:
                    if column_name == "index":
                        index = get_table_entry_data(table, row_number, column_name)["entry"]
                    if column_name == "character":
                        character = get_table_entry_data(table, row_number, column_name)["entry"]
            content_together[int(index)] = character

        
        sorted_content = dict(sorted(content_together.items()))
        content_together = ""
        for key in sorted_content:
            content_together += sorted_content[key] 
        print(content_together)

                
