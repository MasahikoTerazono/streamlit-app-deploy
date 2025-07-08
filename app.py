import os
import streamlit as st
import datetime

# 基本テスト用の簡素なバージョン
st.write("🔧 デバッグモード - アプリの起動テスト")
st.write(f"現在時刻: {datetime.datetime.now()}")
st.write("基本的なStreamlit機能は動作しています")

# 環境変数テスト
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    st.write("✅ python-dotenvの読み込み成功")
    st.write(f"APIキー取得: {'成功' if api_key else '失敗'}")
except ImportError as e:
    st.error(f"❌ python-dotenvのインポートエラー: {e}")

# langchain-openaiテスト
try:
    from langchain_openai import ChatOpenAI
    st.write("✅ langchain-openaiの読み込み成功")
except ImportError as e:
    st.error(f"❌ langchain-openaiのインポートエラー: {e}")

# langchainテスト
try:
    from langchain.schema import SystemMessage, HumanMessage
    st.write("✅ langchainの読み込み成功")
except ImportError as e:
    st.error(f"❌ langchainのインポートエラー: {e}")

st.success("アプリの基本構造は正常に動作しています！")

# Streamlit設定（最初に実行する必要がある）
st.set_page_config(
    page_title="専門家LLMアプリ", 
    page_icon="🧠",
    layout="wide"
)

# 環境変数読み込み（.envファイルから）
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# デバッグ情報をより詳細に表示
st.sidebar.write("🔧 デバッグ情報")
st.sidebar.write(f"現在時刻: {datetime.datetime.now().strftime('%H:%M:%S')}")
st.sidebar.write(f"APIキーの長さ: {len(api_key) if api_key else 0}")
if api_key:
    st.sidebar.write(f"🔍 APIキー（マスク済）: {api_key[:5]}*****")
    st.sidebar.success("✅ APIキー設定済み")
else:
    st.sidebar.error("❌ APIキー未設定")
    st.sidebar.write("環境変数OPENAI_API_KEYを確認してください")

# エラーメッセージを表示（st.stop()を一時的に無効化）
if not api_key:
    st.error("OpenAI APIキーが設定されていません。`.env`ファイルを確認してください。")
    st.write("⚠️ APIキーがないため、一部機能が制限されます。")
    # st.stop()  # 一時的にコメントアウト

# キャッシュクリア機能
if st.sidebar.button("🔄 アプリをリフレッシュ"):
    st.rerun()

if st.sidebar.button("🗑️ セッションクリア"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Streamlit 画面構成
st.title("🧠 専門家に聞けるLLMアプリ")
st.markdown("このアプリでは、専門家に質問するようにLLMに問い合わせができます。質問内容と専門家タイプを選んでください。")

# 一意のIDを表示してキャッシュ問題を確認
st.caption(f"アプリバージョン: v2.0 - 更新時刻: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.success("✅ 新しいバージョンのアプリが正常に読み込まれました！")

# ラジオボタンで専門家の種類を選択
role = st.radio("専門家の種類を選んでください：", ["心理カウンセラー", "金融アドバイザー", "キャリアコーチ"])

# 質問入力欄
user_input = st.text_input("質問を入力してください")

# 回答関数（プロンプトをロールに応じて切り替え）
def get_answer_by_expert(role: str, query: str) -> str:
    system_prompt = {
        "心理カウンセラー": "あなたは優しい心理カウンセラーです。利用者の心を軽くするように答えてください。",
        "金融アドバイザー": "あなたは専門的な知識を持つ金融アドバイザーです。正確で簡潔に答えてください。",
        "キャリアコーチ": "あなたは親身で実践的なキャリアコーチです。前向きで具体的なアドバイスをしてください。"
    }.get(role, "")

    chat = ChatOpenAI(
        temperature=0.3, 
        model="gpt-3.5-turbo",
        api_key=api_key  # APIキーを明示的に渡す
    )
    response = chat([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])
    return response.content

# 実行ボタン
if st.button("質問する", key="submit") and user_input and api_key:
    with st.spinner("考え中..."):
        try:
            answer = get_answer_by_expert(role, user_input)
            st.markdown("### 📝 回答：")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
            st.write("APIキーが正しく設定されているか確認してください。")
elif st.button("質問する", key="no_input") and not user_input:
    st.warning("⚠️ 質問を入力してください。")
elif st.button("質問する", key="no_key") and not api_key:
    st.error("❌ OpenAI APIキーが設定されていません。")