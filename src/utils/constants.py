#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constants for the game
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game settings
FPS = 60
GAME_TITLE = "アマゾン・フォレスト・クエスト：秘宝と七つのAWS守護者"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)

# Player stats
INITIAL_MOTIVATION = 100
INITIAL_AWS_KNOWLEDGE = 0
INITIAL_CONCENTRATION = 100

# Asset paths
ASSETS_DIR = "src/assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# Game areas
AREAS = [
    "S3湿地帯",
    "EC2迷いの森",
    "Lambda峡谷",
    "DynamoDB砂漠",
    "CloudFront山脈",
    "IAM神殿",
    "SQS川"
]

# AWS Guardians
AWS_GUARDIANS = [
    {
        "name": "S3守護者",
        "service": "Amazon S3",
        "description": "データを安全に保管する巨大なバケツを持つ守護者",
        "hp": 100,
        "attack_patterns": ["データ洪水", "バケット投げ", "アクセス拒否"],
        "weakness": "データ整理",
        "area": "S3湿地帯"
    },
    {
        "name": "EC2守護者",
        "service": "Amazon EC2",
        "description": "様々な姿に変身できる計算の守護者",
        "hp": 120,
        "attack_patterns": ["インスタンス増殖", "リソース枯渇", "再起動攻撃"],
        "weakness": "オートスケーリング",
        "area": "EC2迷いの森"
    },
    {
        "name": "Lambda守護者",
        "service": "AWS Lambda",
        "description": "瞬時に現れては消える謎の守護者",
        "hp": 80,
        "attack_patterns": ["コールドスタート", "タイムアウト", "メモリ不足"],
        "weakness": "関数最適化",
        "area": "Lambda峡谷"
    },
    {
        "name": "DynamoDB守護者",
        "service": "Amazon DynamoDB",
        "description": "無限のテーブルを操る砂漠の守護者",
        "hp": 110,
        "attack_patterns": ["キー攻撃", "スロットリング", "容量不足"],
        "weakness": "インデックス設計",
        "area": "DynamoDB砂漠"
    },
    {
        "name": "CloudFront守護者",
        "service": "Amazon CloudFront",
        "description": "世界中に分身を持つ配信の守護者",
        "hp": 90,
        "attack_patterns": ["キャッシュ混乱", "エッジロケーション攻撃", "無効化"],
        "weakness": "キャッシュ戦略",
        "area": "CloudFront山脈"
    },
    {
        "name": "IAM守護者",
        "service": "AWS IAM",
        "description": "鍵と権限を司る厳格な守護者",
        "hp": 100,
        "attack_patterns": ["アクセス拒否", "権限剥奪", "ポリシー混乱"],
        "weakness": "最小権限の原則",
        "area": "IAM神殿"
    },
    {
        "name": "SQS守護者",
        "service": "Amazon SQS",
        "description": "メッセージを操る川の守護者",
        "hp": 85,
        "attack_patterns": ["メッセージ洪水", "配信遅延", "可視性タイムアウト"],
        "weakness": "キュー管理",
        "area": "SQS川"
    }
]

# Items
ITEMS = [
    {
        "name": "AWS ドキュメント",
        "description": "AWS知識を10回復する",
        "effect": {"aws_knowledge": 10}
    },
    {
        "name": "クラウドコーヒー",
        "description": "集中力を20回復する",
        "effect": {"concentration": 20}
    },
    {
        "name": "モチベーションクッキー",
        "description": "やる気を15回復する",
        "effect": {"motivation": 15}
    },
    {
        "name": "アーキテクチャ図",
        "description": "次の試練でのダメージを半減する",
        "effect": {"damage_reduction": 0.5}
    },
    {
        "name": "クラウドエッセンス",
        "description": "全てのステータスを少し回復する",
        "effect": {"motivation": 10, "aws_knowledge": 5, "concentration": 10}
    }
]

# Skills (unlocked as player progresses)
SKILLS = [
    {
        "name": "基本コマンド",
        "level_required": 1,
        "description": "基本的なAWSコマンドを使用する",
        "power": 10
    },
    {
        "name": "リソース最適化",
        "level_required": 3,
        "description": "AWSリソースを最適化して攻撃する",
        "power": 20
    },
    {
        "name": "クラウドアーキテクト",
        "level_required": 5,
        "description": "高度なアーキテクチャ知識で攻撃する",
        "power": 30
    },
    {
        "name": "サーバーレスマスター",
        "level_required": 7,
        "description": "サーバーレスの力を解き放つ",
        "power": 40
    },
    {
        "name": "クラウドネイティブ",
        "level_required": 10,
        "description": "クラウドの真髄を理解した究極の技",
        "power": 50
    }
]
