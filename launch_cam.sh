#!/bin/bash

token=/home/pi/wild_camera/secrets/BOT_TOKEN
wildlife_telegram=/home/pi/wild_camera/wildlife-telegram
py_env=/home/pi/py_envs/wild_py

source $py_env/bin/activate

cd $wildlife_telegram
sleep 5
python3 main.py --bot_token $(cat $token)



