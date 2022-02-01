import base64
from getpass import getpass

key = getpass("Please Enter Key: ")
# print(key)

codedKey = key.encode('utf-8')
base64Bytes = base64.b64encode(codedKey)
print(base64Bytes.decode("utf-8"))
