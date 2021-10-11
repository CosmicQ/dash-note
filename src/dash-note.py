#!/usr/local/bin/python3

import sys
import boto3
import os
import time
import json
from datetime import datetime

dashboard = "Test"
label = "Just a test"

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
        #  'annotations': {
        #      'vertical': [
        #          {
        #              'label': 'Untitled annotation', 
        #              'value': '2021-10-08T01:26:46.000Z'
        #          }
        #      ]
        #  }
  
  return data

# Upload Dashboard
def upload_dash( new_dash_data, dashboard ):
    dash = boto3.client('cloudwatch')
    this_dash_data = json.dumps( new_dash_data )
    print( f"DEBUG: {type(this_dash_data)} - {this_dash_data}\n" )

    response = dash.put_dashboard( DashboardName=dashboard, DashboardBody=this_dash_data )

    print( f"DEBUG: {response}\n" )
    return response

########################################
# Main
#def lambda_handler(event, context):

# Get the dashboard(s) from cloudwatch
dash_data = get_dashboard( dashboard )

# Add the vertical annotation to all graphs
new_dash_data = add_vertical( dash_data, label, date_time )

# Upload the modified dashboard
upload_dash( new_dash_data, dashboard )
