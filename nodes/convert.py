from __future__ import annotations


class StringToAudioPath:
    """Retype a STRING (file path) as AUDIOPATH.

    ComfyUI's type system is nominal — slots only connect when type names
    match exactly. Some audio packs (e.g. UVR5 forks) declare an AUDIOPATH
    input that's semantically a path but won't accept plain STRING. This
    node passes the value through unchanged while switching the declared
    return type so the wire connects.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("AUDIOPATH",)
    RETURN_NAMES = ("audio_path",)
    FUNCTION = "convert"
    CATEGORY = "audio/utils"

    def convert(self, path: str):
        return (path,)
