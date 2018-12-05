#!/bin/bash
FILE=$(ls -t /root/*.pcapng)
set -- $FILE
python3 extract.py $FILE
python3 construct.py .
