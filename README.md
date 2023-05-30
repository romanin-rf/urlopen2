# urlopen2
## Description
Improvement for the `urllib.request.urlopen` function.

## Install
```shell
pip install urlopen2
```

## Using
```python
from urlopen2 import URLFile

url = "https://example.com/file.bin"

with URLFile(url) as f:
    f.read(128)
    # In this case, 128 bytes of the file will be loaded.
    f.seek(0)
    # Move the caret to the beginning of the file
    data = f.read(128) 
    # Since we are taking the same 128 bytes that have already been loaded, they will be received from the buffer.

print(data)
```