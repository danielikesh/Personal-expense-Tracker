#!/bin/bash
set -e
cd /home/ec2-user/Personal-expense-Tracker
sudo pip3 install -r requirements.txt
sudo systemctl daemon-reload
sudo systemctl enable expenseapp.service
