from typing import AnyStr
from gentopia.tools.basetool import *
import urllib.request
import PyPDF2
import io


class PdfReaderArgs(BaseModel):
    query: str = Field(..., description="a link to the paper")


class PdfReader(BaseTool):
    """Tool that adds the capability to query the Google search API."""

    name = "pdf_reader"
    description = ("A pdf reader reading the pdf."
                   "Input should be a pdf link.")

    args_schema: Optional[Type[BaseModel]] = PdfReaderArgs

    def _run(self, query: AnyStr) -> str:
        req = urllib.request.Request(
            query, headers={'User-Agent': "Magic Browser"})
        remote_file = urllib.request.urlopen(req).read()
        remote_file_bytes = io.BytesIO(remote_file)
        pdfdoc_remote = PyPDF2.PdfReader(remote_file_bytes)
        return "\n\n".join(pdfdoc_remote.pages[i].extract_text() for i in range(len(pdfdoc_remote.pages)))

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PdfReader()._run("https://arxiv.org/pdf/2308.04030.pdf")
    print(ans)
