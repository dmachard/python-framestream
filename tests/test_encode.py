import fstrm
import unittest

class TestEncode(unittest.TestCase):
    def test_encode_ready(self):
        """encode ready control"""   
        f = fstrm.FstrmCodec()
        ctrl = f.encode(ctrl=fstrm.FSTRM_CONTROL_READY, ct=[b"protobuf:dnstap.Dnstap"])
        self.assertEqual( len(ctrl), 42 )
     
    def test_encode_accept(self):
        """encode accept control"""   
        f = fstrm.FstrmCodec()
        ctrl = f.encode(ctrl=fstrm.FSTRM_CONTROL_ACCEPT, ct=[b"protobuf:dnstap.Dnstap"])
        self.assertEqual( len(ctrl), 42 )
       
    def test_encode_finish(self):
        """encode finish control"""   
        f = fstrm.FstrmCodec()
        ctrl = f.encode(ctrl=fstrm.FSTRM_CONTROL_FINISH)
        self.assertEqual( len(ctrl), 12 )
        
    def test_encode_start(self):
        """encode start control"""   
        f = fstrm.FstrmCodec()
        ctrl = f.encode(ctrl=fstrm.FSTRM_CONTROL_START)
        self.assertEqual( len(ctrl), 12 )
        
    def test_encode_stop(self):
        """encode stop control"""   
        f = fstrm.FstrmCodec()
        ctrl = f.encode(ctrl=fstrm.FSTRM_CONTROL_STOP)
        self.assertEqual( len(ctrl), 12 )
       
    def test_encode_dataframe(self):
        """encode data frame"""   
        f = fstrm.FstrmCodec()
        data = f.encode(ctrl=fstrm.FSTRM_DATA_FRAME, payload=b"hello")
        self.assertEqual( len(data), 9 )