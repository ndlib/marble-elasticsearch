#!/bin/bash
magenta=`tput setaf 5`
reset=`tput sgr0`

echo "${magenta}----- BUILD -----${reset}"

# build
cdk synth || { echo "Synthesizing cloud formation failed"; exit 1; }