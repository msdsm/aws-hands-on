# クラインAWSハンズオンLambda

## ソース
- https://www.youtube.com/watch?v=BDviXnpOCms&list=PLS0SWeRoWAzEo2RffpYiRSSdHmQnTQl95&index=2

## ワークフロー
- a.json作成
- main.py作成
- awsコンソールでs3バケット作成
- a.jsonアップロード
- lambdaにmain.pyアップロード(zip)
- main.handlerをセット
- テストでeventを以下のように定義
```
{
  "bucket_name": "lambda-test-kleintube",
  "bucket_key": "a.json"
}
```
- lambdaのロールにs3のアクセス権限与える
- テスト実行
- cloudwatchでコンソール出力確認
- s3のbucketに実際にb.jsonがあることを確認
- ダウンロードして内容が変更されていることを確認
