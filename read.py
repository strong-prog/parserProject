import json
 
with open("prod_data_base.json", "r") as rf:
    decoded_data = json.load(rf)
 
print(decoded_data)