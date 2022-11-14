import base64
import struct
import hashlib
import time

def GoogleAuthenticatorCode(secret):
	key = base64.b32decode(secret)
	msg = struct.pack(">Q", int(time.time()) // 30)
	h = hashlib.new("sha1", key + msg).digest()
	o = h[19] & 15
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
	return str(h).zfill(6)

print ("Début du programme")
secret = "FBSWY3DPEHPK3PXP"
print ("Secret : " + secret)
code = GoogleAuthenticatorCode(secret)
print ("Code : " + code)