#!/bin/bash
set -e
sudo systemctl restart expenseapp.service
sudo systemctl status expenseapp.service --no-pager
