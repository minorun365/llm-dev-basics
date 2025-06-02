# 必要なPythonライブラリをインポート
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from langchain_community.vectorstores import FAISS

# 生成AIモデルを設定
llm = ChatBedrockConverse(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0
)

embeddings = BedrockEmbeddings(
    model_id="cohere.embed-multilingual-v3"
)

# ========================================
# 社内文書を定義
# ========================================
documents = [
    Document(
        page_content="かぐたんはKAG社のSlackチャットボットです。",
        metadata={"title": "かぐたん", "id": 0}
    ),
    Document(
        page_content="カグカグはKAG社のゆるキャラです。",
        metadata={"title": "カグカグ", "id": 1}
    )
]

# ========================================
# 社内文書をベクトルに変換
# ========================================
print("【ベクトルデータを準備】")

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

print("ベクトルストアの構築が完了しました。")
print()

# ========================================
# 検索を実行
# ========================================
query = "KAG社のゆるキャラの名前は？"

# Retrieverを実行（上位1件を取得）
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
retrieved_docs = retriever.invoke(query)
context = retrieved_docs[0].page_content

print("【検索結果】")
print("クエリ： ", query)
print("結果：", retrieved_docs)
print()

# ========================================
# LLMの推論
# ========================================
# プロンプトテンプレートを定義
prompt = ChatPromptTemplate.from_template(
    "質問： {question} / コンテキスト： {context}"
)

print("【プロンプト】")
print(f"質問： {query} / コンテキスト： {context}")
print()

# LCELを使ってRAGチェーンを構築
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# RAGチェーンを実行
print("【LLMの回答】")
result = rag_chain.invoke(query)
print(result)