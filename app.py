import streamlit as st

# 🚨 set_page_config は最初に書く（これが原因でエラーになりがち）
st.set_page_config(
    page_title="専門家LLMアプリ", 
    page_icon="🧠",
    layout="wide"
)

import os
import datetime

# dotenv 読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    st.write("✅ python-dotenvの読み込み成功")
    st.write(f"APIキー取得: {'成功' if api_key else '失敗'}")
except ImportError as e:
    st.error(f"❌ python-dotenvのインポートエラー: {e}")

# langchain-openai 読み込み
try:
    from langchain_openai import ChatOpenAI
    st.write("✅ langchain-openaiの読み込み成功")
except ImportError as e:
    st.error(f"❌ langchain-openaiのインポートエラー: {e}")

# langchain 読み込み
try:
    from langchain.schema import SystemMessage, HumanMessage
    st.write("✅ langchainの読み込み成功")
except ImportError as e:
    st.error(f"❌ langchainのインポートエラー: {e}")

st.write(f"現在時刻: {datetime.datetime.now()}")
st.write("基本的なStreamlit機能は動作しています")
st.success("アプリの基本構造は正常に動作しています！")

# サイドバーの表示
st.sidebar.write("🔧 デバッグ情報")
st.sidebar.write(f"現在時刻: {datetime.datetime.now().strftime('%H:%M:%S')}")
st.sidebar.write(f"APIキーの長さ: {len(api_key) if api_key else 0}")
if api_key:
    st.sidebar.write(f"🔍 APIキー（マスク済）: {api_key[:5]}*****")
    st.sidebar.success("✅ APIキー設定済み")
else:
    st.sidebar.error("❌ APIキー未設定")

# セーフティ：APIキー未設定なら警告
if not api_key:
    st.error("OpenAI APIキーが設定されていません。`.env`ファイルを確認してください。")
    st.write("⚠️ APIキーがないため、一部機能が制限されます。")

# キャッシュクリア機能
if st.sidebar.button("🔄 アプリをリフレッシュ"):
    st.rerun()
if st.sidebar.button("🗑️ セッションクリア"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# アプリのメイン画面
st.title("🧠 専門家に聞けるLLMアプリ")
st.markdown("このアプリでは、専門家に質問するようにLLMに問い合わせができます。質問内容と専門家タイプを選んでください。")

# ラジオボタンで専門家の種類を選択
role = st.radio("専門家の種類を選んでください：", ["心理カウンセラー", "金融アドバイザー", "キャリアコーチ"])

# 質問入力欄
user_input = st.text_input("質問を入力してください")

# 回答生成関数
def get_answer_by_expert(role: str, query: str) -> str:
    system_prompt = {
        "心理カウンセラー": "あなたは優しい心理カウンセラーです。利用者の心を軽くするように答えてください。",
        "金融アドバイザー": "あなたは専門的な知識を持つ金融アドバイザーです。正確で簡潔に答えてください。",
        "キャリアコーチ": "あなたは親身で実践的なキャリアコーチです。前向きで具体的なアドバイスをしてください。"
    }.get(role, "")

    chat = ChatOpenAI(
        temperature=0.3, 
        model="gpt-3.5-turbo",
        api_key=api_key
    )
    response = chat([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])
    return response.content

# 質問ボタンの処理
if st.button("質問する") and user_input and api_key:
    with st.spinner("考え中..."):
        try:
            answer = get_answer_by_expert(role, user_input)
            st.markdown("### 📝 回答：")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            st.write("APIキーが正しく設定されているか確認してください。")
elif st.button("質問する") and not user_input:
    st.warning("⚠️ 質問を入力してください。")
elif st.button("質問する") and not api_key:
    st.error("❌ OpenAI APIキーが設定されていません。")