# 必要なPyhtonライブラリをインポート
import boto3

# AWS SDK for Pythonで、Bedrock用のAPIクライアントを作成
client = boto3.client("bedrock-runtime")

# Converse Stream APIでストリーミング推論を行う
response = client.converse_stream(
    modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
    messages=[{
        "role": "user",
        "content": [{"text": "KAGのゆるキャラの名前は？"}]
    }]
)

# ストリーミングレスポンスを自動待機し、チャンクごとにプリント
for event in response['stream']:
    if 'contentBlockDelta' in event:
        if 'delta' in event['contentBlockDelta']:
            if 'text' in event['contentBlockDelta']['delta']:
                print(event['contentBlockDelta']['delta']['text'], end='', flush=True)

print()  # 最後に改行