#!/bin/bash
magenta=`tput setaf 5`
reset=`tput sgr0`

echo "${magenta}----- INSTALL -----${reset}"

# We need to specify a version so the pipeline won't break from an update
npm install -g aws-cdk@1.7 || { echo "CDK install failed"; exit 1; }

pip install -r requirements.txt
