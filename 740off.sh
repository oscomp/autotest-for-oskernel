#!/bin/bash
set -ex
python3 test_relay.py $1 2 on
sleep 4;
python3 test_relay.py $1 2 off