# 第4章

## AWS CLI
- コマンドを使用してAWSを操作するツール
- `aws`という名前のコマンド

## CloudFormation
- AWSサービスの1つ
- 作成したいAWSリソースを設定とともにテンプレートファイルに記述しておき、AWSマネジメントコンソールやAWS CLIのコマンドを使用してCloudFormationにそのテンプレートファイルを渡すと、スタックと呼ばれるAWSリソース群が作られてAWSリソース一式が作成される
- CloudFormationではすべての構成を1つのテンプレートファイルにまとめることができる
- CloudFormationを使えば、AWS CLIでひとつずつAWSのリソースを作成する必要もないしソースコードの変更やリソースの設定変更の際もテンプレートを修正してスタックを更新することでまとめて適用できる
- ただし、CloudFormationで管理している場合はマネジメントコンソールから変更することはやってはいけない

## SAM
- Serverless Application Modelの略
- `sam`というコマンド
- CloudFormationをベースにしたサーバーレスアプリケーションの開発手法
- samによる開発の流れは以下
  - `sam init`でプロジェクトディレクトリを初期化
  - lambdaを使う場合は、lambda関数のソースコードを記述
  - samテンプレート(`template.json`)を書く
  - `sam build`でビルドする
    - `--use-container`をつけるとdockerで動く
      - 初回だけdockerの立ち上げで時間かかる 
    - ビルドしたファイルは`.aws-sam`ディレクトリにある
  - `sam deploy`でデプロイする
    - `--guided`で対話モードで実行できる
      - regionなどの設定が聞かれる
- CloudFormationをベースにしているためマネジメントコンソールから変更することはやってはいけない

## Cloud9
- Webブラウザを使って開発できる統合開発環境
- 内部ではEC2のインスタンスが動いていてNode.js, AWS CLI, AWS SAM CLI, Docker, Pythonなどがもとからインストールされている
- AWSのリソースを管理できるエクスプローラを実現するAWS Toolkitが組み込まれている
- Cloud9と同じことをvscodeでもできて、AWS Toolkit for Visual Studio Codeというプラグインを使えば良い

## samプロジェクトの構成
- `sam init`でプロジェクトを作成する際にテンプレートを選択できる
- hello worldを選択した時に作られる主要なディレクトリの説明は以下
  - `events`ディレクトリ : ローカルでのテストの際に使うイベントを模したJSONデータの格納場所
  - `hello_world`ディレクトリ : Lambda関数のひな形, requirements.txtに利用するライブラリ一式を記述するとビルド時に組み込まれる
  - `tests`ディレクトリ : 単体テストのためのプログラム一式
  - `template.yaml` : SAMテンプレートファイル


## Serverless Application Repository
- AWSのサービス
- SAMのためのさまざまなテンプレートのひな形がある
- 今回はlambda-canary-python3を使用

## sam deploy後の確認方法
- CloudFormationをひらいてstackがあるか確認
- lambdaを開いてアプリケーションがあるか確認
  - アプリケーションからfunctionの論理IDをクリックすると関数の中身を確認できる

## lambda関数からsamのテンプレートファイルを取得する方法
- lambdaのコンソール画面からダウンロード->samファイルを選択するとtemplate.yamlを取得できる

## ローカル環境テスト
- 以下のようにしてLambda関数をdeployする前にローカルでテストできる
- `sam local generate-event -h`でリスト表示
  - cloudwatchを今回は使用
- `sam local generate-event cloudwatch --help`でhelp表示
  - scheduled-eventを今回は使用
- `sam local generate-event cloudwatch scheduled-event | tee events/scheduled-event.json`でテスト内容をeventsディレクトリの中にファイルとして作成
- `sam local invoke -e events/scheduled-event.json HelloWorldFunction`でテスト
  - `sam local invoke -e テストファイルパス 関数のID`
  - 論理IDはtemplate.yamlのresourcesの最上位ツリーの値