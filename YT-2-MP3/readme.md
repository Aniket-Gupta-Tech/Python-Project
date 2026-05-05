# YT-2-MP3

A simple web-based YouTube to MP3 converter built with **Streamlit** and **yt-dlp**. Paste a YouTube URL, hit download, and get your MP3 file — right from the browser.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Paste any YouTube video URL and convert it to MP3
- Best-quality audio extraction (192 kbps)
- In-browser download button for the converted file
- Minimal, clean Streamlit UI

## Tech Stack

| Component | Tool |
|-----------|------|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| YouTube Downloader | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| Audio Conversion | [FFmpeg](https://ffmpeg.org/) (required on system PATH) |

## Prerequisites

- **Python 3.10+**
- **FFmpeg** installed and available on your system PATH
  - Windows: download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to PATH
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Installation

```bash
# Clone the repository
git clone https://github.com/Mr-Aniket-Gupta/YT-2-MP3.git
cd YT-2-MP3

# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run yt-mp.py
```

The app will open in your default browser at `http://localhost:8501`.

1. Paste a YouTube video URL into the text input.
2. Click **Download MP3**.
3. Once conversion finishes, click **Download MP3 File** to save it locally.

## Project Structure

```
YT-2-MP3/
├── yt-mp.py           # Main Streamlit application
├── requirements.txt   # Python dependencies
└── readme.md          # Project documentation
```

## How It Works

1. The user provides a YouTube URL through the Streamlit interface.
2. `yt-dlp` downloads the best available audio stream.
3. FFmpeg (via yt-dlp's post-processor) converts the audio to MP3 at 192 kbps.
4. The converted file is served back through a Streamlit download button.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

---

Made by [Aniket Gupta](https://github.com/Mr-Aniket-Gupta)
