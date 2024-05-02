# AWS ECS + Fargate + CodePipeline + RDSでバックエンドサービス基盤を作る

## ソース
- https://zenn.dev/taiki_asakawa/books/dfc00287d5b8c7

## 内容
- VPCの作成
- セキュリティグループの作成
- VPCエンドポイントの作成
- Route53 ACM
- ALB・ターゲットグループの作成
- ECRの作成 & Docker push
- ECSクラスター作成・タスク定義
- ECSサービスの作成・実行
- RDSの作成
- CodePipelineとは
- CodePipeline事前準備
- CodeBuildプロジェクトの作成
- CodeDeployアプリケーションの作成
- CodePipelineの設定

## VPCの作成
- VPCなどの作成を選択して以下作成
  - VPC
  - サブネット(AZ2つそれぞれにpublic, privateで合計4つ)
  - IGWをVPCにアタッチ
  - ルートテーブル作成
  - publicサブネットにあたるものにルートテーブル関連付け
  - NAT gateway作成
  - S3エンドポイント作成

### セキュリティグループの作成
- 以下4つ
  - default : すべて許可
  - https : httpsリクエスト->ALB
  - alb : ALB->ECSのサービス
  - rds : ECSのサービス->RDS

### VPCエンドポイントの作成
- 以下4つ
  - s3 : VPC作成時に作成されている
  - ecr-dkr : ~ecr.dkrを選択
  - ecr-api : ~ecr.apiを選択
  - logs : ~.logsを選択

### Route53 ACM
- Route53でドメイン紐づけ
- 飛ばした

### ALB・ターゲットグループの作成
- IPアドレスを選択したターゲットグループを作成
- ALB作成
- httpsを選択するとACMの証明書が必要になるので、httpにした
- それに伴い上述のセキュリティグループでポート443から80に変更
### ECRの作成 & Docker push
- ローカルでapi作成
- ECRでリポジトリ作成
- プッシュコマンドコピペ
  - docker loginする際は、--profile "IAMユーザー名"で認証する
### ECRクラスター作成・タスク定義
- クラスターおよびタスク定義を作成
- タスク定義を作成する際に、ECRのリポジトリのURIコピペ
### ECSサービスの作成・実行
- クラスターからサービスの作成をクリックして作成
  - VPC選択
  - サブネットはprivate2つ選択
- load balancerのDNS名:80でapiあくせすできた
- セキュリティグループのつながりや、ポートマッピングがうまくいっていることがわかった

### RDSの作成
- とばした
### CodePipelineとは
- CI/CDを実現できるAWSサービス
  - CI : Continuous Integration(継続的インテグレーション)
    - Code -> build -> Test -> Codeのサイクルを回して開発のスピードと品質を担保するというもの
  - CD : Continuous Delivery(継続的デリバリー)
    - CIによって検知した変更内容を本番環境などに自動で反映して利用可能にするというもの
- AWSのサービスでCode Build, Code Deploy, Code commitなどcodeから始まるサービスをまとめてcode兄弟と呼ばれる

### CodePipeline 事前準備
- blue/green deployにはターゲットグループが2つ必要であるため以下やる
  - ターゲットグループもう一つ作成
  - ALBのリスナールールを編集してターゲットグループ追加
- CodePipelineによる実行ではタスク定義をjsonファイルで作成する必要があるため以下やる
  - コンソールからタスク定義ひらく
  - jsonファイルひらく
  - コピーしてローカルファイルにペースト
- ローカルで以下3つのファイル必要
  - taskdef.json
  - buildspec.yml
  - appspec.yaml
### CodeBuild プロジェクトの作成
- githubアカウント登録してbuildspec.ymlのパスを与える
### CodeDeploy アプリケーションの作成
- ECSのクラスターからサービスの作成をクリック
- デプロイメントタイプからblue/greenデプロイメント(AWS CodeDeployを使用)をクリック
- IAMロールでCodedeploy for ecsのロールを作成しておく必要がある
- 以降は普通のサービス作成と同じくポチポチする
- 作成後にCodeDeployコンソールのアプリケーションに作成されていることを確認
### CodePipelineの設定
- codepipelineの作成
  - githubに接続してリポジトリとブランチを選択
  - code buildで作成したもの選択
  - code deployで作成したもの選択
### 動作確認
- 実際にapiのソース変更してpush
- awsコンソールでcode pipelineみてみる
  - code buildで失敗している
  - docker loginする際に、--profile msd_userで認証しようとしているが、credentialsに登録されていないからできていないと思われる
  - これはどこで実行されているのか？
  - github上で実行されていそうなので、github上でsecret keyとか登録すればいける？
## 自分用メモ
### VPCエンドポイントとは
- VPCとほかのサービス間の通信を可能にするVPCコンポーネントのこと
- VPCエンドポイントを作成することで、VPC内のインスタンスとVPC外のサービスをプライベート接続できるようになる
### code兄弟について
- Codeから始まるAWSのサービスのこと
### CodeCommit
- AWSのGitホスティングサービス
- Githubのようなもの
### CodeBuild
- 自動テストやビルドを実行してくれるサービス
- DockerImageから環境を立ち上げて、S3やCodeCommit, Githubからソースコードを取得した後にビルドやテストを実行してくれる
- githubをソースとして指定した場合はpushを検知できる
### CodeDeploy
- S3, GithubなどにあるソースコードをEC2やLambda,オンプレミス環境などにデプロイすることができる
- ECSでBlue/Greenデプロイを実行するときにもCodeDeployを使う
### CodePipeline
- CI/CDを管理するサービス
- CodeBuildの処理が終わればCodeDeployに処理を渡すなどをしてくれる
### taskdef.json
- CodeDeployでECSのデプロイを行う際に必要になる
- タスク定義を記述したJSONファイル
### buildspec.yml
- Code Buildの実行計画を記述するファイル
- Code Buildでファイルパスを入力するタイミングがあるため、ファイル名は必ずしもこれでなくてもよい
- 以下記述例
```yaml
version: 0.2

# 各種コマンドを実行するユーザーを指定する。指定がない場合はrootユーザーが使われる。
run-as: Linux-user-name

# ビルド環境の設定。シェルや環境変数の設定を行う。指定しなくても良い
# 環境変数はkey, valueで直接指定もできるが、Systems Managerのパラメーターストアの値を用いることもできる
env: 

# プロキシサーバーにてCodeBuildを実行する際に指定する。指定しない場合はCodeBuildのデフォルトのまま実行される
proxy:

# バッチビルドの設定を行う。指定しない場合はバッチビルドが実行されない。
batch:

# 各種ビルドフェーズに関する設定
# 各フェーズにてrun-as（実行するユーザー）, on-failure（失敗したら次のフェーズにいくかどうか）, commands（実行コマンド）, finally（必ず_failureでも_実行するコマンド）等を設定
phases:
  # パッケージのインストールのコマンドを設定。
  install:
  # ビルド前に実行するコマンドを設定。
  pre_build:
  # ビルド時に実行するコマンドを設定
  build:
  # ビルド後の実行するコマンドを設定
  post_build:

# CodeBuildのレポート機能の設定。指定がない場合は、レポートが出力されない（ログとは異なるので注意）
reports:

# CodeBuildの出力をするための設定。出力先や出力ファイル等を指定する
artifacts:

# キャッシュの利用に関する設定。指定がない場合は特にキャッシュの利用がされない
# CodeBuildがS3キャッシュバケットへアップロードするための設定をする。
cache:
```
### appspec.yaml
- CodeDeployで使うデプロイ設定ファイル
- サービスとかポートとか指定できる