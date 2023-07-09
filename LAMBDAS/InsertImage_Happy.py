import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    data = json.loads(event['Records'][0]['body'])
    body = json.loads(data['Message'])
    print(body)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_images_happy')
    
    print(body) # Revisar en CloudWatch
    response = table.put_item(Item = body)
    
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }