from io import IOBase
from aiofiles.threadpool.binary import AsyncBufferedReader
# > Typing
from typing import Optional, Tuple, Literal

# ! Main Class
class AsyncURLFile(IOBase):
    async def __init__(
        self,
        url: str,
        buffer: AsyncBufferedReader,
        **kwargs
    ) -> None: ...
    
    @staticmethod
    def open(
        url: str,
        buffer: AsyncBufferedReader
    ) -> AsyncURLFile: ...

    @staticmethod
    def gbuf() -> Tuple[str, Literal['wb+']]: ...
    
    @property
    def length(self) -> Optional[int]: ...
    @property
    def downloaded(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def mode(self) -> str: ...
    @property
    def closed(self) -> bool: ...
    @property
    def full(self) -> bool: ...
    
    async def __aenter__(self) -> AsyncURLFile: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    
    def readable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def writable(self) -> bool: ...
    
    async def fulling(self) -> None:
        """Full topload of the file to the buffer."""
        ...
    
    async def tell(self) -> int: ...
    async def read(self, n: Optional[int]=...) -> bytes: ...
    async def seek(self, offset: int, whence: int=...) -> int: ...
    
    async def close(self) -> None: ...
