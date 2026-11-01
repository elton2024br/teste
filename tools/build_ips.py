"""Create an IPS patch and verify that applying it reconstructs the target."""
from pathlib import Path
import sys,hashlib

def create(source,target):
    if len(source)!=len(target) or len(target)>0x1000000:
        raise ValueError('This tool requires equal sizes up to 16 MiB.')
    patch=bytearray(b'PATCH'); pos=0
    while pos<len(target):
        if source[pos]==target[pos]:pos+=1;continue
        start=pos
        if start==0x454f46:start-=1
        pos+=1
        while pos<len(target) and pos-start<65535 and source[pos]!=target[pos]:pos+=1
        payload=target[start:pos]
        patch+=start.to_bytes(3,'big')+len(payload).to_bytes(2,'big')+payload
    patch+=b'EOF'
    rebuilt=bytearray(source);cursor=5
    while patch[cursor:cursor+3]!=b'EOF':
        offset=int.from_bytes(patch[cursor:cursor+3],'big');size=int.from_bytes(patch[cursor+3:cursor+5],'big');cursor+=5
        assert size>0
        rebuilt[offset:offset+size]=patch[cursor:cursor+size];cursor+=size
    assert rebuilt==target,'Patch verification failed'
    return patch

if __name__=='__main__':
    source,target,out=map(Path,sys.argv[1:])
    result=create(source.read_bytes(),target.read_bytes());out.write_bytes(result)
    print(f'Patch verified: {len(result)} bytes; target SHA-1 {hashlib.sha1(target.read_bytes()).hexdigest()}')
