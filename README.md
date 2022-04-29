# 批量ETH创建钱包地址助记词 batch create eth wallet

Batch eth helper creation public key, private key wallet address

批量创建 eth  助记词 公钥，私钥 钱包地址

1、先安装依赖  

    pip3 install -r requirement.txt

用法: 

    python3 publicKey.py [数量] [模式]  

2、模式一：使用随机助记词生成2个钱包地址

    python3.x publicKey.py 2 1

生成： 随机助记词_2个地址_年-月-日_时-分-秒.json   文件

    文件内容
    [
        {
            "id": 0,
            "助记词": "panda ensure crawl unfair category merge very twist fire trash hotel jeans unknown swamp deal either panda bomb venture detail scan write fiscal ankle",
            "私钥": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "公钥": "031485e28599522e5d535cc0a72d53d2027239ce5a0d3a2eac302b7f8f59374c88",
            "地址": "0xc94D6BDfBc31f1cBE73C04e35B0f5D215Ffe65e8"
        },
        {
            "id": 1,
            "助记词": "present ice clerk skate notice youth furnace despair drive team runway humor prosper design basic nasty pause tank inspire print shield leaf must olive",
            "私钥": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "公钥": "030f751c55a0c89b95f2182fa4d7773f39529a07f672278fd88367aa6c5e49572a",
            "地址": "0xff496224317f9Ce21cA3294c47203C75F2Cd010F"
        }
    ]




3、模式二：使用固定助记词生成2个钱包地址 

      python3.x publicKey.py 100 2
      
生成： 固定助记词_2个地址_年-月-日_时-分-秒.json   文件
     
    文件内容
     {
          "助记词": "guitar shock advance invite danger raw start fuel verify clean illegal hammer term claw indoor learn fuel draft inherit sort stay flee trigger arm",
          "钱包": [
              {
                  "id": 0,
                  "私钥": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                  "公钥": "039c86bb0339a97f2425cd88eb9ad06840bfe0a1c2264e39324102400ef06a718d",
                  "地址": "0x37097Ff2164fe37D2dd7141F0a5F0EB47a8B5F53"
              },
              {
                  "id": 1,
                  "私钥": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                  "公钥": "03ed91be6f4ac403535f9f117940138d4efd912159f8fb1f24467957ddffd82281",
                  "地址": "0x62090336Fb8e5fBb024c502A74B9647b374bC35f"
              }
          ]
      }
