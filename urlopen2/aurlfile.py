import asyncio
from io import IOBase
from tempfile import mkstemp
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from aiofiles.threadpool.binary import AsyncBufferedReader
# > Typing
from typing import Optional, TypeVar, Tuple
# > Local Import's
from .types import URLOpenRet

# ! Type Alias
T = TypeVar("T")

# ! Vars
pool = ThreadPoolExecutor()

# ! Main Class
class AsyncURLFile(IOBase):
    def __init__(
        self,
        url: str,
        buffer: AsyncBufferedReader,
        **kwargs
    ) -> None:
        self._name = url
        self._buffer = buffer
        self._furl: URLOpenRet = urlopen(self._name, **kwargs)
        self._full: bool = False
    
    @staticmethod
    def open(
        url: str,
        buffer: AsyncBufferedReader
    ):
        return AsyncURLFile(url, buffer)
    
    @staticmethod
    def gbuf() -> Tuple[str, str]:
        return mkstemp(".bin")[1], "wb+"
    
    @property
    def length(self) -> Optional[int]: return self._furl.length
    @property
    def downloaded(self) -> int: return pool.submit(asyncio.run, self._getsize()).result()
    @property
    def name(self) -> str: return self._name
    @property
    def mode(self) -> str: return "rb"
    @property
    def closed(self) -> bool: return self._buffer.closed
    @property
    def full(self) -> bool: return self._full
    
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc_val, exc_tb): await self.close()
    
    def readable(self) -> bool: return True
    def seekable(self) -> bool: return True
    def writable(self) -> bool: return False

    async def tell(self) -> int:
        return await self._buffer.tell()
    
    async def close(self) -> None:
        await self._buffer.close()
        if not self._furl.closed:
            self._furl.close()
    
    async def _getsize(self) -> int:
        ct = await self.tell()
        size = await self._buffer.seek(0, 2)
        await self._buffer.seek(ct)
        return size
    
    async def _topload(self, size: int) -> None:
        if not self._full:
            ct = await self.tell()
            data = self._furl.read(size)
            if len(data) != size:
                self._full = True
                self._furl.close()
            await self._buffer.seek(0, 2)
            await self._buffer.write(data)
            await self._buffer.seek(ct)
    
    async def _fullload(self) -> None:
        if not self._full:
            ct = await self.tell()
            await self._buffer.seek(0, 2)
            while len(data:=self._furl.read(65536)) > 0:
                await self._buffer.write(data)
            self._furl.close()
            self._full = True
            await self._buffer.seek(ct)
    
    async def fulling(self) -> None:
        await self._fullload()
    
    async def read(self, n: Optional[int]=-1) -> bytes:
        n = n or -1
        if not self._full:
            if n > 0:
                s = n - (await self._getsize() - await self.tell())
                if s > 0:
                    await self._topload(s)
            elif n < 0:
                await self._fullload()
        return await self._buffer.read(n)
    
    async def seek(self, offset: int, whence: int=0) -> int:
        if (offset > 0) and (not self._full):
            if whence == 0:
                s = await self._getsize() - offset
                if s > 0:
                    await self._topload(s)
            elif whence == 1:
                s = offset - (await self._getsize() - await self.tell())
                if s > 0:
                    await self._topload(s)
            elif whence == 2:
                if (self.length is not None) and (self.length != 0):
                    s = self.length - await self._getsize() - offset
                    if s > 0:
                        await self._topload(s)
                    else:
                        await self._fullload()
                else:
                    await self._fullload()
        return await self._buffer.seek(offset, whence)
