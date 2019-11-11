#!/bin/bash
magenta=`tput setaf 5`
reset=`tput sgr0`

echo "${magenta}----- BUILD SETUP -----${reset}"
stackname=${1}
deploy_cfg="deploy.json"
stack_json="{ \"stackname\": \"${stackname}\" }"
echo ${stack_json} > ${deploy_cfg}