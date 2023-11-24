import decimal
from mypy_boto3_dynamodb import DynamoDBServiceResource

class DynamoTable:
    def __init__(self, dyn_resource: DynamoDBServiceResource, table_name: str):
        table = dyn_resource.Table(table_name)
        table.load()
        self.table = table
    
    def increment_counter(self, name: str, channel: str, increment: int):
        return self.table.update_item(
            Key={"name" : name, "channel" : channel},
            UpdateExpression="ADD #c :i",
            ExpressionAttributeNames={"#c" : "count"},
            ExpressionAttributeValues={":i" : decimal.Decimal(1)},
            ReturnValues="UPDATED_NEW"
        )
    