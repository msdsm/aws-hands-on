# AWS ECS + Fargate + CodePipeline + RDSでバックエンドサービス基盤を作る

## ソース
- https://zenn.dev/taiki_asakawa/books/dfc00287d5b8c7

## 内容
- VPCの作成
- セキュリティグループの作成
- VPCエンドポイントの作成

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
- もっと詳細に調べる
### taskdef.json
- 意味不明
### buildspec.yml
- 意味不明
### appspec.yaml
- 意味不明