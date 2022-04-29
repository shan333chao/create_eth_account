import binascii, hashlib, hmac, struct
import json
import datetime

from ecdsa.curves import SECP256k1
from eth_utils import to_checksum_address, keccak as eth_utils_keccak
from mnemonic import Mnemonic

BIP39_PBKDF2_ROUNDS = 2048
BIP39_SALT_MODIFIER = "mnemonic"
BIP32_PRIVDEV = 0x80000000
BIP32_CURVE = SECP256k1
BIP32_SEED_MODIFIER = b'Bitcoin seed'
ETH_DERIVATION_PATH = "m/44'/60'/0'/0"

MNEMONIC_LENGTH_MAP = {12: 128, 15: 160, 18: 192, 21: 224, 24: 256}
# 设置助记词长度
mnemonic_length = MNEMONIC_LENGTH_MAP[15]
mnemonic_service = Mnemonic("english")


class PublicKey:
    def __init__(self, private_key):
        self.point = int.from_bytes(private_key, byteorder='big') * BIP32_CURVE.generator

    def __bytes__(self):
        xstr = self.point.x().to_bytes(32, byteorder='big')
        parity = self.point.y() & 1
        return (2 + parity).to_bytes(1, byteorder='big') + xstr

    def address(self):
        x = self.point.x()
        y = self.point.y()
        s = x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
        return to_checksum_address(eth_utils_keccak(s)[12:])


def mnemonic_to_bip39seed(mnemonic, passphrase):
    mnemonic = bytes(mnemonic, 'utf8')
    salt = bytes(BIP39_SALT_MODIFIER + passphrase, 'utf8')
    return hashlib.pbkdf2_hmac('sha512', mnemonic, salt, BIP39_PBKDF2_ROUNDS)


def bip39seed_to_bip32masternode(seed):
    h = hmac.new(BIP32_SEED_MODIFIER, seed, hashlib.sha512).digest()
    key, chain_code = h[:32], h[32:]
    return key, chain_code


def derive_bip32childkey(parent_key, parent_chain_code, i):
    assert len(parent_key) == 32
    assert len(parent_chain_code) == 32
    k = parent_chain_code
    if (i & BIP32_PRIVDEV) != 0:
        key = b'\x00' + parent_key
    else:
        key = bytes(PublicKey(parent_key))
    d = key + struct.pack('>L', i)
    while True:
        h = hmac.new(k, d, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]
        a = int.from_bytes(key, byteorder='big')
        b = int.from_bytes(parent_key, byteorder='big')
        key = (a + b) % BIP32_CURVE.order
        if a < BIP32_CURVE.order and key != 0:
            key = key.to_bytes(32, byteorder='big')
            break
        d = b'\x01' + h[32:] + struct.pack('>L', i)
    return key, chain_code


def parse_derivation_path(str_derivation_path):
    path = []
    if str_derivation_path[0:2] != 'm/':
        raise ValueError("Can't recognize derivation path. It should look like \"m/44'/60/0'/0\".")
    for i in str_derivation_path.lstrip('m/').split('/'):
        if "'" in i:
            path.append(BIP32_PRIVDEV + int(i[:-1]))
        else:
            path.append(int(i))
    return path


def mnemonic_to_private_key(mnemonic, str_derivation_path, passphrase=""):
    derivation_path = parse_derivation_path(str_derivation_path)
    bip39seed = mnemonic_to_bip39seed(mnemonic, passphrase)
    master_private_key, master_chain_code = bip39seed_to_bip32masternode(bip39seed)
    private_key, chain_code = master_private_key, master_chain_code
    for i in derivation_path:
        private_key, chain_code = derive_bip32childkey(private_key, chain_code, i)
    return private_key


def get_address_key(mnemonic: str, index: int):
    private_key = mnemonic_to_private_key(mnemonic, str_derivation_path=f'{ETH_DERIVATION_PATH}/{index}')
    public_key = PublicKey(private_key)
    private_key_str = binascii.hexlify(private_key).decode("utf-8")
    public_key_str = binascii.hexlify(bytes(public_key)).decode("utf-8")
    address = public_key.address()
    return [private_key_str, public_key_str, address]


def gen_multi_mnemonic(mnemonic_count):
    all_wallet = []
    for i in range(0, mnemonic_count):
        wallet_account = {}
        mnemonic = mnemonic_service.generate(strength=mnemonic_length)
        ret = get_address_key(mnemonic, 0)
        wallet_account["id"] = i
        wallet_account["助记词"] = mnemonic
        wallet_account["私钥"] = ret[0]
        wallet_account["公钥"] = ret[1]
        wallet_account["地址"] = ret[2]
        all_wallet.append(wallet_account)
    return all_wallet


def get_by_single_mnemonic(mnemonic_count):
    mnemonic = mnemonic_service.generate(strength=mnemonic_length)
    all_wallet = {"助记词": mnemonic, "钱包": []}
    for i in range(0, mnemonic_count):
        wallet_account = {}
        ret = get_address_key(mnemonic, i)
        wallet_account["id"] = i
        wallet_account["私钥"] = ret[0]
        wallet_account["公钥"] = ret[1]
        wallet_account["地址"] = ret[2]
        all_wallet["钱包"].append(wallet_account)
    return all_wallet


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print(f"# 未找到 输入参数 【生成数量】【生成模式】")
        print(f"# 未找到 生成数量和生成模式 参数： {sys.argv[0]} [生成数量] [模式 1:按随机助记词 2：按固定助记词] ")
        print(f"# 举个栗子1: 生成10个地址 固定助记词: {sys.argv[0]} 10  1 ")
        print(f"# 举个栗子2: 生成10个地址 随机助记词 : {sys.argv[0]} 10  2 ")
        exit()

    count = int(sys.argv[1])
    mode = int(sys.argv[2])
    file_prefix = {1: "随机助记词", 2: "固定助记词"}
    if mode == 1:
        ret = gen_multi_mnemonic(count)
    elif mode == 2:
        ret = get_by_single_mnemonic(count)
    else:
        print(f"输入的参数不正确 {sys.argv}")
        print(f"# 未找到 输入参数 【生成数量】【生成模式】")
        print(f"# 未找到 生成数量和生成模式 参数： {sys.argv[0]} [生成数量] [模式 1:按随机助记词 2：按固定助记词] ")
        print(f"# 举个栗子1: 生成10个地址 固定助记词: {sys.argv[0]} 10  1 ")
        print(f"# 举个栗子2: 生成10个地址 随机助记词 : {sys.argv[0]} 10  2 ")
        exit()

    filename = f"{file_prefix[mode]}_{count}个地址_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(ret, f, ensure_ascii=False, indent=4)
    print(f"生成文件: {filename}")
