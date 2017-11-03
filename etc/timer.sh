#!/bin/bash

if [ $@ -ne 3 ]; then
    echo -n "Duration?: "
    read duration
    echo -n "Rest?: "
    read rest
else
    duration=$1
    rest=$2
fi

function prtBanner() {
    banner "$1 $2" && sleep 1
    clear
}
function du() {
    for __ii__ in `seq 1 $1`; do
	prtBanner "Go!" $__ii__
    done
    paplay /usr/share/sounds/ubuntu/notifications/Amsterdam.ogg
}
function re() {
    for __ii__ in `seq 1 $1`; do
	prtBanner "Rest!" $__ii__
    done
    paplay /usr/share/sounds/ubuntu/notifications/Mallet.ogg
}
function start() {
    clear
    prtBanner "Ready!" 5 
    for __ii__ in `seq 4 -1 1`; do
	prtBanner "Ready!" $__ii__
    done
    paplay /usr/share/sounds/ubuntu/notifications/Mallet.ogg
}

start
clear
for ii in `seq 3 -1 1`; do
    du $duration
    clear
    if [ $ii -ne 1 ]; then
	re $rest
	clear
    fi
done
