import streamlit as st
import os
import datetime

# 基本的なStreamlitテスト
st.set_page_config(page_title="専門家LLMアプリ", layout="centered")

st.title("🧠 専門家LLMアプリ")
st.markdown("**AI専門家に質問して、専門的なアドバイスを受けることができます。**")

# アプリの概要と操作方法を表示
st.markdown("---")
st.subheader("📖 アプリの概要")
st.markdown("""
このアプリは、**AI技術を活用した専門家相談システム**です。
様々な分野の専門家として振る舞うAIに、気軽に相談することができます。

### 🎯 主な特徴
- 🧠 **心理カウンセラー**: 心の悩みや人間関係についてのアドバイス
- 💰 **金融アドバイザー**: 投資・貯蓄・資産運用に関する専門的なサポート
- 🚀 **キャリアコーチ**: 転職・昇進・スキルアップの実践的ガイダンス
- 💻 **ITコンサルタント**: 技術的課題やデジタル化への専門的助言
- ⚕️ **医療アドバイザー**: 健康管理や予防に関する一般的な情報提供

### 📋 操作方法
1. **専門家を選択**: 相談内容に適した専門家をラジオボタンで選択
2. **質問を入力**: 相談したい内容を入力フィールドに記入
3. **質問ボタンをクリック**: AIが選択された専門家として回答を生成
4. **回答を確認**: 専門的な視点からのアドバイスを受け取る

### ⚠️ 注意事項
- このサービスは**情報提供のみ**を目的としており、専門的な診断や治療の代替ではありません
- 重要な決定の前には、必ず実際の専門家にご相談ください
- 緊急の場合は、適切な専門機関に直接ご連絡ください
""")

st.markdown("---")

# システム情報とデバッグ機能
with st.expander("🔧 システム情報・デバッグ", expanded=False):
    st.write("📋 パッケージ確認中...")
    
    # 1. python-dotenvテスト
    try:
        from dotenv import load_dotenv
        load_dotenv()
        st.success("✅ python-dotenv: インストール済み")
    except ImportError:
        st.error("❌ python-dotenv: インストールされていません")
        st.code("pip install python-dotenv")
    except Exception as e:
        st.error(f"❌ python-dotenv: エラー - {e}")

    # 2. langchain-openaiテスト
    try:
        from langchain_openai import ChatOpenAI
        st.success("✅ langchain-openai: インストール済み")
    except ImportError:
        st.error("❌ langchain-openai: インストールされていません")
        st.code("pip install langchain-openai")
    except Exception as e:
        st.error(f"❌ langchain-openai: エラー - {e}")

    # 3. langchain-coreテスト
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        st.success("✅ langchain-core: インストール済み")
    except ImportError:
        st.error("❌ langchain-core: インストールされていません")
        st.code("pip install langchain-core")
    except Exception as e:
        st.error(f"❌ langchain-core: エラー - {e}")

    st.write(f"🕐 現在時刻: {datetime.datetime.now()}")
    st.success("Streamlitアプリは正常に動作しています")

    # 関数使用例
    st.write("**関数使用例:**")
    st.code("""
# 使用例：
response = get_expert_response(
    user_input="転職を考えているのですが...", 
    expert_type="キャリアコーチ", 
    api_key=your_api_key
)
print(response)  # LLMからの回答が返される
    """)
    st.write("**関数の仕様:**")
    st.write("- 引数: `user_input` (str), `expert_type` (str), `api_key` (str)")
    st.write("- 戻り値: LLMからの回答 (str)")
    st.write("- 例外: ImportError, Exception")

# APIキー設定状況
st.subheader("🔑 API設定状況")

# Streamlit Community Cloud用の環境変数読み込み
api_key = None

# 1. Streamlit Secretsから読み込み（Community Cloud用）
if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
    api_key = st.secrets['OPENAI_API_KEY']
    st.info("🌐 Streamlit Community Cloud環境で動作中")

# 2. 環境変数から読み込み（ローカル開発用）
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.info("💻 ローカル開発環境で動作中")

if not api_key:
    st.error("❌ OpenAI APIキーが設定されていません")
    st.info("""
    **ローカル開発での設定方法:**
    1. プロジェクトフォルダに `.env` ファイルを作成
    2. ファイル内に以下を記述：
    ```
    OPENAI_API_KEY=your_actual_api_key_here
    ```
    
    **Streamlit Community Cloudでの設定方法:**
    1. アプリの設定画面で "Secrets" を開く
    2. 以下を追加：
    ```
    OPENAI_API_KEY = "your_actual_api_key_here"
    ```
    
    **APIキー取得:**
    [OpenAI API Keys](https://platform.openai.com/api-keys) から取得
    """)
    st.warning("⚠️ APIキーが設定されるまで、AI機能は利用できません。")
else:
    st.success("✅ OpenAI APIキーが正常に設定されています")
    st.sidebar.success("🔑 APIキー設定済み")
    st.sidebar.write(f"📏 APIキーの長さ: {len(api_key)} 文字")

st.markdown("---")

# チャット入力
st.subheader("💬 専門家との対話")

# 専門家選択ラジオボタン
expert_type = st.radio(
    "相談したい専門家を選択してください：",
    ["心理カウンセラー", "金融アドバイザー", "キャリアコーチ", "ITコンサルタント", "医療アドバイザー"],
    horizontal=True
)

# 選択された専門家の説明を表示
expert_descriptions = {
    "心理カウンセラー": "🧠 心の悩みや人間関係について優しくアドバイスします",
    "金融アドバイザー": "💰 投資、貯蓄、資産運用について専門的にサポートします",
    "キャリアコーチ": "🚀 転職、昇進、スキルアップについて実践的にガイドします",
    "ITコンサルタント": "💻 技術的な課題やデジタル化について専門的に助言します",
    "医療アドバイザー": "⚕️ 健康管理や医療に関する一般的な情報を提供します"
}

st.info(f"選択中: {expert_descriptions[expert_type]}")

# 質問入力のヒント
st.markdown("### 💡 効果的な質問のコツ")
tips_by_expert = {
    "心理カウンセラー": "具体的な状況や感情を詳しく教えてください。例：「職場で上司との関係がうまくいかず、毎日ストレスを感じています」",
    "金融アドバイザー": "現在の状況（年収、貯蓄額、投資経験など）を可能な範囲で教えてください。例：「30代、年収500万円、投資未経験で老後資金を考え始めました」",
    "キャリアコーチ": "現在の職種、経験年数、目標を明確にしてください。例：「営業職5年目、マネジメント職への転向を考えています」",
    "ITコンサルタント": "技術的な背景や課題の詳細を教えてください。例：「小規模ECサイトの運営で、セキュリティ強化を検討しています」",
    "医療アドバイザー": "症状の詳細や期間を教えてください。例：「最近疲れやすく、健康的な生活習慣について知りたいです」"
}

st.info(f"💡 **質問のヒント**: {tips_by_expert[expert_type]}")

user_input = st.text_area(
    "質問を入力してください", 
    height=100,
    placeholder=f"{expert_type}への相談内容を詳しく入力してください...",
    key="user_input_text"
)

# 応答表示エリア
response_area = st.empty()

# 専門家ごとのシステムメッセージを定義
def get_system_message(expert_type):
    system_messages = {
        "心理カウンセラー": """あなたは経験豊富で優しい心理カウンセラーです。
        - 相談者の心に寄り添い、共感的に対応してください
        - 判断を押し付けず、相談者が自分で答えを見つけられるようサポートしてください
        - 心理学的な知見を分かりやすく説明してください
        - 深刻な問題の場合は専門機関への相談を勧めてください""",
        
        "金融アドバイザー": """あなたは専門的な知識を持つ金融アドバイザーです。
        - 投資、貯蓄、保険、税務について正確で実践的なアドバイスを提供してください
        - リスクとリターンについて明確に説明してください
        - 個人の状況に合わせた具体的な提案をしてください
        - 最新の金融市場の動向を考慮してください""",
        
        "キャリアコーチ": """あなたは親身で実践的なキャリアコーチです。
        - 転職、昇進、スキルアップについて前向きで具体的なアドバイスをしてください
        - 相談者の強みを見つけて伸ばす方法を提案してください
        - 実現可能なアクションプランを一緒に考えてください
        - 業界の動向やトレンドを踏まえた助言をしてください""",
        
        "ITコンサルタント": """あなたは経験豊富なITコンサルタントです。
        - 技術的な課題について専門的で実践的な解決策を提案してください
        - 最新の技術トレンドとベストプラクティスを考慮してください
        - ビジネス視点も含めた総合的なアドバイスを提供してください
        - 分かりやすい例や図解で説明してください""",
        
        "医療アドバイザー": """あなたは医療知識を持つアドバイザーです。
        - 健康管理や予防について一般的な情報を提供してください
        - 科学的根拠に基づいた情報を分かりやすく説明してください
        - 症状が深刻な場合は必ず医療機関での受診を勧めてください
        - 自己診断や自己治療は避けるよう注意を促してください"""
    }
    return system_messages.get(expert_type, "あなたは経験豊富な専門家です。分かりやすく、論理的に説明してください。")

# LLMからの回答を取得する関数
def get_expert_response(user_input: str, expert_type: str, api_key: str) -> str:
    """
    専門家として回答を生成する関数
    
    Args:
        user_input (str): ユーザーの入力テキスト
        expert_type (str): 選択された専門家の種類
        api_key (str): OpenAI APIキー
        
    Returns:
        str: LLMからの回答テキスト
        
    Raises:
        Exception: LLM呼び出し時のエラー
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        
        # LLMインスタンスを作成
        llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # 選択された専門家に応じたシステムメッセージを取得
        system_message_content = get_system_message(expert_type)
        
        # メッセージを構成
        messages = [
            SystemMessage(content=system_message_content),
            HumanMessage(content=f"【{expert_type}への相談】\n{user_input}"),
        ]
        
        # LLMから回答を取得
        response = llm.invoke(messages)
        return response.content
        
    except ImportError as e:
        raise Exception(f"必要なパッケージがインストールされていません: {e}")
    except Exception as e:
        raise Exception(f"LLM呼び出し中にエラーが発生しました: {e}")

# LLM呼び出し
if st.button("質問する", key="ask_button"):
    if not api_key:
        st.error("❌ OpenAI APIキーが設定されていません。.envファイルを確認してください。")
    elif not user_input:
        st.warning("⚠️ 質問を入力してください。")
    else:
        try:
            with st.spinner(f"{expert_type}が回答を考えています..."):
                # 新しい関数を使用してLLMから回答を取得
                response_content = get_expert_response(user_input, expert_type, api_key)
            
            # 専門家の名前とアイコンを一緒に回答を表示
            expert_icons = {
                "心理カウンセラー": "🧠",
                "金融アドバイザー": "💰",
                "キャリアコーチ": "🚀",
                "ITコンサルタント": "💻",
                "医療アドバイザー": "⚕️"
            }
            
            icon = expert_icons.get(expert_type, "👨‍⚕️")
            response_area.markdown(f"### {icon} {expert_type}からの回答\n\n{response_content}")
            
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {e}")
            if "パッケージ" in str(e):
                st.write("以下のコマンドを実行してパッケージをインストールしてください：")
                st.code("pip install python-dotenv langchain-openai langchain-core")
            else:
                st.write("APIキーが正しく設定されているか確認してください。")