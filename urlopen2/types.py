from typing import Optional

# ! URLOpenRet Type Alias
class URLOpenRet:
    url: str
    code: int
    status: int
    closed: bool
    chunked: bool
    will_close: bool
    length: Optional[int]

    def read(self, n: int=-1) -> bytes: ...
    def read1(self, n: int=-1) -> bytes: ...
    def readinto(self, b) -> int: ...
    def readinto1(self, b) -> int: ...

    def isclosed(self) -> bool: ...
    def close(self) -> None: ...