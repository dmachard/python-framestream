
import fstrm
import unittest
import asyncio

class FstrmServerProtocol(asyncio.Protocol):
    def __init__(self, hanshake_server, data_recv):
        self.fstrm = fstrm.FstrmCodec()
        self.data_recv = data_recv
        self.hanshake_server = hanshake_server
        self.handshake_accept_done = False

    def connection_made(self, transport):
        print('Server - Connection from {}'.format(transport.get_extra_info('peername')))
        self.transport = transport

    def data_received(self, data):
        if not self.hanshake_server.done():
            if not self.handshake_accept_done:
                if self.fstrm.is_ctrlready(data):
                    print('Server - handshake CONTROL_READY received!')
                    self.transport.write(self.fstrm.encode_ctrlaccept(b"plaintext"))
                    print('Server - handshake CONTROL_ACCEPT sent')
                    self.handshake_accept_done = True
            else:
                if self.fstrm.is_ctrlstart(data): 
                    print('Server - handshake CONTROL_START received!')
                    self.hanshake_server.set_result(True)
                    print('Server - handshake success!')
        else:
            payload = self.fstrm.is_data(data)
            if payload:
                self.data_recv.set_result(payload)
                print('Server - Data received!')

class FstrmClientProtocol(asyncio.Protocol):
    def __init__(self, handshake):
        self.fstrm = fstrm.FstrmCodec()
        self.handshake = handshake
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(self.fstrm.encode_ctrlready(b"plaintext"))
        print('Client - send handshake CONTROL_READY')

    def data_received(self, data):
        if not self.handshake.done():
            if self.fstrm.is_ctrlaccept(data):
                print('Client - handshake CONTROL_ACCEPT received!')
                self.transport.write(self.fstrm.encode_ctrlstart())
                print('Client - handshake CONTROL_START sent')
                self.handshake.set_result(True)
                print('Client - handshake success!')

    def send_data(self, data):
        payload = self.fstrm.encode_data(data)
        self.transport.write(payload)
        print('Client - Data sent!')

class TestClientServer(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test1_handshake(self):
        """do handshake"""
        async def run():
            # Create server and client
            data_recv = self.loop.create_future()
            hanshake_server = self.loop.create_future()
            server = await self.loop.create_server(lambda: FstrmServerProtocol(hanshake_server, data_recv), 'localhost', 8000)

            hanshake_client = self.loop.create_future()
            transport, protocol =  await self.loop.create_connection(lambda: FstrmClientProtocol(hanshake_client), 'localhost', 8000)

            # check handshake
            try:
                await asyncio.wait_for(hanshake_server, timeout=0.5)
            except asyncio.TimeoutError:
                self.fail("handshake server failed")

            try:
                await asyncio.wait_for(hanshake_client, timeout=0.5)
            except asyncio.TimeoutError:
                self.fail("handshake client failed")

            # Shut down server and client
            server.close()
            transport.close()

        self.loop.run_until_complete(run())

    def test2_client_send_data(self):
        """client sent data"""
        async def run():
            # Create server and client
            data_recv = self.loop.create_future()
            hanshake_server = self.loop.create_future()
            server = await self.loop.create_server(lambda: FstrmServerProtocol(hanshake_server, data_recv), 'localhost', 8000)

            hanshake_client = self.loop.create_future()
            transport, client =  await self.loop.create_connection(lambda: FstrmClientProtocol(hanshake_client), 'localhost', 8000)

            # check handshake
            data = b"some data"
            try:
                await asyncio.wait_for(hanshake_server, timeout=0.5)
            except asyncio.TimeoutError:
                self.fail("handshake server failed")

            try:
                await asyncio.wait_for(hanshake_client, timeout=0.5)
            except asyncio.TimeoutError:
                self.fail("handshake client failed")
            
            # send data from client
            client.send_data(data)

            # wait data on server side
            try:
                await asyncio.wait_for( data_recv, timeout=0.5)
                self.assertEqual(data_recv.result(), data)
            except asyncio.TimeoutError:
                self.fail("data failed")

            # Shut down server and client
            server.close()
            transport.close()

        self.loop.run_until_complete(run())