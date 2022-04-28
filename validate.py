import binascii
from web3.auto import w3
json_keyfile = w3.eth.account.privateKeyToAccount(binascii.unhexlify('c1348ffd4dabba89c93c9d3c81322ea01187d40b0d75fceff0e8481edb31b04d')).encrypt(b"any password")
print(json_keyfile)

a = {'address': '9823ed7519e6efad84da9965b8267501564d638c',
     'crypto': {'cipher': 'aes-128-ctr', 'cipherparams': {'iv': '96720a9f39765f9c854a8311eb6df20e'},
                'ciphertext': 'b3a16c4a9a6e4cdf09ae75390217f05128251f007f7ca95981a18636240baf5c', 'kdf': 'scrypt',
                'kdfparams': {'dklen': 32, 'n': 262144, 'r': 1, 'p': 8, 'salt': '3b4bd8279abd4d46dce8a2a32f7377e4'},
                'mac': '6fb1a72e8775bcc19e39f9484c25f7a93fde0fe578052190593dc71f97925c42'},
     'id': '78fa8415-013b-448d-90e8-2324576f9cc2', 'version': 3}
