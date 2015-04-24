#!/bin/bash

# Dependencies.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install requests[security]

# Setting-up database.
python setup.py