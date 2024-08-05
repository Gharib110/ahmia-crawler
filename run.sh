#!/bin/bash

cd ahmia

MAX_TIME=2160 # 25 days
FINAL_MAX_TIME=2163 # Finally, wait 60 mins more

echo ""
time timeout --signal=SIGKILL $FINAL_MAX_TIME timeout --kill-after=120 --signal=SIGINT $MAX_TIME scrapy crawl ahmia-tor -s DEPTH_LIMIT=1
echo ""
