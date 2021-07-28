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

class FstrmServerProtocol(asyncio.Protocol):
    def __init__(self, handshake, content_type=b"plaintext"):
        self.fstrm = fstrm.FstrmCodec()
        self.content_type = content_type
        self.data_recv = data_recv
        self.handshake = handshake
        self.handshake_accept_done = False

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if not self.handshake.done():
            if not self.handshake_accept_done:
                if self.fstrm.is_ctrlready(data):
                    self.transport.write(self.fstrm.encode_ctrlaccept(self.content_type)
                    self.handshake_accept_done = True
            else:
                if self.fstrm.is_ctrlstart(data):
                    self.handshake.set_result(True)
        else:
            payload = self.fstrm.is_data(data)
            # do someting with the payload...

class FstrmClientProtocol(asyncio.Protocol):
    def __init__(self, handshake, content_type=b"plaintext"):
        self.fstrm = fstrm.FstrmCodec()
        self.content_type = content_type
        self.handshake = handshake
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(self.fstrm.encode_ctrlready(self.content_type)

    def data_received(self, data):
        if not self.handshake.done():
            if self.fstrm.is_ctrlaccept(data):
                self.transport.write(self.fstrm.encode_ctrlstart(self.content_type))
                self.handshake.set_result(True)

    def send_data(self, data):
        payload = self.fstrm.encode_data(data)
        self.transport.write(payload)

async def run(loop):
    # Create server and client
    hanshake_server = loop.create_future()
    server = await loop.create_server(lambda: FstrmServerProtocol(hanshake_server), 'localhost', 8000)

    hanshake_client = loop.create_future()
    transport, client =  await loop.create_connection(lambda: FstrmClientProtocol(hanshake_client), 'localhost', 8000)

    # check handshake
    try:
        await asyncio.wait_for(hanshake_client, timeout=0.5)
    except asyncio.TimeoutError:
       raise Exception("handshake client failed")

    # ok, the client send some data
    data = b"some data..."
    client.send_data(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
```
