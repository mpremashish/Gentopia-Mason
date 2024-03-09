from typing import AnyStr
from gentopia.tools.basetool import *
from youtube_transcript_api import YouTubeTranscriptApi
import re


class YoutubeTranscriptArgs(BaseModel):
    query: str = Field(..., description="video id")


class YoutubeTranscript(BaseTool):
    """Tool that adds the capability to query the youtube search API."""

    name = "youtube_transcript"
    description = ("youtube search for getting the transcripts."
                   "Input should be a video Id.")

    args_schema: Optional[Type[BaseModel]] = YoutubeTranscriptArgs

    def _run(self, query: AnyStr) -> str:
        transcript_list = YouTubeTranscriptApi.list_transcripts(query)
        key_list = []

        for key, value in transcript_list._manually_created_transcripts.items():
            key_list.append(key)

        if not key_list:
            for key, value in transcript_list._generated_transcripts.items():
                key_list.append(key)

        transcript = YouTubeTranscriptApi.get_transcript(
            query, key_list)

        return " ".join(transcript[i]['text'] for i in range(len(transcript)))

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = YoutubeTranscript()._run("I9-HzAKza50")
    print(ans)
