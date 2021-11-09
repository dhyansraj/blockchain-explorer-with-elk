import requests
import json
from types import SimpleNamespace
from ast import literal_eval
from datetime import datetime
import pandas as pd
import os
import time

url = 'http://ethereum:8545'
headers = {"Content-Type": "application/json; charset=utf-8"}
log_file_location = "/home/ethingester/output/ethereum.log"

log_file = open(log_file_location, "a")

def get_latest_block_number():
    input = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":83}'

    response = requests.post(url, headers=headers, data=input)

    if response.status_code == 200:
        data = response.json()

        return literal_eval(data['result'])

def wait_for_geth():
    while True:

        if type(get_latest_block_number()) != int or get_latest_block_number() == 0:
            time.sleep(10)
        else:
            print("Started instegsting logs")
            break

def get_block_by_number(n):

    input = json.loads('{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x4", true],"id":1}')

    input['params'] = [hex(n), True]

    response = requests.post(url, headers=headers, data=json.dumps(input))

    if response.status_code == 200:
        response_data = response.json()
        block = SimpleNamespace(** SimpleNamespace(** response_data).result)

        return block


def transform_block_data(b):
    delattr(b, 'extraData')
    delattr(b, 'logsBloom')
    delattr(b, 'mixHash')
    delattr(b, 'nonce')
    delattr(b, 'receiptsRoot')
    delattr(b, 'sha3Uncles')
    delattr(b, 'stateRoot')
    delattr(b, 'transactions')
    delattr(b, 'transactionsRoot')
    delattr(b, 'uncles')

    setattr(b, 'difficulty', literal_eval(b.difficulty))
    setattr(b, 'gasLimit', literal_eval(b.gasLimit))
    setattr(b, 'gasUsed', literal_eval(b.gasUsed))
    setattr(b, 'hash', literal_eval(b.hash))
    setattr(b, 'miner', b.miner)
    setattr(b, 'blockNumber', literal_eval(b.number))
    setattr(b, 'parentHash', b.parentHash)
    setattr(b, 'size', literal_eval(b.size))
    setattr(b, 'timestamp', pd.to_datetime(literal_eval(b.timestamp), unit='s').strftime('%Y-%m-%d %H:%M:%S'))
    setattr(b, 'totalDifficulty', literal_eval(b.totalDifficulty))

    delattr(b, 'number')

    return b


def transform_log_data(b, t):
    delattr(t, 'input')
    delattr(t, 'v')
    delattr(t, 'r')
    delattr(t, 's')
    delattr(t, 'nonce')
    if hasattr(t, 'maxPriorityFeePerGas'):
        delattr(t, 'maxPriorityFeePerGas')
    if hasattr(t, 'accessList'):
        delattr(t, 'accessList')
    if hasattr(t, 'chainId'):
        delattr(t, 'chainId')
    if hasattr(t, 'maxFeePerGas'):
        delattr(t, 'maxFeePerGas')

    setattr(t, 'difficulty', literal_eval(b.difficulty))
    setattr(t, 'gasLimit', literal_eval(b.gasLimit))
    setattr(t, 'gasUsed', literal_eval(b.gasUsed))
    setattr(t, 'hash', literal_eval(b.hash))
    setattr(t, 'miner', b.miner)
    setattr(t, 'parentHash', b.parentHash)
    setattr(t, 'size', literal_eval(b.size))
    setattr(t, 'timestamp', pd.to_datetime(literal_eval(b.timestamp), unit='s').strftime('%Y-%m-%d %H:%M:%S'))
    setattr(t, 'totalDifficulty', literal_eval(b.totalDifficulty))

    t.blockNumber = literal_eval(t.blockNumber)
    t.gas = literal_eval(t.gas)
    t.gasPrice = literal_eval(t.gasPrice)
    t.transactionIndex = literal_eval(t.transactionIndex)
    t.value = literal_eval(t.value)

    return t

def print_txn_in_block(n):
    block = get_block_by_number(n)

    if len(block.transactions) > 0 :
        for t in block.transactions:
            t = transform_log_data(block, SimpleNamespace(** t))
            log_file.write(json.dumps(vars(t)) + "\n")
            log_file.flush()
    else:
        log_file.write(json.dumps(vars(transform_block_data(block))) + "\n")
        log_file.flush()

def last_written_block_number():
    try:
        with open(log_file_location, 'rb') as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            block = json.loads(last_line)

            return block['blockNumber'] + 1

    except OSError:
        return 1
    except ValueError:
        return 1

def main():
    block_height = get_latest_block_number()
    current_block = last_written_block_number()

    print(f"block_height={block_height}, current_block={current_block}")

    while True:

        if(current_block < block_height):
            print_txn_in_block(current_block)
            current_block += 1

        if current_block == block_height:
            block_height = get_latest_block_number()

            if current_block == block_height:
                time.sleep(10)

if __name__ == "__main__":
    wait_for_geth()
    main()
