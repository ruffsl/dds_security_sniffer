import pyshark

def extract(rtps):
    lfs = rtps.get('rtps.property_name').fields
    idx = -1
    for i, lf in enumerate(lfs):
        if lf.show == 'c.perm':
            idx = i
            break
    udBin = rtps.get('rtps.param.userData').fields[idx].show
    ud = bytes.fromhex(''.join(udBin.split(':'))).decode('utf-8')
    
    #TODO: Extract xml data from userdata and generate a xml permission file with 256 hash of corresponding subject_name.

if __name__ == '__main__':
    cap = pyshark.FileCapture('tshark-recording.pcapng', display_filter='rtps.property_name == "c.perm"')

    for pac in cap:
        extract(pac.rtps)
