#!/usr/bin/env bash

NAME="$(basename $0)"
SRC="$(realpath $(dirname $0))"
XKB="/usr/share/X11/xkb"

function check_xkb {
    if [[ ! -d $XKB ]]
    then
        echo "XKB installation not found at $XKB"
        exit 1
    fi
}

function install_symbols {
    sudo cp $SRC/symbols/eumak $XKB/symbols/
}

function uninstall_symbols {
    sudo rm $XKB/symbols/eumak
}

function install_rules {
    sudo $SRC/_install_rules.py install "${XKB}/rules/evdev.xml"
}

function uninstall_rules {
    sudo $SRC/_install_rules.py uninstall "${XKB}/rules/evdev.xml"
}

check_xkb
if [[ "${NAME}" == "uninstall.sh" ]]
then
    uninstall_symbols
else
    install_symbols
    install_rules
fi

