import { useState, useEffect } from 'react';
import './App.css';

// # React（りあくと）のメインコンポーネントです
function App() {
  const [file, setFile] = useState<File | null>(null);
  const [transcription, setTranscription] = useState("ここに結果が表示されます");
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<string>("未確認");

  // # API（えーぴーあい：外部プログラムとの接点）のベースURLを決定する関数
  const getApiBaseUrl = () => {
    // # 【修正済み】Hugging FaceのURLを正確に記述しました
    // # セキュリティ上の注意: このURLは公開されるものなので、機密情報（パスワードなど）は含めないでください。
    const HF_SPACE_URL = "https://yg5555-whisper.hf.space";

    // # 環境変数 VITE_API_BASE（ゔぃーと・えーぴーあい・べーす）があるか確認します
    const envBase = import.meta.env.VITE_API_BASE;

    // # 環境変数が設定されていればそれを使用（Renderの設定画面で指定可能）
    if (envBase && envBase.trim() !== '') {
      return envBase.replace(/\/$/, '');
    }

    // # 本番環境（PROD：ぷろど）であれば、Hugging FaceのURLを返します
    if (import.meta.env.PROD) {
      return HF_SPACE_URL;
    }

    // # 自分のPCで開発中であれば localhost（ろーかるほすと）を使用します
    return 'http://localhost:8000';
  };

  // # サーバーが生きているか（Health Check：へるすちぇっく）確認する関数
  const checkApiHealth = async () => {
    try {
      const base = getApiBaseUrl();
      const healthUrl = `${base}/api/health`;

      console.log('接続確認先:', healthUrl);

      // # ネットワーク経由でデータを取得（fetch：ふぇっち）します
      const response = await fetch(healthUrl);

      if (!response.ok) {
        setApiStatus(`接続エラー: ${response.status}`);
        return;
      }

      const data = await response.json();
      if (data.status === 'ok') {
        setApiStatus('接続OK');
      }
    } catch (error) {
      setApiStatus('接続失敗');
      console.error('API接続に失敗しました。URLが正しいか、HF側が起動しているか確認してください:', error);
    }
  };

  // # コンポーネントが表示された時に1回だけ実行される処理（useEffect：ゆーずえふぇくと）
  useEffect(() => {
    checkApiHealth();
  }, []);

  // # 音声ファイルをアップロードして文字起こしを依頼する処理
  const handleUpload = async () => {
    if (!file) return;

    setIsLoading(true);
    // # ファイルを送るための形式（FormData：ふぉーむでーた）を作成
    const formData = new FormData();
    formData.append("file", file);

    try {
      const base = getApiBaseUrl();
      const apiUrl = `${base}/api/transcribe`;

      console.log('送信開始:', apiUrl);

      const response = await fetch(apiUrl, {
        method: "POST", // # データを送る（POST：ぽすと）
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`サーバーエラー: ${response.status}`);
      }

      const data = await response.json();

      // # 成功したら文字起こし結果を画面に反映
      setTranscription(data.transcription || "結果が空でした");
    } catch (error) {
      console.error("文字起こし失敗:", error);
      setTranscription(`エラー: ${error instanceof Error ? error.message : '通信に失敗しました'}`);
    } finally {
      setIsLoading(false);
    }
  };

  // # 結果を .txt や .json で保存（Download：だうんろーど）する処理
  const handleDownload = (format: "txt" | "json") => {
    if (transcription === "ここに結果が表示されます" || transcription.startsWith("エラー")) {
      return;
    }

    const content = format === "json"
      ? JSON.stringify({ transcription }, null, 2)
      : transcription;

    // # ブラウザ上で一時的なファイル（Blob：ぶろぶ）を作成してダウンロード
    const blob = new Blob([content], { type: format === "json" ? "application/json" : "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `transcription.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Whisper Transcriber</h1>

      {/* # 接続状態の表示エリア */}
      <div className="api-status">
        <span>API接続状態: {apiStatus}</span>
        <button onClick={checkApiHealth} className="health-check-button" disabled={isLoading}>
          再試行
        </button>
      </div>

      <div className="upload-section">
        {/* # ファイル選択（input：いんぷっと） */}
        <input
          type="file"
          onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
          accept="audio/*,.mp3,.wav,.m4a,.flac"
          disabled={isLoading}
        />
        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={isLoading || !file}
        >
          {isLoading ? '解析中...' : 'アップロードして文字起こし'}
        </button>
      </div>

      <div className="result-container">
        <h2 className="result-title">文字起こし結果</h2>
        {/* # 結果表示エリア（textarea：てきすとえりあ） */}
        <textarea
          className="result-text"
          rows={10}
          readOnly
          value={transcription}
          placeholder={isLoading ? 'サーバーでWhisperが解析中です。しばらくお待ちください...' : 'ここに結果が表示されます'}
        />
        <div className="download-buttons">
          <button onClick={() => handleDownload("txt")} disabled={isLoading || transcription.startsWith("ここに")}>
            .txt保存
          </button>
          <button onClick={() => handleDownload("json")} disabled={isLoading || transcription.startsWith("ここに")}>
            .json保存
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;