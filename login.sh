#!/bin/sh
cp ../users.json .
cp ../secret.key .
echo Email : Bob@email.com Password : password 
sudo python3 main.py
