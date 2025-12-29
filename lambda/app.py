import json
import os
import boto3

# DynamoDB Table Name from Environment Variable
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    
    # httpMethod が存在しない場合（テスト時など）の安全策
    method = event.get('httpMethod')
    
    # レスポンスの共通ヘッダー（JSON形式、CORS対応を強化）
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS', # OPTIONSを追加
        'Access-Control-Allow-Headers': 'Content-Type' # ブラウザからのヘッダーを許可
    }

    # --- 追加: ブラウザからの事前確認（OPTIONS）への応答 ---
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('OK')
        }
    # --------------------------------------------------

    try:
        if method == 'GET':
            response = table.scan()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'items': response.get('Items', [])})
            }
        
        elif method == 'POST':
            body = json.loads(event['body'])
            # データの保存（既存のロジックを維持）
            table.put_item(Item=body)
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps({'message': 'Item created'})
            }
            
        elif method == 'DELETE':
            path_params = event.get('pathParameters')
            if path_params and 'id' in path_params:
                pk = path_params['id']
                table.delete_item(Key={'PK': pk, 'SK': pk})
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Item deleted'})
                }
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing path parameter: id'})
            }
        
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }