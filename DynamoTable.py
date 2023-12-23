import decimal
import logging
from mypy_boto3_dynamodb import DynamoDBServiceResource
from botocore.exceptions import ClientError

logger = logging.getLogger(f"shepbot.{__name__}")

class DynamoTable:
    def __init__(self, dyn_resource: DynamoDBServiceResource, table_name: str):
        table = dyn_resource.Table(table_name)
        table.load()
        self.table = table
    
    def increment_counter(self, name: str, channel: str, increment: int):
        try:
            response = self.table.update_item(
                Key={"name" : name, "channel" : channel},
                UpdateExpression="ADD #c :i",
                ExpressionAttributeNames={"#c" : "count"},
                ExpressionAttributeValues={":i" : decimal.Decimal(increment)},
                ReturnValues="UPDATED_NEW")
            return response["Attributes"]["count"].to_integral_value()            
        except ClientError as err:
            logger.error("Couldn't increment value %s: %s",
                         err.response["Error"]["Code"], 
                         err.response["Error"]["Message"])
        except Exception as err:
            logger.error(f"Unkown error incrementing value {err}")

    