# urlopen2
## Description
Improvement for the `urllib.request.urlopen` function.

## Install
```shell
pip install urlopen2
```

## Using
### Synchronous
```python
from urlopen2 import URLFile

url = "https://example.com/file.bin"

with URLFile.open(url) as urlfile:
    urlfile.read(128)
    # In this case, 128 bytes of the file will be loaded.
    urlfile.seek(0)
    # Move the caret to the beginning of the file
    data = urlfile.read(128)
    # Since we are taking the same 128 bytes that have already been loaded, they will be received from the buffer.

print(data)
```

### Asynchronous
```python
import asyncio
import aiofiles
from urlopen2 import AsyncURLFile

url = "https://example.com/file.bin"

async def main():
    async with aiofiles.open(*AsyncURLFile.gbuf()) as abuffer:
        async with AsyncURLFile.open(url, abuffer) as aurlfile:
            await aurlfile.read(128)
            # In this case, 128 bytes of the file will be loaded.
            await aurlfile.seek(0)
            # Move the caret to the beginning of the file
            data = await aurlfile.read(128)
            # Since we are taking the same 128 bytes that have already been loaded, they will be received from the buffer.
    
    print(data)

if __name__ == "__main__":
    asyncio.run(main())
```