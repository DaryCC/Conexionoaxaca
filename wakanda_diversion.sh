#!/usr/bin/sh
rm -rf ./images/*
wait 1
source .venv/bin/activate
wait 2
copyq&
wait 2
python oaxaca2.py                                                                                                                                                               
