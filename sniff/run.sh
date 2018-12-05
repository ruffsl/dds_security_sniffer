#!/bin/bash
FILE=./tshark_recording.pcapng
tshark -i br-$(docker network ls -f name=sros2_default -q) -w $FILE -F pcapng -a duration:60
python3 extract.py ./$FILE
python3 construct.py .
