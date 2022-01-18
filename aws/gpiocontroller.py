import json
import datetime


def dynamo_get_table(name):



# put item as specificed json format
def dynamo_put(table, data):
    request = table.put_item(Item=data)
    print(request)

# convert text file with json contents into json variable
def text_to_json(txt_file):
    with open(txt_file, "rb") as fin:
        content = json.load(fin)
        return content


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    table = dynamo_get_table('test-ddb')  # CHANGE DATABASE TO USE REAL ONE
    data = text_to_json("testdata.txt")  # CHANGE HASH AND SORT KEY
    data["log-hash"] = str(datetime.datetime.now())  # change datetime to now

    print(data)

    dynamo_put(table, data)
