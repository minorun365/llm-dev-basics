# 必要なPythonライブラリをインポート
import json
import asyncio
import urllib.request
import streamlit as st
from strands import Agent, tool

# フロントエンド
st.title("おしえて！ Strandsエージェント")
question = st.text_input("質問を入力", "2025年6月の祝日はいつ？")

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

# 非同期ストリーミング処理
async def process_stream(question, container):
    text_holder = container.empty()
    response = ""
    shown_tools = set()

    # エージェントからのストリーミングレスポンスを処理    
    async for chunk in agent.stream_async(question):
        if isinstance(chunk, dict):
            event = chunk.get('event', {})

            # ツール実行を検出して表示
            if 'contentBlockStart' in event:
                tool_use = event['contentBlockStart'].get('start', {}).get('toolUse', {})
                tool_id = tool_use.get('toolUseId')

                # バッファをクリア
                if response:
                    text_holder.markdown(response)
                    response = ""

                # ツール実行のメッセージを表示
                container.info("ツールを実行中…")
                text_holder = container.empty()
            
            # テキストを抽出してリアルタイム表示
            if text := chunk.get('data'):
                response += text
                text_holder.markdown(response)

# ボタンを押したら生成開始
if st.button("質問する"):    
    with st.spinner("回答を生成中…"):
        container = st.container()
        asyncio.run(process_stream(question, container))