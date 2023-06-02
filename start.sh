#!/bin/bash
cd src
echo "staring api..."
nohup gunicorn -w 4 main:app -b :5856 --timeout=600 > /dev/null 2>&1 &
