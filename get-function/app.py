#New imported libraries
import json 
import boto3
import logging

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.event_handler.api_gateway import Response #Imported library

#Initialize clients and Powertools
dynamodb = boto3.client("dynamodb")

app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")

#Modified segment
@app.get("/get")
@tracer.capture_method
def getfunction():
    metrics.add_metric(name="GetAPI", unit=MetricUnit.Count, value=1)
    logger.info("Count endpoint hit - HTTP 200")
    
    try:
        response = dynamodb.get_item(
            TableName="cloud-resume-challenge",
            Key={
                "ID": {"S": "visitors"}
            }
        )

        item=response.get("Item")
        if not item:
            raise Exception("No item found with ID 'visitors'")
        
        #Extract the visitor count from the response
        visitors = item.get("visitors", {}).get("N", "0")

        return Response(
            status_code=200,
            content_type="application/json",
            body={"count": visitors},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )

    except Exception as e:
        logger.error(f"Error retrieving count: {str(e)}")

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
