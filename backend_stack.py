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

        # 1. DynamoDB Table
        table = dynamodb.Table(
            self, "SmartOrganizerTable",
            table_name="smart-organizer-table-dev",
            partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        table.add_global_secondary_index(
            index_name="GSI1",
            partition_key=dynamodb.Attribute(name="GSI1PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="GSI1SK", type=dynamodb.AttributeType.STRING),
        )

        # 2. Lambda Function
        handler = _lambda.Function(
            self, "SmartOrganizerHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset("lambda"),
            handler="app.lambda_handler",
            environment={
                "TABLE_NAME": table.table_name,
            },
        )

        table.grant_read_write_data(handler)

        # 3. API Gateway (CORS設定を追加)
        api = apigateway.RestApi(
            self, "SmartOrganizerApi",
            rest_api_name="Smart Organizer API",
            description="API for Smart Organizer App",
            # --- 追加: API全体のデフォルトCORS設定 ---
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS, # すべてのサイトからのアクセスを許可
                allow_methods=["GET", "POST", "DELETE", "OPTIONS"], # 許可する操作
                allow_headers=["Content-Type", "Authorization"]    # 許可するヘッダー
            )
        )

        # 4. Resources & Methods
        data_resource = api.root.add_resource("data")
        integration = apigateway.LambdaIntegration(handler)

        # メソッドの追加
        data_resource.add_method("POST", integration)
        data_resource.add_method("GET", integration)

        # /data/{id} (DELETE用)
        data_id_resource = data_resource.add_resource("{id}")
        data_id_resource.add_method("DELETE", integration)