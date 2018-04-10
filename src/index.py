import boto3
import json
import os
import decimal
from botocore.vendored import requests

ddb = boto3.resource('dynamodb')

def handler (event, context):

  ip = event['requestContext']['identity']['sourceIp']
  ip_api_url = "https://ipapi.co/" + ip + "/json/"
  ip_api_response = requests.get(ip_api_url).json()

  country = ip_api_response['country']
  country_name = ip_api_response['country_name']

  ddb_table = ddb.Table(os.environ['TABLE_NAME'])

  ddb_response = ddb_table.get_item(
    Key={'country': country}
  )
  
  try:
    hits = int(ddb_response['Item']['hits']) + 1
  except KeyError:
    hits = 1
  
  try: 
    ddb_table.update_item(
      Key={
        'country': country
      },
      UpdateExpression='set hits = hits + :val',
      ExpressionAttributeValues={
        ':val': 1
      },
      ReturnValues="UPDATED_NEW"
    )
  except:
    ddb_table.put_item(
      Item={
        'country': country,
        'country_name': country_name,
        'hits': hits
      }
    )

  body = {
    "country": country,
    "country_name": country_name,
    "hits": hits
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }
 
  print(country + ' has been seen ' + str(hits) + ' times')
    
  return(response)
