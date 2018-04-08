import boto3
import os

def handler (event, context):
  print os.environ('TEST_STRING')

