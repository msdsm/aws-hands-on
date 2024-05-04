# 第2章

## Pythonでの書き方
```python
def 関数名(event, context)
```
### event引数
- JSONデータ
- 今回の場合は以下
```json
{
    "x" : 10,
    "y" : 2
}
```

### context引数
- Lambda関数が配置されているパス名やメモリ容量など実行環境の情報

## ランタイム設定
- pythonでは"ファイル名.関数名"で設定

## 実行方法
- ソースコードを編集して保存->deploy
- jsonでテストをかいてテスト押す

## 実行結果確認方法
- Cloud Watchのlogで確認できる