#New imported libraries
import json 
import boto3 #AWS SDK for Pyhton
import logging

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.event_handler.api_gateway import Response #Imported library

#Initialize AWS SDK client
dynamodb = boto3.client("dynamodb")

#Powertools Components
app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")

#Modified segment
@app.post("/put")
@tracer.capture_method
def putfunction():
    metrics.add_metric(name="PutAPI", unit=MetricUnit.Count, value=1)
    logger.info("Count endpoint hit - HTTP 200")
    
    try:
        #Increment the visitor count in DynamoDB
        response = dynamodb.update_item(
            TableName="cloud-resume-challenge",
            Key={
                "ID": {"S": "visitors"}
            },
            UpdateExpression="ADD visitors :inc",
            ExpressionAttributeValues={
                ":inc": {"N": "1"}
            }
        )


        #Log message
        logger.info("DynamoDB update succeeded.")


        #Return method
        return Response( #Powertools' built-in response
            status_code=200,
            content_type="application/json", #JSON format
            body={"message": "Visitor count incremented successfully"},
            headers={ #CORS headers
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
   
    except Exception as e:
        logger.error(f"DynamoDB update failed: {str(e)}")


        return Response(
            status_code=500,
            content_type="application/json",
            body={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )


# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
# Adding tracer
# See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/tracer/
@tracer.capture_lambda_handler
# ensures metrics are flushed upon request completion/failure and capturing ColdStart metric
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
