import boto3
import time
import json
from datetime import datetime

#######################################
# Required Vars
#   dash = ""
#   note = ""
# Optional Vars (coming)
#   time = ""

# We need the current time in UTC
# 2021-10-08T01:26:46.000Z
now = datetime.utcnow()
date_time = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

########################################
# Bring on the functions

# Get Dashboard
def get_dashboard( dashboard ):
    dash = boto3.client('cloudwatch')
    response = dash.get_dashboard( DashboardName=dashboard )

    return response

# Add the vertical
def add_vertical( dashboard, label, date_time ):
  data = dashboard['DashboardBody'].replace("'", "\"")
  data = json.loads(data)
  payload = { 'label': label, 'value': date_time }
  
  for i in range(len(data['widgets'])):
    if data['widgets'][i]['type'] == "metric":
      if "title" in data['widgets'][i]['properties']:
        print( f"Adding annotation to {data['widgets'][i]['properties']['title']}" )
      else:
        print( f"Adding annotation to MISSING TITLE" )

      if "annotations" in data['widgets'][i]['properties']:
        if "vertical" in data['widgets'][i]['properties']['annotations']:
          # Add a vertical annotation
          count = len(data['widgets'][i]['properties']['annotations']['vertical'])
          data['widgets'][i]['properties']['annotations']['vertical'].append(payload)

        else:
          # Create a vertical annotation
          data['widgets'][i]['properties']['annotations']['vertical'] = []
          data['widgets'][i]['properties']['annotations']['vertical'].append(payload)

      else:
        # Create annotation and create vertical annotation
        data['widgets'][i]['properties']['annotations'] = {}
        data['widgets'][i]['properties']['annotations']['vertical'] = []
        data['widgets'][i]['properties']['annotations']['vertical'].append(payload)
  
  return data

# Upload Dashboard
def upload_dash( new_dash_data, dashboard ):
    dash = boto3.client('cloudwatch')
    this_dash_data = json.dumps( new_dash_data )
    print( f"DEBUG: {type(this_dash_data)} - {this_dash_data}\n" )
    response = dash.put_dashboard( DashboardName=dashboard, DashboardBody=this_dash_data )

    return response

def validate( event, response ):

    # Do we have a dashboard defined?
    if "dash" not in event['queryStringParameters'].keys():
        response['statusCode'] = 400
        response['body'] = "dash not defined"

        return response
    
    if "note" not in event['queryStringParameters'].keys():
        response['statusCode'] = 400
        response['body'] = "note not defined"
       
        return response

    # Future - Add more validation

    return

########################################
# Main
def lambda_handler(event, context):

    response = {
        'isBase64Encoded': 'false',
        'statusCode': 200,
        'body': 'Validated',
        'headers': {
        'content-type': "application/json"
        }
    }

    # Validate the input
    validate( event, response )

    if response['statusCode'] == 200:

        # Get the dashboard(s) from cloudwatch
        dash_data = get_dashboard( event['queryStringParameters']['dash'] )

        # Add the vertical annotation to all graphs
        new_dash_data = add_vertical( dash_data, event['queryStringParameters']['note'], date_time )

        # Upload the modified dashboard
        upload_dash( new_dash_data, event['queryStringParameters']['dash'] )

    # Send response to API Gateway
    response_json = json.dumps(response)
    return response_json