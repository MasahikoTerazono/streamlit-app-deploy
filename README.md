# 🧠 専門家LLMアプリ

AI技術を活用した専門家相談システムです。心理カウンセラー、金融アドバイザー、キャリアコーチ、ITコンサルタント、医療アドバイザーの5つの専門分野でAIによる相談サービスを提供します。

## 🚀 デプロイ状況

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## ✨ 機能

- **5つの専門家タイプ**: 心理、金融、キャリア、IT、医療
- **インタラクティブなUI**: 直感的な操作で簡単相談
- **リアルタイム回答**: OpenAI GPT-3.5による即座の専門的アドバイス
- **安全な設定管理**: APIキーの安全な管理

## 🛠️ 技術スタック

- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT-3.5-turbo via LangChain
- **Environment**: Python 3.11+
- **Deployment**: Streamlit Community Cloud

## 📋 必要な環境変数

Streamlit Community Cloudでのデプロイ時は、以下の環境変数を設定してください：

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

## 🚀 ローカル実行

1. リポジトリをクローン
```bash
git clone <your-repo-url>
cd streamlit-app-deploy
```

2. 仮想環境を作成・有効化
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# または
source .venv/bin/activate  # Mac/Linux
```

3. 依存関係をインストール
```bash
pip install -r requirements.txt
```

4. 環境変数を設定
```bash
# .envファイルを作成
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

5. アプリを実行
```bash
streamlit run app.py
```

## 📝 使用方法

1. **専門家を選択**: 相談内容に適した専門家をラジオボタンで選択
2. **質問を入力**: 相談したい内容を入力フィールドに記入
3. **質問ボタンをクリック**: AIが選択された専門家として回答を生成
4. **回答を確認**: 専門的な視点からのアドバイスを受け取る

## ⚠️ 注意事項

このサービスは情報提供のみを目的とし、専門的な診断や治療の代替ではありません。重要な決定の前には、必ず実際の専門家にご相談ください。

## 📄 ライセンス

MIT License

## 🤝 コントリビューション

プルリクエストや課題の報告を歓迎します。

---

Made with ❤️ using Streamlit and OpenAI
