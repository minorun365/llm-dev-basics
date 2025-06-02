# 必要なPythonライブラリをインポート
import json
import urllib.request
from strands import Agent, tool

# Strandsのデコレーターでツールを定義
@tool
def get_holidays(year):
    url = f"https://holidays-jp.github.io/api/v1/{year}/date.json"
    with urllib.request.urlopen(url) as response:
        data = response.read()
        holidays = json.loads(data)
    return holidays

# エージェントを作成
agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    system_prompt="あなたは日本の祝日を調べるプロフェッショナルです。",
    tools=[get_holidays],
)

# エージェントを実行
agent("2025年6月の祝日はいつ？")