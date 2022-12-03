import json
import configparser
from web3 import Web3
from web3.middleware import geth_poa_middleware

# 加载现有配置文件
conf = configparser.ConfigParser()
conf.read('./env.conf', encoding='utf-8')

ACC = conf.get('Account', 'addr') # 个人钱包地址
KEY = conf.get('Account', 'key')
CONTRACT = Web3.toChecksumAddress(conf.get('Contract', 'addr')) # 合约地址
API = "https://goerli.infura.io/v3/" + conf.get('Account', 'api')

with open('./contract_abi.json', 'r') as contract_abi:
    abi = json.load(contract_abi)

# 提供HTTPProvider，链上互动的接口
w3 = Web3(Web3.HTTPProvider(API))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入poa中间件
# 因为POA共识算法在extraData字段添加了一些额外的数据从而导致该字段超过以太坊的黄皮书约定的32字节长度，
# 而Web3.py默认情况下是按照以太坊黄皮书的约定来检查extraData字段的长度，这造成了不一致并抛出异常。

# 检查HTTPProvider
if not w3.isConnected():
    exit('Web3 connect failed!')
print('ClientVersion: ', w3.clientVersion)

# 创建合约实例
contract = w3.eth.contract(address=CONTRACT, abi=abi)

# 调用合约功能
balance = contract.functions.banana().call()
print(balance)

def claim(info:dict):
    ## build Claim TX
    claim_tx = contract.functions.claim(
        info["ethAddress"],
        info["useFor"],
        int(info["amount"]),
        info["signatureExpiredTime"],
        info["nonce"],
        info["signature"]
    ).buildTransaction(
        {
            'from': ACC,
            'gas': 700000,
            'gasPrice': w3.toWei('1', 'gwei'),
            'nonce': w3.eth.get_transaction_count(ACC),
        }
    )
    ## Sign TX with PK
    tx_create = w3.eth.account.sign_transaction(claim_tx, KEY)
    ## Send TX and wait for receipt
    try:
        tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    except ValueError as e:
        print(f'id~{info["id"]}&user~{info["ethAddress"]} with err: { e }')
    else:
        print(f'id~{info["id"]}&user~{info["ethAddress"]} with hash: { tx_receipt.transactionHash.hex() }')

if __name__ == "__main__":
    with open('./claim.json', 'r') as infos:
        info_list = json.load(infos)

    for info in info_list:
        # exit(claim(info))
        claim(info)