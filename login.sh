#!/bin/sh
cp ../users.json .
cp ../secret.key .
echo Email : Bob@email.com Password : password 
sudo python main.py
