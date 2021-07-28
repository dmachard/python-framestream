import fstrm
import unittest

class TestCodec(unittest.TestCase):
    def test_control_ready(self):
        """decode control ready"""   
        f = fstrm.FstrmCodec()
        
        data_bin = f.encode(ctrl=fstrm.FSTRM_CONTROL_READY, ct=[b"protobuf:dnstap.Dnstap"])
        f.append(data=data_bin)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_CONTROL_READY )
        
    def test_control_accept(self):
        """decode control accept"""   
        f = fstrm.FstrmCodec()
        
        data_bin = f.encode(ctrl=fstrm.FSTRM_CONTROL_ACCEPT, ct=[b"protobuf:dnstap.Dnstap"])
        f.append(data=data_bin)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_CONTROL_ACCEPT )
        
    def test_control_finish(self):
        """decode control finish"""   
        f = fstrm.FstrmCodec()
        
        data_bin = f.encode(ctrl=fstrm.FSTRM_CONTROL_FINISH)
        f.append(data=data_bin)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_CONTROL_FINISH )

    def test_decode_control_start(self):
        """decode control start"""   
        f = fstrm.FstrmCodec()
        
        data_bin = f.encode(ctrl=fstrm.FSTRM_CONTROL_START)
        f.append(data=data_bin)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_CONTROL_START )
        
    def test_decode_control_stop(self):
        """decode control stop"""   
        f = fstrm.FstrmCodec()
        
        data_bin = f.encode(ctrl=fstrm.FSTRM_CONTROL_STOP)
        f.append(data=data_bin)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_CONTROL_STOP )

    def test_decode_data_frame(self):
        """decode data frame"""   
        f = fstrm.FstrmCodec()
        
        data_frame = f.encode(ctrl=fstrm.FSTRM_DATA_FRAME, payload=b"hello")
        f.append(data=data_frame)
        
        ft = -1
        if f.process():
            ft, ct, payload  = f.decode()
        self.assertEqual( ft, fstrm.FSTRM_DATA_FRAME )