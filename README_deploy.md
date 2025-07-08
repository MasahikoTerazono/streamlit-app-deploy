# 🧠 専門家LLMアプリ

AI技術を活用した専門家相談システムです。様々な分野の専門家として振る舞うAIに、気軽に相談することができます。

## 🎯 主な特徴

- 🧠 **心理カウンセラー**: 心の悩みや人間関係についてのアドバイス
- 💰 **金融アドバイザー**: 投資・貯蓄・資産運用に関する専門的なサポート
- 🚀 **キャリアコーチ**: 転職・昇進・スキルアップの実践的ガイダンス
- 💻 **ITコンサルタント**: 技術的課題やデジタル化への専門的助言
- ⚕️ **医療アドバイザー**: 健康管理や予防に関する一般的な情報提供

## 🚀 デプロイ方法（Streamlit Community Cloud）

### 1. 前提条件
- Python 3.11
- OpenAI API キー

### 2. Streamlit Community Cloudでのデプロイ

1. **GitHubリポジトリを作成**
   - このプロジェクトをGitHubにプッシュ

2. **Streamlit Community Cloudにアクセス**
   - [https://share.streamlit.io/](https://share.streamlit.io/) にアクセス
   - GitHubアカウントでログイン

3. **新しいアプリをデプロイ**
   - "New app" をクリック
   - リポジトリを選択
   - ブランチ: `main`
   - メインファイル: `app.py`

4. **環境変数を設定**
   - Advanced settings を開く
   - Secrets に以下を追加:
   ```
   OPENAI_API_KEY = "your_actual_api_key_here"
   ```

5. **デプロイ実行**
   - "Deploy!" をクリック

### 3. ローカル開発

```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements_cloud.txt

# 環境変数を設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定

# アプリを起動
streamlit run app.py
```

## 📁 プロジェクト構造

```
.
├── app.py                 # メインアプリケーション
├── requirements_cloud.txt # 本番用依存関係
├── .python-version       # Python バージョン指定
├── .env.example          # 環境変数のテンプレート
├── .streamlit/
│   └── config.toml       # Streamlit設定
└── README.md             # このファイル
```

## ⚠️ 注意事項

- このサービスは情報提供のみを目的としており、専門的な診断や治療の代替ではありません
- 重要な決定の前には、必ず実際の専門家にご相談ください
- 緊急の場合は、適切な専門機関に直接ご連絡ください

## 🔧 技術スタック

- **フレームワーク**: Streamlit
- **AI**: OpenAI GPT-3.5/4 (langchain-openai)
- **言語**: Python 3.11
- **デプロイ**: Streamlit Community Cloud
