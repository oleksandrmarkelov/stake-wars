# stake-wars
The guide below explains how to setup near validator in azure in less expensive way.

Prerequisites: 
- credit card.

## Step 1. Login into Azure Portal and create user/with existing user
Go to http://portal.azure.com

![image](https://user-images.githubusercontent.com/63374230/179372498-51e51e63-6576-4215-aab4-1df7f498d5c0.png)

Create new user or login with exisitng

## Step 2. Select subscription

Select "Start with an Azure free trial" and provide credit card details.

![image](https://user-images.githubusercontent.com/63374230/179372619-340e4c64-3651-4a76-95c7-5f1f97af88b6.png)

## Step 3. Order Virtual machine

Select Virtual machines

<img width="1127" alt="image" src="https://user-images.githubusercontent.com/63374230/179372804-fd220df1-d36d-47df-a325-7e1517a355f1.png">

Create a new VM

<img width="1127" alt="image" src="https://user-images.githubusercontent.com/63374230/179372837-448a96ab-d6cb-4924-987b-54d27f94a3fc.png">

On the basics tab create a new resource group. In "Availability options" select availability set and create a new set with default configuration. The avialability zone would create replicated instances of validator which would require higher costs. Select image Ubuntu and size "Standart_B4ms". 

<img width="1127" alt="image" src="https://user-images.githubusercontent.com/63374230/179372879-17578b00-6721-497e-bf52-f9e60a9371fb.png">

In the public ports select SSH(22)

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/63374230/179373068-c459cb51-dfa3-402d-ba0c-bd34462c18ff.png">

On the disks tab select Premium SSD for OS and add 1T Premium SSD data disk

<img width="907" alt="image" src="https://user-images.githubusercontent.com/63374230/179373103-b2c49a6f-99af-462e-a84c-cb3c7e0d881f.png">

On the rest of tabs keep default option to create virtual network and publiv IP

![image](https://user-images.githubusercontent.com/63374230/179373131-13b84c8e-5045-4250-808b-bbf857793181.png)

On the last tab click create. The total cost of the server is displayed before creation.

<img width="710" alt="image" src="https://user-images.githubusercontent.com/63374230/179373163-4f7d48c9-7009-4bd8-b95e-86db75dfa5a2.png">

## Step 4. Connect to VM and mount the data drive

Go to newly created VM and mark IP

<img width="1244" alt="image" src="https://user-images.githubusercontent.com/63374230/179373327-95e22d92-b963-4912-af9a-6c5a6965aa9f.png">

Connect to VM with putty, how to mount the drive is described in details under https://docs.microsoft.com/en-us/azure/virtual-machines/linux/attach-disk-portal. In short find list the drives 
```
lsblk -o NAME,HCTL,SIZE,MOUNTPOINT | grep -i "sd"
```
Output
<img width="440" alt="image" src="https://user-images.githubusercontent.com/63374230/179373453-0d25cbd6-3e7e-4bce-9b05-194af08f7751.png">

Find the drive with 1T and prepare it (assuming the drive called sda)
```
sudo parted /dev/sda --script mklabel gpt mkpart xfspart xfs 0% 100%
sudo mkfs.xfs /dev/sda1
sudo partprobe /dev/sda1
```
Mount the drive
```
sudo mkdir /datadrive
sudo mount /dev/sda1 /datadrive
```
To ensure that the drive is remounted automatically after a reboot, it must be added to the /etc/fstab file. Details are in the article https://docs.microsoft.com/en-us/azure/virtual-machines/linux/attach-disk-portal

## Step 5. Setup validator

According to Stake Wars instructions (Challenge 001, 002, 003 and 004) setup the validator. 

Important note: The validator needs to be installed into data disk (mounted under /datadrive). The OS drive is limited to 32 GB and must not be used for installation. Therefore: clone nearcore and init home folder into /datadrive.

Below is the list of instructions to setup validator into /datadrive/nearval/ folder for nearval user
```
sudo apt update && sudo apt upgrade -y
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -  
sudo apt install build-essential nodejs
PATH="$PATH"
sudo npm install -g near-cli
export NEAR_ENV=shardnet
sudo apt install -y git binutils-dev libcurl4-openssl-dev zlib1g-dev libdw-dev libiberty-dev cmake gcc g++ python docker.io protobuf-compiler libssl-dev pkg-config clang llvm cargo
sudo apt install python3-pip
USER_BASE_BIN=$(python3 -m site --user-base)/bin
export PATH="$USER_BASE_BIN:$PATH"
sudo apt install clang build-essential make
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

cd /datadrive
sudo mkdir -p 755 nearval
sudo chown nearval:nearval nearval
cd nearval

git clone https://github.com/near/nearcore
cd nearcore
git fetch
git checkout master
cargo build -p neard --release --features shardnet
./target/release/neard --home /datadrive/nearval/.near init --chain-id shardnet --download-genesis
rm /datadrive/nearval/.near/config.json
wget -O /datadrive/nearval/.near/config.json https://s3-us-west-1.amazonaws.com/build.nearprotocol.com/nearcore-deploy/shardnet/config.json
sed -e 's/"archive": false/"archive": true/' -i config.json
sudo apt-get install awscli -y
cd /datadrive/nearval/.near
aws s3 --no-sign-request cp s3://build.openshards.io/stakewars/shardnet/data.tar.gz .  
tar -xzvf data.tar.gz
pip3 install awscli --upgrade
cd nearcore
./target/release/neard --home /datadrive/nearval/.near run
near login
near generate-key <pool_id>
cp ~/.near-credentials/shardnet/YOUR_WALLET.json /datadrive/nearval/.near/validator_key.json
target/release/neard --home /datadrive/nearval/.near run

near call factory.shardnet.near create_staking_pool '{"staking_pool_id": "<pool id>", "owner_id": "<accountId>", "stake_public_key": "<public key>", "reward_fee_fraction": {"numerator": 5, "denominator": 100}, "code_hash":"DD428g9eqLL8fWUxv8QSpVFzyHi1Qd16P8ephYCTmMSZ"}' --accountId="<accountId>" --amount=30 --gas=300000000000000
near call <pool_name> update_reward_fee_fraction '{"reward_fee_fraction": {"numerator": 1, "denominator": 100}}' --accountId <account_id> --gas=300000000000000
```

## Pricing
The server cost is 0.164 CHF per hour, in addition to storage, IP address, and virtual network. which is approx. 220 USD per month. 

![image](https://user-images.githubusercontent.com/63374230/179889228-d4bba662-bea9-4570-b72c-771761a20da6.png)




