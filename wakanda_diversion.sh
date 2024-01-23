#!/usr/bin/sh

copyq&

wait 1
source .venv/bin/activate                                                                                                                                                       
wait 2
python oaxaca2.py                                                                                                                                                               
