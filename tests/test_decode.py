import fstrm
import unittest

class TestDecode(unittest.TestCase):
    def test_decode_control_ready(self):
        """decode control ready"""   
        f = fstrm.FstrmCodec()
        
        data = b'\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x16protobuf:dnstap.Dnstap'
        f.append(data=data)
        ctrl, ct, payload  = f.decode()
        self.assertEqual( len(ctrl), fstrm.FSTRM_CONTROL_READY )
        
    def test_decode_control_start(self):
        """decode control start"""   
        f = fstrm.FstrmCodec()
        
        data = b'\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16protobuf:dnstap.Dnstap'
        f.append(data=data)
        ctrl, ct, payload  = f.decode()
        self.assertEqual( len(ctrl), fstrm.FSTRM_CONTROL_START )
        
    def test_decode_data_frame(self):
        """decode data frame"""   
        f = fstrm.FstrmCodec()
        
        data = b'\n\x08dnsdist1\x12\rdnsdist 1.5.0ru\x08\x05\x10\x02\x18\x01"\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01*\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x010\xc6\xac\x0385@\x9c\xbd\xb6\xff\x05M\xcb\xabL\x06R8~8\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x03www\x07netflix\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08a\xb7\xeb\x88\xc1|M\xf3x\x01'
        f.append(data=data)
        ctrl, ct, payload  = f.decode()
        self.assertEqual( len(ctrl), fstrm.FSTRM_DATA_FRAME )