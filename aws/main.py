import boto3
from botocore.config import Config

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
    table.put_item(Item=data)

def s3_get_buckets():
    s3 = boto3.resource('s3')

    for bucket in s3.buckets.all():
        print(bucket.name)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    table = dynamo_get_table('test-ddb')

    #s3_get_buckets()



