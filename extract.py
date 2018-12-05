import pyshark
import xml.etree.ElementTree as ET
import hashlib
import sys
from M2Crypto import SMIME, BIO

def extract(ip, rtps):
    lfs = rtps.get('rtps.property_name').fields
    idx = -1
    for i, lf in enumerate(lfs):
        if lf.show == 'c.perm':
            idx = i
            break
    ud = bytes.fromhex(rtps.get('rtps.param.userData').fields[idx].show.replace(':', ''))
    bio = BIO.MemoryBuffer(ud)
    p7, data = SMIME.smime_load_pkcs7_bio(bio)
    xml_str = data.read().decode('utf-8').split('\n',2)[2]
    filename = ip + "_" + hashlib.sha256(ud).hexdigest()[:20]
    with open(filename+'.xml', 'w') as f:
        f.write(xml_str)

if __name__ == '__main__':
    cap = pyshark.FileCapture(sys.argv[1], display_filter='rtps.property_name == "c.perm"')

    for pac in cap:
        ip = pac.ip.src
        extract(ip, pac.rtps)
