"""comfyui-karaoke — ComfyUI node pack for karaoke pipeline construction.

Current scope: source fetching (yt-dlp) and stem separation (audio-separator).
Future stages (pitch shift, lyric transcription/sync, video render) are
planned but not implemented here yet.
"""

import os

from .nodes.convert import StringToAudioPath
from .nodes.downloader import VideoDownloader
from .nodes.load_audio import LoadAudioFromPath
from .nodes.separation import AudioSeparator


def _register_audio_separator_folder() -> None:
    """Register ComfyUI/models/audio_separator so audio-separator caches there.

    Silently no-ops outside a ComfyUI environment — the node falls back to
    ~/.audio-separator/models/ in that case.
    """
    try:
        import folder_paths

        models_root = folder_paths.models_dir
        target = os.path.join(models_root, "audio_separator")
        os.makedirs(target, exist_ok=True)
        folder_paths.add_model_folder_path("audio_separator", target)
    except Exception:
        pass


_register_audio_separator_folder()


NODE_CLASS_MAPPINGS = {
    "VideoDownloader": VideoDownloader,
    "LoadAudioFromPath": LoadAudioFromPath,
    "StringToAudioPath": StringToAudioPath,
    "AudioSeparator": AudioSeparator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoDownloader": "Video Downloader (yt-dlp)",
    "LoadAudioFromPath": "Load Audio (from path)",
    "StringToAudioPath": "String → AudioPath",
    "AudioSeparator": "Audio Separator",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
