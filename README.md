# アマゾン・フォレスト・クエスト：秘宝と七つのAWS守護者

Pygameで実装されたAWSサービスをテーマにしたRPGミニゲームです。

## ゲーム概要

アマゾンの森の奥深くに隠された伝説の秘宝「無限の拡張性」を求めて冒険に出かけましょう。
秘宝は七人のAWS守護者によって守られており、それぞれの試練をクリアする必要があります。

## 特徴

- AWSサービスを擬人化したユニークな守護者たち
- グラフィカルなRPG風インターフェース
- AWSの知識を活かした戦闘システム
- 探索、アイテム収集、成長要素を含むゲームプレイ

## 必要条件

- Python 3.x
- Pygame

## インストール方法

1. リポジトリをクローンまたはダウンロードします
2. 必要なパッケージをインストールします：
   ```
   pip install pygame
   ```
3. ゲームを起動します：
   ```
   python main.py
   ```

## 操作方法

- マウス：ボタンクリックでメニュー選択
- キーボード：テキスト入力、スペースキーでテキストスキップ

## ゲームの流れ

1. タイトル画面でゲームを開始
2. 冒険者の名前を入力
3. プロローグを読む
4. マップ画面で探索するエリアを選択
5. ランダムイベントや守護者との戦闘に挑む
6. 全ての守護者を倒して秘宝を手に入れる

## AWS守護者

- S3守護者：データを安全に保管する巨大なバケツを持つ守護者
- EC2守護者：様々な姿に変身できる計算の守護者
- Lambda守護者：瞬時に現れては消える謎の守護者
- DynamoDB守護者：無限のテーブルを操る砂漠の守護者
- CloudFront守護者：世界中に分身を持つ配信の守護者
- IAM守護者：鍵と権限を司る厳格な守護者
- SQS守護者：メッセージを操る川の守護者

## ディレクトリ構造

```
amazon-q-cli-shirt/
├── main.py                  # メインゲームファイル
├── src/                     # ソースコード
│   ├── assets/              # ゲームアセット
│   │   ├── images/          # 画像ファイル
│   │   ├── sounds/          # 音声ファイル
│   │   └── fonts/           # フォントファイル
│   ├── scenes/              # ゲームシーン
│   │   ├── scene_manager.py # シーン管理
│   │   ├── title_scene.py   # タイトル画面
│   │   └── ...              # その他のシーン
│   ├── entities/            # ゲームエンティティ
│   ├── ui/                  # UIコンポーネント
│   └── utils/               # ユーティリティ
│       └── constants.py     # 定数定義
└── README.md                # このファイル
```

## 注意事項

- このゲームはAWSサービスの学習を目的としています
- 実際のAWSサービスの機能とは異なる場合があります
- ゲーム内の描写はユーモアを含んでいます

## クレジット

- 開発：Amazon Q CLI チーム
- フレームワーク：Pygame
- グラフィック：チームメンバー作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
