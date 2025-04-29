from collections.abc import Generator
import json
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
import requests

DEFAULT_BASE_URL = "https://developer.voicemaker.in/voice/api"


class VoicemakerTool(Tool):
    def _parse_response(self, response: dict) -> dict:
        result = {}
        if response.get("success"):
            result["audio_url"] = response.get("path", "")
            result["used_chars"] = response.get("usedChars", 0)
            result["remain_chars"] = response.get("remainChars", 0)
            result["remain_key_chars"] = response.get("remainKeyChars", 0)
        return result

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:

        api_key = self.runtime.credentials["serpapi_api_key"]
        base_url = self.runtime.credentials["base_url"] if self.runtime.credentials["base_url"] else DEFAULT_BASE_URL
        headers = {
            "Authorization": "Bearer "+api_key,
            "Content-Type": "application/json"
        }

        json_data = {
            "Engine": tool_parameters["engine"],
            "VoiceId": tool_parameters["voiceId"],
            "LanguageCode": tool_parameters["languageCode"],
            "Text": tool_parameters["text"],
            "OutputFormat": tool_parameters["outputFormat"],
            "SampleRate": tool_parameters["sampleRate"],
            "Effect": tool_parameters["effect"],
            "MasterVolume": tool_parameters["masterVolume"],
            "MasterSpeed": tool_parameters["masterSpeed"],
            "MasterPitch": tool_parameters["masterPitch"],
        }
        response = requests.post(
            url=base_url, headers=headers, data=json.dumps(json_data), timeout=5)
        response.raise_for_status()
        valuable_res = self._parse_response(response.json())

        yield self.create_json_message(valuable_res)
