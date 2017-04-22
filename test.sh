#!/bin/bash

virtualenv run 
. run/bin/activate

pip install --upgrade -r requirements.txt

python queue_test.py -v

deactivate
