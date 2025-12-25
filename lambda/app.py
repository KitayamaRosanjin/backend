import json
import os
import boto3

# DynamoDB Table Name from Environment Variable
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    
    method = event['httpMethod']
    
    # レスポンスの共通ヘッダー（JSON形式、CORS対応）
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    try:
        if method == 'GET':
            # GET: データベース内の全アイテムをスキャンして取得します。
            # 結果は 'items' キーを持つJSONオブジェクトとして返却されます。
            response = table.scan()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'items': response.get('Items', [])})
            }
        
        elif method == 'POST':
            # POST: リクエストボディに含まれるデータを使用して新しいアイテムを作成します。
            # 作成成功のメッセージを返却します。
            body = json.loads(event['body'])
            table.put_item(Item=body)
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps({'message': 'Item created'})
            }
            
        elif method == 'DELETE':
            # DELETE: パスパラメータで指定されたID ('id') を持つアイテムを削除します。
            path_params = event.get('pathParameters')
            if path_params and 'id' in path_params:
                pk = path_params['id']
                # PKとSKが同一であるという前提で削除を実行
                table.delete_item(Key={'PK': pk, 'SK': pk})
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'message': 'Item deleted'})
                }
            # IDが指定されていない場合は400エラーを返します
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing path parameter: id'})
            }
        
        # サポートされていないメソッドの場合
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
