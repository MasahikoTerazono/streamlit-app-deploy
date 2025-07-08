import streamlit as st
import os
import datetime

# 設定
st.set_page_config(page_title="専門家LLMアプリ", layout="centered")

# ヘルスチェックとパッケージ検証
def check_environment():
    """環境とパッケージの状態をチェック"""
    health_status = {'streamlit': True, 'os': True, 'datetime': True, 'basic_functions': True}
    packages_status = {}
    
    # パッケージチェック
    checks = [
        ('python-dotenv', lambda: __import__('dotenv').load_dotenv()),
        ('langchain-openai', lambda: __import__('langchain_openai')),
        ('langchain-core', lambda: __import__('langchain_core.messages'))
    ]
    
    for name, check_func in checks:
        try:
            check_func()
            packages_status[name] = {'status': 'OK', 'error': None}
        except ImportError:
            packages_status[name] = {'status': 'missing', 'error': 'インストールされていません'}
        except Exception as e:
            packages_status[name] = {'status': 'error', 'error': str(e)}
    
    return health_status, packages_status

health_status, packages_status = check_environment()

# メイン UI
st.title("🧠 専門家LLMアプリ")
st.markdown("**AI専門家に質問して、専門的なアドバイスを受けることができます。**")

# アプリ概要
st.markdown("---")
st.subheader("📖 アプリの概要")
st.markdown("""
このアプリは、**AI技術を活用した専門家相談システム**です。

### 🎯 主な特徴
- 🧠 **心理カウンセラー**: 心の悩みや人間関係についてのアドバイス
- 💰 **金融アドバイザー**: 投資・貯蓄・資産運用に関する専門的なサポート
- 🚀 **キャリアコーチ**: 転職・昇進・スキルアップの実践的ガイダンス
- 💻 **ITコンサルタント**: 技術的課題やデジタル化への専門的助言
- ⚕️ **医療アドバイザー**: 健康管理や予防に関する一般的な情報提供

### 📋 操作方法
1. 専門家を選択 → 2. 質問を入力 → 3. 質問ボタンをクリック → 4. 回答を確認

### ⚠️ 注意事項
このサービスは情報提供のみを目的とし、専門的な診断や治療の代替ではありません。
""")

# システム情報
with st.expander("🔧 システム情報・デバッグ", expanded=False):
    st.write("📋 パッケージ確認結果:")
    for package_name, info in packages_status.items():
        if info['status'] == 'OK':
            st.success(f"✅ {package_name}: インストール済み")
        else:
            st.error(f"❌ {package_name}: {info['error']}")
            if info['status'] == 'missing':
                st.code(f"pip install {package_name}")
    
    st.write("**環境設定状況:**")
    env_file_path = os.path.join(os.getcwd(), '.env')
    st.write(f"📁 作業ディレクトリ: {os.getcwd()}")
    st.write(f"📄 .envファイル存在: {'✅' if os.path.exists(env_file_path) else '❌'}")
    
    api_key_env = os.getenv("OPENAI_API_KEY")
    if api_key_env:
        masked_key = api_key_env[:8] + "..." + api_key_env[-4:] if len(api_key_env) > 12 else "設定済み"
        st.write(f"🔑 環境変数 OPENAI_API_KEY: {masked_key}")
    else:
        st.write("🔑 環境変数 OPENAI_API_KEY: 未設定")

# API設定状況
st.markdown("---")
st.subheader("🔑 API設定状況")

def get_api_key():
    """APIキーを安全に取得"""
    # Community Cloud
    try:
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            st.info("🌐 Streamlit Community Cloud環境で動作中")
            return st.secrets['OPENAI_API_KEY']
    except Exception:
        pass
    
    # ローカル環境
    if packages_status.get('python-dotenv', {}).get('status') == 'OK':
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception:
            pass
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.info("💻 ローカル開発環境で動作中")
    return api_key

api_key = get_api_key()

if not api_key:
    st.error("❌ OpenAI APIキーが設定されていません")
    env_file_path = os.path.join(os.getcwd(), '.env')
    
    if os.path.exists(env_file_path):
        st.warning("⚠️ .envファイルは存在しますが、APIキーが正しく読み込まれていません。")
        st.info("**トラブルシューティング:** 1. .envファイルの内容確認 2. 形式確認 (`OPENAI_API_KEY=your_key`) 3. アプリ再起動")
    else:
        st.info("**設定方法:** プロジェクトフォルダに `.env` ファイルを作成し、`OPENAI_API_KEY=your_key`を記述")
    
    st.info("**APIキー取得:** [OpenAI API Keys](https://platform.openai.com/api-keys)")
    st.warning("⚠️ APIキーが設定されるまで、AI機能は利用できません。")
else:
    st.success("✅ OpenAI APIキーが正常に設定されています")
    st.sidebar.success("🔑 APIキー設定済み")
    st.sidebar.write(f"📏 APIキーの長さ: {len(api_key)} 文字")

# 専門家選択
st.markdown("---")
st.subheader("💬 専門家との対話")

expert_data = {
    "心理カウンセラー": {
        "description": "🧠 心の悩みや人間関係について優しくアドバイスします",
        "tip": "具体的な状況や感情を詳しく教えてください。例：「職場で上司との関係がうまくいかず、毎日ストレスを感じています」",
        "icon": "🧠",
        "system_msg": """あなたは経験豊富で優しい心理カウンセラーです。
        - 相談者の心に寄り添い、共感的に対応してください
        - 判断を押し付けず、相談者が自分で答えを見つけられるようサポートしてください
        - 心理学的な知見を分かりやすく説明してください
        - 深刻な問題の場合は専門機関への相談を勧めてください"""
    },
    "金融アドバイザー": {
        "description": "💰 投資、貯蓄、資産運用について専門的にサポートします",
        "tip": "現在の状況（年収、貯蓄額、投資経験など）を可能な範囲で教えてください。例：「30代、年収500万円、投資未経験で老後資金を考え始めました」",
        "icon": "💰",
        "system_msg": """あなたは専門的な知識を持つ金融アドバイザーです。
        - 投資、貯蓄、保険、税務について正確で実践的なアドバイスを提供してください
        - リスクとリターンについて明確に説明してください
        - 個人の状況に合わせた具体的な提案をしてください
        - 最新の金融市場の動向を考慮してください"""
    },
    "キャリアコーチ": {
        "description": "🚀 転職、昇進、スキルアップについて実践的にガイドします",
        "tip": "現在の職種、経験年数、目標を明確にしてください。例：「営業職5年目、マネジメント職への転向を考えています」",
        "icon": "🚀",
        "system_msg": """あなたは親身で実践的なキャリアコーチです。
        - 転職、昇進、スキルアップについて前向きで具体的なアドバイスをしてください
        - 相談者の強みを見つけて伸ばす方法を提案してください
        - 実現可能なアクションプランを一緒に考えてください
        - 業界の動向やトレンドを踏まえた助言をしてください"""
    },
    "ITコンサルタント": {
        "description": "💻 技術的な課題やデジタル化について専門的に助言します",
        "tip": "技術的な背景や課題の詳細を教えてください。例：「小規模ECサイトの運営で、セキュリティ強化を検討しています」",
        "icon": "💻",
        "system_msg": """あなたは経験豊富なITコンサルタントです。
        - 技術的な課題について専門的で実践的な解決策を提案してください
        - 最新の技術トレンドとベストプラクティスを考慮してください
        - ビジネス視点も含めた総合的なアドバイスを提供してください
        - 分かりやすい例や図解で説明してください"""
    },
    "医療アドバイザー": {
        "description": "⚕️ 健康管理や医療に関する一般的な情報を提供します",
        "tip": "症状の詳細や期間を教えてください。例：「最近疲れやすく、健康的な生活習慣について知りたいです」",
        "icon": "⚕️",
        "system_msg": """あなたは医療知識を持つアドバイザーです。
        - 健康管理や予防について一般的な情報を提供してください
        - 科学的根拠に基づいた情報を分かりやすく説明してください
        - 症状が深刻な場合は必ず医療機関での受診を勧めてください
        - 自己診断や自己治療は避けるよう注意を促してください"""
    }
}

expert_type = st.radio("相談したい専門家を選択してください：", list(expert_data.keys()), horizontal=True)
st.info(f"選択中: {expert_data[expert_type]['description']}")
st.info(f"💡 **質問のヒント**: {expert_data[expert_type]['tip']}")

user_input = st.text_area(
    "質問を入力してください", 
    height=100,
    placeholder=f"{expert_type}への相談内容を詳しく入力してください...",
    key="user_input_text"
)

response_area = st.empty()

# LLM関数
def get_expert_response(user_input: str, expert_type: str, api_key: str) -> str:
    """専門家として回答を生成"""
    if not api_key:
        raise Exception("APIキーが設定されていません")
    if not user_input.strip():
        raise Exception("質問が入力されていません")
    
    # パッケージチェック
    for pkg in ['langchain-openai', 'langchain-core']:
        if packages_status.get(pkg, {}).get('status') != 'OK':
            raise Exception(f"{pkg}が正常にインストールされていません")
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        
        llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo", temperature=0.7)
        messages = [
            SystemMessage(content=expert_data[expert_type]['system_msg']),
            HumanMessage(content=f"【{expert_type}への相談】\n{user_input}")
        ]
        
        response = llm.invoke(messages)
        if not response or not hasattr(response, 'content'):
            raise Exception("LLMから有効な回答を取得できませんでした")
        
        return response.content
        
    except ImportError as e:
        raise Exception(f"必要なパッケージがインストールされていません: {e}")
    except Exception as e:
        error_msg = str(e)
        if any(word in error_msg.lower() for word in ["api", "key"]):
            raise Exception(f"OpenAI APIエラー: {e}")
        elif any(word in error_msg.lower() for word in ["network", "connection"]):
            raise Exception(f"ネットワークエラー: {e}")
        else:
            raise Exception(f"LLM呼び出し中にエラーが発生しました: {e}")

# メイン実行
if st.button("質問する", key="ask_button"):
    if not api_key:
        st.error("❌ OpenAI APIキーが設定されていません。")
        st.info("上記の「API設定状況」セクションを参考に、APIキーを設定してください。")
    elif not user_input.strip():
        st.warning("⚠️ 質問を入力してください。")
    else:
        missing_packages = [name for name, info in packages_status.items() if info['status'] != 'OK']
        
        if missing_packages:
            st.error(f"❌ 必要なパッケージが不足しています: {', '.join(missing_packages)}")
            st.code("pip install python-dotenv langchain-openai langchain-core")
        else:
            try:
                with st.spinner(f"{expert_type}が回答を考えています..."):
                    response_content = get_expert_response(user_input, expert_type, api_key)
                
                icon = expert_data[expert_type]['icon']
                response_area.markdown(f"### {icon} {expert_type}からの回答\n\n{response_content}")
                st.success("✅ 回答が完了しました！")
                
            except Exception as e:
                error_message = str(e)
                st.error(f"❌ エラーが発生しました: {error_message}")
                
                # エラー別ヘルプ
                if any(word in error_message for word in ["APIキー", "api"]):
                    st.info("🔑 **APIキーの問題**: 上記の「API設定状況」セクションを参考に設定してください。")
                elif any(word in error_message for word in ["パッケージ", "インストール"]):
                    st.info("📦 **パッケージの問題**: 以下のコマンドで再インストールしてください。")
                    st.code("pip install --upgrade python-dotenv langchain-openai langchain-core")
                elif "ネットワーク" in error_message:
                    st.info("🌐 **ネットワークの問題**: インターネット接続を確認してください。")
                else:
                    st.info("🔧 **トラブルシューティング**: 1. APIキー確認 2. ネット接続確認 3. 時間をおいて再試行")
                
                # デバッグ情報
                with st.expander("🔍 デバッグ情報", expanded=False):
                    st.write(f"**エラー詳細**: {error_message}")
                    st.write(f"**選択された専門家**: {expert_type}")
                    st.write(f"**入力文字数**: {len(user_input)}")
                    st.write(f"**APIキー設定状況**: {'設定済み' if api_key else '未設定'}")
                    st.write(f"**パッケージ状況**: {packages_status}")