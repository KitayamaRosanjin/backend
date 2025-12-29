# Smart Organizer Backend 🚀

AWS CDKを使用して構築した、メモアプリ用のサーバーレス・バックエンド基盤です。

## 🌟 プロジェクトの概要

このプロジェクトは、フロントエンドからのリクエストを受け取り、データを安全に保存・管理するためのAPIを提供します。 Infrastructure as Code (IaC) を実践し、AWSの各リソースをPythonコードで定義・管理しています。

## 🛠 使用技術

- **Language**: Python 3.12 / 3.14
- **Infrastructure**: AWS CDK (Cloud Development Kit)
- **Services**:
  - **Amazon API Gateway**: RESTful APIの提供
  - **AWS Lambda**: サーバーレスなロジック実行（CORS対応済み）
  - **Amazon DynamoDB**: 高速でスケーラブルなNoSQLデータベース

## 🏗 アーキテクチャ

*(ここにアーキテクチャ図の画像を配置することを推奨します)*

## 🚀 実装のこだわり

- **環境変数の活用**: Lambda内でテーブル名をハードコードせず、環境変数から取得するように設計し、保守性を高めました。
- **CORS対応**: フロントエンド（React等）からの呼び出しを想定し、カスタムヘッダーを実装済みです。
- **エラーハンドリング**: 400系、405系、500系のステータスコードを適切に返却するようにロジックを整理しました。

## 📝 セットアップ手順

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. AWS環境の初期化

```bash
cdk bootstrap
```

### 3. デプロイ

```bash
cdk deploy
```