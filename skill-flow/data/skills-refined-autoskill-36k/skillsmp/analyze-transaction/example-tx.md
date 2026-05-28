# Example Transaction

## About Andamio API

The Andamio API provides REST endpoints for building valid Cardano transactions. All transactions are documented at https://atlas-api-preprod-507341199760.us-central1.run.app/swagger.json

Each endpoint accepts a necessary set of parameters in the request body, and returns unsigned transaction CBOR. 

This CBOR can be decoded into JSON. 

## Examples

### This request:
```bash
curl -X 'POST' \
  'https://atlas-api-preprod-507341199760.us-central1.run.app/v2/tx/global/general/access-token/mint' \
  -H 'accept: application/json;charset=utf-8' \
  -H 'Content-Type: application/json;charset=utf-8' \
  -d '{
  "initiator_data": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
  "alias": "somealias"
}'
```

### Yields this response, with an unsigned transaction in CBOR format:
```json
{
  "unsigned_tx": "84ab00d901028282582055b81a73d2e0b472ec3c5431515dff0697a4c23aec8a4d216900141f094ed7c700825820607ef78bbc4bf1b4d519b42c521d31130fe6b5046352a867cf3cd4a7e243d1d2000188a3005839304758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c92e162807df59763a4c1fd4d54ceb6f33cae3ceb8a0ed4c97d68226001821a00132342a1581c4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063ca1412001028201d81856d8799f47706f776e65723149736f6d65616c696173ffa3005839304758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c92e162807df59763a4c1fd4d54ceb6f33cae3ceb8a0ed4c97d68226001821a00133418a1581c4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063ca1412001028201d81857d8799f49736f6d65616c696173487465616368657231ff825839009eac365b4bead2b70a6da30a3c8538adb2949242fd721104b35378c6bee003ff51c57fec5d5d678e14babbc21b87b1f8455540752a0cc46f1a004c4b40a300583930d5c90b00801e17279d88272312b5ad6cea3668a16289fb35927e4ef792e162807df59763a4c1fd4d54ceb6f33cae3ceb8a0ed4c97d68226001821a001344eea1581c4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063ca14a67736f6d65616c69617301028201d8184fd8799f49736f6d65616c696173a0ff82583900957aaaf3b663749e6fa6d57137bddf03acb5206320a84c17df12c7e46405d6906b097597b1b5de2cd50d85ad3cd55a88e62a62ad7907c0b51a0139488982583900957aaaf3b663749e6fa6d57137bddf03acb5206320a84c17df12c7e46405d6906b097597b1b5de2cd50d85ad3cd55a88e62a62ad7907c0b51a04b0a8ac82583900957aaaf3b663749e6fa6d57137bddf03acb5206320a84c17df12c7e46405d6906b097597b1b5de2cd50d85ad3cd55a88e62a62ad7907c0b5821a013d43d6a1581c4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063ca14a75736f6d65616c6961730182583900957aaaf3b663749e6fa6d57137bddf03acb5206320a84c17df12c7e46405d6906b097597b1b5de2cd50d85ad3cd55a88e62a62ad7907c0b51a015166e0021a0005607905a1581df0034295fa4682513591fdd39550083bb074b494a21cc4e712a6d6cb7e00075820c5331a5093754d320e9e3f820f7a780bd2163a86bf1cbce800625edfde1c8f7b09a1581c4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063ca34120014a67736f6d65616c696173014a75736f6d65616c696173010b5820e08e257d6fb1efb7696cfee958f367099bf4655fb4e2342eaad5125dfc1ca97d0dd901028182582006770f631599f82119f599f492f68ad68c067c13442e07883e6c3d5bab4defaf001082583900957aaaf3b663749e6fa6d57137bddf03acb5206320a84c17df12c7e46405d6906b097597b1b5de2cd50d85ad3cd55a88e62a62ad7907c0b51a08e8c0ca111a000810b612d901028282582057701f1a1870c1786524f0462b608e1fb8f597694c49c18cea058032812c79370082582057701f1a1870c1786524f0462b608e1fb8f597694c49c18cea058032812c793702a105a382000082d87980821a0001574b1a01bf34448201008249736f6d65616c696173821a000778ef1a0a38c1908203008249736f6d65616c696173821a0001d1401a02ce174bf5d90103a100a11902d1a178383437353836313338363761386137616135303062356435376130653837376630316138653633633133363534363935383962313230363363a16a75736f6d65616c696173a8646e616d6574416e64616d696f2041636365737320546f6b656e65616c69617369736f6d65616c69617365696d616765827838697066733a2f2f62616679626569686a676e74686b747278686f7172346d6e636d736a6e6e37366f6b3434666672647836736569647a6f376a65667834683273676734696d656469615479706567696d6167652f2a6b6465736372697074696f6e816d46697273742045646974696f6e636572616e466f756e646174696f6e20457261636170707668747470733a2f2f6170702e616e64616d696f2e696f6566696c657381a2696d656469615479706567696d6167652f2a63737263827838697066733a2f2f62616679626569686a676e74686b747278686f7172346d6e636d736a6e6e37366f6b3434666672647836736569647a6f376a65667834683273676734"
}
```

### When we decode this CBOR, we get:
```json
{
  "transaction_hash": "785f364529c1ffca3862a154192ca276e8552b6e6f1ddfa22c710245b66af7db",
  "transaction": {
    "body": {
      "inputs": [
        {
          "index": 0,
          "transaction_id": "55b81a73d2e0b472ec3c5431515dff0697a4c23aec8a4d216900141f094ed7c7"
        },
        {
          "index": 0,
          "transaction_id": "607ef78bbc4bf1b4d519b42c521d31130fe6b5046352a867cf3cd4a7e243d1d2"
        }
      ],
      "outputs": [
        {
          "address": "addr_test1xpr4scfcv75202jspdw40g8gwlcp4rnrcym9g62cnvfqv0yju93gql04ja36fs0af42vadhn8jhre6u2pm2vjltgyfsqkhmv8z",
          "amount": {
            "coin": "1254210",
            "multiasset": {
              "4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c": {
                "20": "1"
              }
            }
          },
          "plutus_data": {
            "Data": "{\"constructor\":0,\"fields\":[{\"bytes\":\"706f776e657231\"},{\"bytes\":\"736f6d65616c696173\"}]}"
          },
          "script_ref": null
        },
        {
          "address": "addr_test1xpr4scfcv75202jspdw40g8gwlcp4rnrcym9g62cnvfqv0yju93gql04ja36fs0af42vadhn8jhre6u2pm2vjltgyfsqkhmv8z",
          "amount": {
            "coin": "1258520",
            "multiasset": {
              "4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c": {
                "20": "1"
              }
            }
          },
          "plutus_data": {
            "Data": "{\"constructor\":0,\"fields\":[{\"bytes\":\"736f6d65616c696173\"},{\"bytes\":\"7465616368657231\"}]}"
          },
          "script_ref": null
        },
        {
          "address": "addr_test1qz02cdjmf04d9dc2dk3s50y98zkm99yjgt7hyygykdfh3347uqpl75w90lk96ht83c2t4w7zrwrmr7z924q822svc3hstlm4js",
          "amount": {
            "coin": "5000000",
            "multiasset": null
          },
          "plutus_data": null,
          "script_ref": null
        },
        {
          "address": "addr_test1xr2ujzcqsq0pwfua3qnjxy4444kw5dng593gn7e4jflyaauju93gql04ja36fs0af42vadhn8jhre6u2pm2vjltgyfsq764wdy",
          "amount": {
            "coin": "1262830",
            "multiasset": {
              "4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c": {
                "67736f6d65616c696173": "1"
              }
            }
          },
          "plutus_data": {
            "Data": "{\"constructor\":0,\"fields\":[{\"bytes\":\"736f6d65616c696173\"},{\"map\":[]}]}"
          },
          "script_ref": null
        },
        {
          "address": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
          "amount": {
            "coin": "20531337",
            "multiasset": null
          },
          "plutus_data": null,
          "script_ref": null
        },
        {
          "address": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
          "amount": {
            "coin": "78686380",
            "multiasset": null
          },
          "plutus_data": null,
          "script_ref": null
        },
        {
          "address": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
          "amount": {
            "coin": "20792278",
            "multiasset": {
              "4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c": {
                "75736f6d65616c696173": "1"
              }
            }
          },
          "plutus_data": null,
          "script_ref": null
        },
        {
          "address": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
          "amount": {
            "coin": "22111968",
            "multiasset": null
          },
          "plutus_data": null,
          "script_ref": null
        }
      ],
      "fee": "352377",
      "ttl": null,
      "certs": null,
      "withdrawals": {
        "stake_test17qp59906g6p9zdv3lhfe25qg8wc8fdy55gwvfecj5mtvklsnff2kf": "0"
      },
      "update": null,
      "auxiliary_data_hash": "c5331a5093754d320e9e3f820f7a780bd2163a86bf1cbce800625edfde1c8f7b",
      "validity_start_interval": null,
      "mint": [
        [
          "4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c",
          {
            "20": "1",
            "67736f6d65616c696173": "1",
            "75736f6d65616c696173": "1"
          }
        ]
      ],
      "script_data_hash": "e08e257d6fb1efb7696cfee958f367099bf4655fb4e2342eaad5125dfc1ca97d",
      "collateral": [
        {
          "index": 0,
          "transaction_id": "06770f631599f82119f599f492f68ad68c067c13442e07883e6c3d5bab4defaf"
        }
      ],
      "required_signers": null,
      "network_id": null,
      "collateral_return": {
        "address": "addr_test1qz2h42hnke3hf8n05m2hzdaamup6edfqvvs2snqhmufv0eryqhtfq6cfwktmrdw79n2smpdd8n244z8x9f3267g8cz6s59993r",
        "amount": {
          "coin": "149471434",
          "multiasset": null
        },
        "plutus_data": null,
        "script_ref": null
      },
      "total_collateral": "528566",
      "reference_inputs": [
        {
          "index": 0,
          "transaction_id": "57701f1a1870c1786524f0462b608e1fb8f597694c49c18cea058032812c7937"
        },
        {
          "index": 2,
          "transaction_id": "57701f1a1870c1786524f0462b608e1fb8f597694c49c18cea058032812c7937"
        }
      ],
      "voting_procedures": null,
      "voting_proposals": null,
      "donation": null,
      "current_treasury_value": null
    },
    "witness_set": {
      "vkeys": null,
      "native_scripts": null,
      "bootstraps": null,
      "plutus_scripts": null,
      "plutus_data": null,
      "redeemers": [
        {
          "data": "{\"constructor\":0,\"fields\":[]}",
          "ex_units": {
            "mem": "87883",
            "steps": "29307972"
          },
          "index": "0",
          "tag": "Spend"
        },
        {
          "data": "{\"bytes\":\"736f6d65616c696173\"}",
          "ex_units": {
            "mem": "489711",
            "steps": "171491728"
          },
          "index": "0",
          "tag": "Mint"
        },
        {
          "data": "{\"bytes\":\"736f6d65616c696173\"}",
          "ex_units": {
            "mem": "119104",
            "steps": "47060811"
          },
          "index": "0",
          "tag": "Reward"
        }
      ]
    },
    "is_valid": true,
    "auxiliary_data": {
      "metadata": {
        "721": "{\"map\":[{\"k\":{\"string\":\"4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c\"},\"v\":{\"map\":[{\"k\":{\"string\":\"usomealias\"},\"v\":{\"map\":[{\"k\":{\"string\":\"name\"},\"v\":{\"string\":\"Andamio Access Token\"}},{\"k\":{\"string\":\"alias\"},\"v\":{\"string\":\"somealias\"}},{\"k\":{\"string\":\"image\"},\"v\":{\"list\":[{\"string\":\"ipfs://bafybeihjgnthktrxhoqr4mncmsjnn76ok44ffrdx6seidzo7\"},{\"string\":\"efx4h2sgg4\"}]}},{\"k\":{\"string\":\"mediaType\"},\"v\":{\"string\":\"image/*\"}},{\"k\":{\"string\":\"description\"},\"v\":{\"list\":[{\"string\":\"First Edition\"}]}},{\"k\":{\"string\":\"era\"},\"v\":{\"string\":\"Foundation Era\"}},{\"k\":{\"string\":\"app\"},\"v\":{\"string\":\"https://app.andamio.io\"}},{\"k\":{\"string\":\"files\"},\"v\":{\"list\":[{\"map\":[{\"k\":{\"string\":\"mediaType\"},\"v\":{\"string\":\"image/*\"}},{\"k\":{\"string\":\"src\"},\"v\":{\"list\":[{\"string\":\"ipfs://bafybeihjgnthktrxhoqr4mncmsjnn76ok44ffrdx6seidzo7\"},{\"string\":\"efx4h2sgg4\"}]}}]}]}}]}}]}}]}"
      },
      "native_scripts": null,
      "plutus_scripts": null,
      "prefer_alonzo_format": true
    }
  }
}
```