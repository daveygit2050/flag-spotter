import boto3
import json
from botocore.vendored import requests

def handler (event, context):

  ip = event['requestContext']['identity']['sourceIp']
  ip_api_url = "https://ipapi.co/" + ip + "/json/"
  ip_api_response = requests.get(ip_api_url).json()

  body = {
    "country": ip_api_response['country'],
    "country_name": ip_api_response['country_name']
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body)
  }

  print(response)
  return(response)
