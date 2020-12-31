# Frame Streams implementation in Python

![Testing](https://github.com/dmachard/python-framestream/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/python-framestream/workflows/Build/badge.svg) ![Pypi](https://github.com/dmachard/python-framestream/workflows/PyPI/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fstrm)

Frame Streams is a lightweight, binary-clean protocol that allows for the transport of arbitrarily encoded data payload sequences with minimal framing overhead.

This package provides a pure Python implementation based on https://github.com/farsightsec/fstrm/.

## Installation

This module can be installed from [pypi](https://pypi.org/project/fstrm/) website

```python
pip install fstrm
```

## Example

The example shows how to read raw data and decode-it with the fstrsm library.

```python
import fstrm
import asyncio

async def on_connect():
    f = fstrm.FstrmCodec()

    while data := await reader.read(f.pending_nb_bytes()) 
        f.append(data=data)
        
        if fstrm_handler.process():
            ctrl, ct, payload  = fstrm_handler.decode()
            
            if ctrl == fstrm.FSTRM_DATA_FRAME:
                do_something(data=payload)
                
            if ctrl == fstrm.FSTRM_CONTROL_READY:
                accept = f.encode(ctrl=fstrm.FSTRM_CONTROL_ACCEPT, ct=[b"protobuf:dnstap.Dnstap"])
                writer.write(accept)
                await writer.drain()
                    
            if ctrl == fstrm.FSTRM_CONTROL_START:
                pass
                
            if ctrl == fstrm.FSTRM_CONTROL_STOP:
                f.reset()  

loop = asyncio.get_event_loop()                
coro = asyncio.start_server(on_connect, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)
loop.close()
```
