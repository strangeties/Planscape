import boto3
import requests
import numpy as np
import json
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

client = boto3.client('sqs', region_name='us-west-1')
QUEUE_URL = 'https://sqs.us-west-1.amazonaws.com/705618310400/forsys_output.fifo'
PLANSCAPE_URL = 'http://planscapedevload-1541713932.us-west-1.elb.amazonaws.com/planscape-backend/plan/update_scenario/'
PROCESSING_STATUS = 2
SUCCESS_STATUS = "3"
FAILED_STATUS = "4"


def lambda_handler(event, context):
    try:
        body = event['Records'][0]['body']
        parsed = json.loads(body)
        user_id = parsed['user_id']
        scenario_id = parsed['scenario_id']

        # TODO: update processing status of Scenario via HTTP call 

        # Hardcoded patchmax run to verify that the library runs in the Lambda
        r = robjects.r
        base = importr('base')
        utils = importr('utils')
        r.source('rank.R')
        r_f = robjects.r['times2']
        # Returns static outputs from project_output.csv, stand_output.csv
        raw_forsys_output = r_f(4)

        stand_output_rdf = raw_forsys_output[0]
        forsys_stand_output_df: dict[str, list] = {
            key: (np.asarray(stand_output_rdf.rx2(key)).tolist()) for key in stand_output_rdf.names}
        project_output_rdf = raw_forsys_output[1]
        forsys_project_output_df: dict[str, list] = {
            key: (np.asarray(project_output_rdf.rx2(key)).tolist()) for key in project_output_rdf.names}

        forsys_outputs = {
            'stand' : forsys_stand_output_df,
            'project' : forsys_project_output_df
        }
        json_outputs = json.dumps(forsys_outputs)

        # TODO: re-enable when PR to add generate_project_areas_from_lambda_output_prototype endpoint is submitted.
        # Endpoint expects body containing: stand, project, user_id, scenario_id 
        
        # resp = requests.post(
        #     "http://planscapedevload-1541713932.us-west-1.elb.amazonaws.com/planscape-backend/forsys/create_scenario/",
        #     json=forsys_outputs)
        # scenario_id = resp.json()

        return {
            'success': event['Records'][0]['messageId']
        }
    except Exception as e:
        response = client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=FAILED_STATUS,
            MessageGroupId=user_id
        )
        return {
            'message': str(e)
        }
