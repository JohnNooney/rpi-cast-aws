import boto3
import json
import datetime


def dynamo_get_table(name):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table(name)

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    print(table.creation_date_time)
    return table


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



