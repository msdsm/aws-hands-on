import boto3
import json
from collections import OrderedDict

def handler(event, context):
    # 必要な定数を定義
    BUCKET_NAME = event['bucket_name'] # s3バケット名前
    BUCKET_KEY = event['bucket_key'] # ファイル名
    UPLOAD_BUCKET_KEY = 'b.json' 

    # a.jsonを読み込み
    s3 = boto3.client('s3') # s3クラスのインスタンスのようなものだと思う
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=BUCKET_KEY) # a.json取得
    data = json.loads(obj['Body'].read().decode('utf-8')) # 中身取得
    print(f'{BUCKET_KEY}の内容 : {data}') # 確認のため出力

    # b.jsonのアップロード
    s3 = boto3.resource('s3')
    obj = s3.Bucket(BUCKET_NAME).Object(UPLOAD_BUCKET_KEY) # b.json作成
    data = OrderedDict(file_name=UPLOAD_BUCKET_KEY, author=data['author'], age=(data['age'] + 1)) # b.jsonのファイルの中身作成
 
    res = obj.put(Body=json.dumps(data)) # 中身代入
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'[SUCCESS] upload {UPLOAD_BUCKET_KEY}')