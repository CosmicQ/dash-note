import boto3
import time
import json
import logging
from datetime import datetime

#######################################
# Required Vars (now coming from the EventBridge event)
#   dashboardName = ""
#   note = ""
# Optional Vars (coming)
#   time = ""

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

# No need for the validate function as EventBridge will provide the structure

########################################
# Main
def lambda_handler(event, context):

    logging.info(f"Received event: {event}")

    dashboard_name = event.get('dashboardName')
    note = event.get('note')

    if not dashboard_name:
        logging.error("Error: 'dashboardName' not found in the event.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'dashboardName not provided in the event'})
        }

    if not note:
        logging.error("Error: 'note' not found in the event.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'note not provided in the event'})
        }

    try:
        # Get the dashboard(s) from cloudwatch
        dash_data = get_dashboard(dashboard_name)

        # Add the vertical annotation to all graphs
        new_dash_data = add_vertical(dash_data, note, date_time)

        # Upload the modified dashboard
        upload_dash(new_dash_data, dashboard_name)

        message = f"Updated {dashboard_name} with '{note}' at {date_time}."
        logging.info(message)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }

    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    