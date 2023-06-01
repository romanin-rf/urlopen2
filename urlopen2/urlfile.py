from tempfile import mkstemp
from urllib.request import urlopen
from io import BytesIO, BufferedRandom, IOBase
# > Typing
from typing import Optional, Union
# > Local Imports
from .types import URLOpenRet

# ! Main Class
class URLFile(IOBase):
    def __init__(
        self,
        url: str,
        *,
        buffer: Optional[Union[BytesIO, BufferedRandom]]=None,
        **kwargs
    ) -> None:
        self._name = url
        self._buffer = buffer or open(mkstemp(".bin")[1], "wb+")
        self._furl: URLOpenRet = urlopen(self._name, **kwargs)
        self._full: bool = False
    
    @property
    def length(self) -> Optional[int]: return self._furl.length
    @property
    def downloaded(self) -> int: return self._getsize()
    @property
    def name(self) -> str: return self._name
    @property
    def mode(self) -> str: return "rb"
    @property
    def closed(self) -> bool: return self._buffer.closed
    @property
    def full(self) -> bool: return self._full
    
    def readable(self) -> bool: return True
    def seekable(self) -> bool: return True
    def writable(self) -> bool: return False
    def tell(self) -> int: return self._buffer.tell()
    
    def close(self) -> None:
        self._buffer.close()
        self._furl.close()
    
    def _getsize(self) -> int:
        ct = self.tell()
        size = self._buffer.seek(0, 2)
        self._buffer.seek(ct)
        return size

    def _topload(self, size: int) -> None:
        if not self._full:
            ct = self.tell()
            data = self._furl.read(size)
            if len(data) != size:
                self._full = True
                self._furl.close()
            self._buffer.seek(0, 2)
            self._buffer.write(data)
            self._buffer.seek(ct)
    
    def _fullload(self) -> None:
        if not self._full:
            ct = self.tell()
            self._buffer.seek(0, 2)
            while len(data:=self._furl.read(65536)) > 0:
                self._buffer.write(data)
            self._furl.close()
            self._full = True
            self._buffer.seek(ct)
    
    def fulling(self) -> None: self._fullload()
    
    def read(self, n: Optional[int]=-1) -> bytes:
        n = n or -1
        if not self._full:
            if n > 0:
                s = n - (self._getsize() - self.tell())
                if s > 0:
                    self._topload(s)
            elif n < 0:
                self._fullload()
        return self._buffer.read(n)
    
    def seek(self, offset: int, whence: int=0) -> int:
        if (offset > 0) and (not self._full):
            if whence == 0:
                s = self._getsize() - offset
                if s > 0:
                    self._topload(s)
            elif whence == 1:
                s = offset - (self._getsize() - self.tell())
                if s > 0:
                    self._topload(s)
            elif whence == 2:
                if (self.length is not None) and (self.length != 0):
                    s = self.length - self._getsize() - offset
                    if s > 0:
                        self._topload(s)
                    else:
                        self._fullload()
                else:
                    self._fullload()
        return self._buffer.seek(offset, whence)
