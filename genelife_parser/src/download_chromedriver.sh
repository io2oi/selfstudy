#!/usr/bin/env bash

# This script is used to download the chromedriver executable.
# This script assumes that the user has a working internet connection.
# This script assumes the version chrome browser is 97.x.x.x

uname_str=`uname`
if [ "$uname_str"="Darwin" ]; then
    ostype="mac"
elif [ "$uname_str"="Linux" ]; then
    ostype="linux"
else
    echo "Unsupported OS: $uname_str"
    exit 1
fi

DRIVER_FILE_NAME="chromedriver_"${ostype}"64.zip"
[ -f "$DRIVER_FILE_NAME" ] && echo "${DRIVER_FILE_NAME} exists. Bye. " && exit 1
DRIVER_ADDRESS="https://chromedriver.storage.googleapis.com/97.0.4692.71/${DRIVER_FILE_NAME}"
wget -nd $DRIVER_ADDRESS
unzip -o $DRIVER_FILE_NAME