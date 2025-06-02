# 必要なPythonライブラリをインポート
import streamlit as st
import boto3

# フロントエンド
st.title("おしえて！ Bedrock")
prompt = st.text_input("質問を入力", "KAGのゆるキャラの名前は？")

# AWS SDK for Pythonで、Bedrock用のAPIクライアントを作成
client = boto3.client("bedrock-runtime")

# ボタンをクリックしたら実行
if st.button("送信"):

    # Converse APIで推論を行う
    response = client.converse(
        modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": prompt}]
        }]
    )
    
    # 回答を表示
    answer = response["output"]["message"]["content"][0]["text"]
    st.write(answer)