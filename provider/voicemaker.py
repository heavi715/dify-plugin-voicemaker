from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.voicemaker import VoicemakerTool


class VoicemakerProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            for _ in VoicemakerTool.from_credentials(credentials).invoke(
                tool_parameters={"Engine": "neural", "VoiceId": "ai3-Jony", "LanguageCode": "en-US", "Text": "Welcome to the Air.",
                                 "OutputFormat": "mp3", "SampleRate": "48000", "Effect": "default", "MasterVolume": "0", "MasterSpeed": "0", "MasterPitch": "0"},
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
