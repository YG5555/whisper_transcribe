# Whisper Transcribe - 音声文字起こしWebアプリケーション

OpenAIのWhisperモデルを活用した、音声ファイルをテキストに変換するWebアプリケーションです。

## 📋 目次

- [プロジェクト概要](#プロジェクト概要)
- [主な機能](#主な機能)
- [技術スタック](#技術スタック)
- [関連ドキュメント](#関連ドキュメント)

## 🎯 プロジェクト概要

このプロジェクトは、OSSのAIモデルであるWhisperを活用した音声文字起こしWebアプリケーションです。音声ファイルをアップロードすることで、自動的にテキストに変換します。

### 開発目的

- 開発・技術に対する理解を深めるための実践的な個人開発
- AIエージェント（ChatGPT、Cursor、Gemini）との対話を通じたバイブコーディングによる学習

### 企画書

- [企画書](https://www.notion.so/22a932a86f6280e79e7dfb44d3797e11?source=copy_link)

## ✨ 主な機能

- **音声ファイルのアップロード**: MP3、WAV、M4A、FLAC、OGG形式に対応
- **自動文字起こし**: Whisperモデルによる高精度な音声認識
- **結果の表示・ダウンロード**: テキスト形式（.txt）およびJSON形式（.json）で結果を取得可能
- **複数の実行モード**: 
  - ローカルUIモード（NiceGUI）
  - APIモード（FastAPI + React）

## 🛠 技術スタック

### バックエンド
- **Python 3.11**
- **FastAPI**: RESTful APIサーバー
- **Whisper**: OpenAIの音声認識モデル
- **Uvicorn**: ASGIサーバー

### フロントエンド
- **React**: UIフレームワーク
- **Vite**: ビルドツール

### ローカル開発
- **NiceGUI**: ローカルUI開発用フレームワーク

### デプロイ
- **Render**: クラウドホスティング

## 📚 関連ドキュメント

### モード別のドキュメント

- [ローカルUI構成（NiceGUI 直結）](./README_local.md)
- [API構成（FastAPI + UI）](./README_API.md)

### テスト・開発ドキュメント

- [連携テスト手順](./README_連携テスト.md)
- [フロントエンドテスト](./README_TEST_frontend.md)

## 🔧 設定

### Whisperモデルの設定

`backend/app/config.py` で以下の設定が可能です：

- **MODEL_NAME**: 使用するWhisperモデル（tiny, base, small, medium, large）
- **LANGUAGE**: 認識言語（デフォルト: ja）
- **メモリ効率化設定**: メモリ使用量を最適化するための設定

環境変数でも設定可能：

```bash
export WHISPER_MODEL=base
export MEMORY_LIMIT_MB=512
```

## 📝 ライセンス

このプロジェクトは個人開発の学習目的で作成されています。

## 🤝 貢献

このプロジェクトは個人開発の学習プロジェクトです。フィードバックや提案は歓迎します。
