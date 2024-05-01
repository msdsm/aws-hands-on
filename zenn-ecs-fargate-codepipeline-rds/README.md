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

### ALBターゲットグループの作成
## 自分用メモ
### VPCエンドポイントとは
- VPCとほかのサービス間の通信を可能にするVPCコンポーネントのこと
- VPCエンドポイントを作成することで、VPC内のインスタンスとVPC外のサービスをプライベート接続できるようになる