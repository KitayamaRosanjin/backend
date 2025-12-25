from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "SmartOrganizerTable",
            table_name="smart-organizer-table-dev",
            partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Add Global Secondary Index (GSI)
        table.add_global_secondary_index(
            index_name="GSI1",
            partition_key=dynamodb.Attribute(name="GSI1PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="GSI1SK", type=dynamodb.AttributeType.STRING),
        )

        # Lambda Function (Python 3.14 で定義)
        handler = _lambda.Function(
            self, "SmartOrganizerHandler",
            runtime=_lambda.Runtime.PYTHON_3_12, # ※現在AWSが公式サポートしている最新安定版を指定（中身は3.14コードでも動作可）
            code=_lambda.Code.from_asset("lambda"),
            handler="app.lambda_handler", # app.py 内の lambda_handler 関数を呼び出す
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        # Grant Read/Write permissions to Lambda
        table.grant_read_write_data(handler)

        # API Gateway
        api = apigateway.RestApi(
            self, "SmartOrganizerApi",
            rest_api_name="Smart Organizer API",
            description="API for Smart Organizer App",
        )

        data_resource = api.root.add_resource("data")
        integration = apigateway.LambdaIntegration(handler)

        data_resource.add_method("POST", integration)
        data_resource.add_method("GET", integration)

        # /data/{id}
        data_id_resource = data_resource.add_resource("{id}")
        data_id_resource.add_method("DELETE", integration)