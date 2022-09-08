import subprocess
import re
import sys
import os.path

message="Status: "
chunk_initial=5
chunk_thold=0.8
stake_warn=1000
block_file_name='block_height.txt'

result = subprocess.getoutput('curl -s -d \'{"jsonrpc": "2.0", "method": "status", "id": "dontcare", "params": [null]}\' -H \'Content-Type: application/json\' 127.0.0.1:3030 | jq -c \'.result.sync_info\'')
if 'latest_block_height' not in result:
    subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot5481157987:AAHe4urIjOv-Ys_1fpi4dV6DdeoUTAXVbIE/sendMessage -d chat_id=-1001612732257 -d parse_mode="Markdown" -d text="Validator is offline"')
    sys.exit()

result = subprocess.getoutput('curl -s -d \'{"jsonrpc": "2.0", "method": "status", "id": "dontcare", "params": [null]}\' -H \'Content-Type: application/json\' 127.0.0.1:3030 | jq -c \'.result.sync_info.latest_block_height\'')
newblock = int(result)
print(newblock)
old_block = -1
if os.path.exists(block_file_name):
    with open(block_file_name, 'r') as f:
        old_block = int(f.read())
print(old_block)
if(newblock<=old_block):
    subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot5481157987:AAHe4urIjOv-Ys_1fpi4dV6DdeoUTAXVbIE/sendMessage -d chat_id=-1001612732257 -d parse_mode="Markdown" -d text="No new blocks produced, last '+str(newblock)+'"')
else:
    with open(block_file_name, 'w') as f:
        f.write(str(newblock))
result = subprocess.getoutput(['near validators current | grep seat'])
rx = re.compile(r'\bprice:[^)]*')
seat = int(rx.findall(result)[0].split(':')[1].replace(',',''))
result = subprocess.getoutput(['near validators current | grep markelov'])
parts = result.split('|')
stake = int(parts[2].replace(',',''))
produced = int(parts[7])
expected = int(parts[8])
rate=produced/expected
if (expected > chunk_initial) and (chunk_thold > rate):
    subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot5481157987:AAHe4urIjOv-Ys_1fpi4dV6DdeoUTAXVbIE/sendMessage -d chat_id=-1001612732257 -d parse_mode="Markdown" -d text="Low block production '+str(produced)+"/"+str(expected)+'"')
if seat + stake_warn > stake:
    subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot5481157987:AAHe4urIjOv-Ys_1fpi4dV6DdeoUTAXVbIE/sendMessage -d chat_id=-1001612732257 -d parse_mode="Markdown" -d text="Stake too low '+str(stake)+"/"+str(seat)+'"')
