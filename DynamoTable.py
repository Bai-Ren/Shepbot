import decimal
from mypy_boto3_dynamodb import DynamoDBServiceResource

class DynamoTable:
    def __init__(self, dyn_resource: DynamoDBServiceResource, table_name: str):
        table = dyn_resource.Table(table_name)
        table.load()
        self.table = table
    
    def increment_counter(self, id: str, increment: int):
        return self.table.update_item(
            Key={"Id" : id},
            UpdateExpression="set val = val + :i",
            ExpressionAttributeValues={":i" : decimal.Decimal(increment)},
            ReturnValues="UPDATED_NEW"
        )
    