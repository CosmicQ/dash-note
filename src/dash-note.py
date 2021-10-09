#!/usr/local/bin/python3

import sys
import boto3
import os
import time
import json
from datetime import datetime

dashboard = "test"

# We need the current time in UTC
# 2021-10-08T01:26:46.000Z
now = datetime.utcnow()
dt = now.strftime("%Y-%m-%dT%H-%M-%S.000Z")

########################################
# Bring on the functions

# Get Dashboard
def get_dashboard( dashboard ):
    dash = boto3.client('cloudwatch')
    response = dash.get_dashboard( DashboardName=dashboard )

    return response

# Add the vertical
def add_vertical( dashboard ):
  data = dashboard['DashboardBody'].replace("'", "\"")
  data = json.loads(data)
  
  for i in range(len(data['widgets'])):
    if data['widgets'][i]['type'] == "metric":
      if "title" in data['widgets'][i]['properties']:
        print( f"Adding annotation to {data['widgets'][i]['properties']['title']}" )
      else:
        print( f"Adding annotation to MISSING TITLE" )

      #  'annotations': {
      #      'vertical': [
      #          {
      #              'label': 'Untitled annotation', 
      #              'value': '2021-10-08T01:26:46.000Z'
      #          }
      #      ]
      #  }

  return

########################################
# Main
#def lambda_handler(event, context):

# Get the dashboard(s) from cloudwatch
my_dash = get_dashboard( dashboard )

# Add the vertical annotation to all graphs
add_vertical( my_dash )

# Upload the modified dashboard
