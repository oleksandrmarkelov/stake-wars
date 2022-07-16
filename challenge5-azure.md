# stake-wars
The guide below explains how to setup near validator in azure in less expensive way.

Prerequisites: 
- credit card.

Step 1. Login into Azure Portal and create user/with exisitng user
Goto http://portal.azure.com

![image](https://user-images.githubusercontent.com/63374230/179372498-51e51e63-6576-4215-aab4-1df7f498d5c0.png)

Create new user or login with exisitng

Step 2. Select subscription

Select "Start with an Azure free trial" and provide credit card details.

![image](https://user-images.githubusercontent.com/63374230/179372619-340e4c64-3651-4a76-95c7-5f1f97af88b6.png)

Step 3. Order Virtual machine

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






