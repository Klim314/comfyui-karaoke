# ComfyUI Video Downloader

ComfyUI custom nodes for downloading video/audio via [yt-dlp](https://github.com/yt-dlp/yt-dlp) and feeding the result into the graph. Supports cookie-based authentication so you can use Premium accounts.

Ships three nodes:

- **Video Downloader (yt-dlp)** — fetch a URL to disk, output the file path.
- **Load Audio (from path)** — read a STRING path into ComfyUI's `AUDIO` type, so `audio_only` downloads compose directly with audio-consuming nodes.
- **String → AudioPath** — retype a STRING as `AUDIOPATH` for packs (e.g. UVR5) whose inputs demand that nominal type.

## Features

- Download video (merged to mp4) or audio only (mp3/m4a/opus/wav/flac/aac/vorbis)
- Optional `cookies.txt` for Premium / age-gated / members-only content
- Path-based outputs that compose with [VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) (`VHS_LoadVideo`) for video, and with the bundled `Load Audio (from path)` node for audio-only flows
- Works with any site yt-dlp supports (YouTube, Vimeo, Twitter/X, etc.)

## Install

### Manual

```bash
cd ComfyUI/custom_nodes
git clone <this-repo> comfyui_video_downloader
cd comfyui_video_downloader
pip install -r requirements.txt
```

### With UV (for development)

```bash
uv sync
```

### External dependency

`audio_only` mode requires **ffmpeg** on your PATH. Video merging to mp4 also uses ffmpeg. Install via your package manager (`winget install Gyan.FFmpeg`, `brew install ffmpeg`, `apt install ffmpeg`, etc.).

## Usage

### Video Downloader (yt-dlp)

Category: `video/download`.

#### Inputs

| Input | Type | Notes |
|---|---|---|
| `url` | STRING | The video URL |
| `mode` | `video` \| `audio_only` | Pick output kind |
| `output_dir` | STRING | Defaults to `ComfyUI/output/downloads` |
| `filename_template` | STRING | yt-dlp template, default `%(title)s.%(ext)s` |
| `audio_format` | dropdown | Only used when `mode=audio_only` |
| `format_override` | STRING | Raw yt-dlp `-f` string; overrides mode default when set |
| `cookies_file` | STRING | Path to a `cookies.txt` (Netscape format) |

#### Outputs

- `file_path` (STRING) — absolute path to the downloaded file
- `title` (STRING)
- `duration` (FLOAT) — seconds

### Load Audio (from path)

Category: `audio`. Reads an audio file at a given path and returns ComfyUI's standard `AUDIO` type — a dict of `{"waveform": Tensor[1, channels, time], "sample_rate": int}`. Sample rate is preserved as-is; no resampling.

- **Input**: `audio_path` (STRING)
- **Output**: `AUDIO`

Uses `torchaudio.load()` under the hood, which comes with any standard ComfyUI environment.

### String → AudioPath

Category: `audio/utils`. Passes a STRING through unchanged but retypes it as `AUDIOPATH`, which is what some audio packs (notably UVR5 forks) declare on their inputs. ComfyUI's type matching is strict/nominal, so without this step a plain STRING won't wire.

- **Input**: `path` (STRING)
- **Output**: `AUDIOPATH`

### Typical wiring

```
Video Downloader (mode=video)       ──►  VHS_LoadVideo ──► IMAGE + AUDIO
Video Downloader (mode=audio_only)  ──►  Load Audio (from path) ──► AUDIO
Video Downloader (mode=audio_only)  ──►  String → AudioPath    ──► UVR5
```

## Using Premium / authenticated downloads

Export your browser cookies to a Netscape-format `cookies.txt`:

1. Install a cookie exporter extension (e.g. "Get cookies.txt LOCALLY" for Chrome/Firefox).
2. While logged in to the target site, export cookies for that domain.
3. Save the file somewhere ComfyUI can read (e.g. `ComfyUI/user/cookies.txt`).
4. Set the node's `cookies_file` input to that absolute path.

**Security note**: the cookie file grants session access to your account. Keep it out of shared folders and out of version control.

## Caching behavior

ComfyUI caches node outputs by input hash. Same URL + same options = no re-download on repeated queue runs. Change the URL or delete the file manually to force a fresh download.
