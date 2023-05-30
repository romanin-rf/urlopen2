from urllib.request import urlopen
from io import BytesIO, BufferedRandom, RawIOBase
# > Typing
from typing import Optional, Union

# ! Main
class URLFile(RawIOBase):
    def __init__(
        self,
        url: str,
        *,
        buffer: Optional[Union[BytesIO, BufferedRandom]]=None,
        **kwargs
    ) -> None:
        self._name = url
        self._buffer = buffer or BytesIO()
        self._furl = urlopen(self._name, **kwargs)
        self._full: bool = False
    
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
    
    def read(self, n: int=-1) -> bytes:
        if n is None:
            n = -1
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
                self._fullload()
        return self._buffer.seek(offset, whence)
