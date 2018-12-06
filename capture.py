import pyshark
import xml.etree.ElementTree as ET
import hashlib
import sys
import os
from M2Crypto import SMIME, BIO
from subprocess import call

class Capture:
    """
    path:           path to store perm xml
    intf:           interface to listen
    constructFn:    shell script that invoke construct process
    """
    def __init__(self, path, intf, constructFn):
        self.path = path
        self.knownPerms = set()
        self.intf = intf
        self.constructFn = constructFn

    """
    pkt: pyshark packet, assume pkt is ip<udp<rtps handshake pkt
    return filename: ip addr + hash
           xml:      perm xml string
    """
    def getPermFromPkt(self, pkt):
        ip = pkt.ip.src
        rtps = pkt.rtps
        if rtps == None:
            return ("", "")

        lfs = rtps.get('rtps.property_name').fields
        idx = -1
        for i, lf in enumerate(lfs):
            if lf.show == 'c.perm':
                idx = i
                break

        if idx == -1:
            return ("", "")

        ud = bytes.fromhex(rtps.get('rtps.param.userData').fields[idx].show.replace(':', ''))
        bio = BIO.MemoryBuffer(ud)
        p7, data = SMIME.smime_load_pkcs7_bio(bio)
        xml_str = data.read().decode('utf-8').split('\n',2)[2]
        filename = ip + "_" + hashlib.sha256(ud).hexdigest()[:8]
        return (filename, xml_str)

    """
    hook given to pyshark
    """
    def processFn(self, pkt):
        filename, xml_str = getPermFromPkt(pkt)
        if (not filename) or (filename in self.knownPerms):
            return

        self.knownPerms.add(filename)
        filename = os.path.join(self.path, ip + "_" + hashlib.sha256(ud).hexdigest()[:8])
        with open(filename+'.xml', 'w') as f:
            f.write(xml_str)

        call(self.constructFn)

    """
    start capture
    """
    def startCap():
        cap = pyshark.LiveCapture(interface=self.intf, bpf_filter="ip and udp and rtps and dst port 7410", display_filter='rtps.property_name == "c.perm"')
        cap.sniff(timeout=50)
        cap.apply_on_packets(self.processFn)

if __name__ == '__main__':
    cap = Capture(sys.argv[1], sys.argv[2], sys.argv[3:])
    cap.startCap()



