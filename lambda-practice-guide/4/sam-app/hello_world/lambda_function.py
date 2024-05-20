import json
def lambda_handler(event, context):
    print('hello')
    print(json.dumps(event))