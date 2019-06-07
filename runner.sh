#!/bin/bash

python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 0 -e 500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 501 -e 1000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 1001 -e 1500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 1501 -e 2000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 2001 -e 2500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 2501 -e 3000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 3001 -e 3500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 3501 -e 4000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 4001 -e 4500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 4501 -e 5000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 5001 -e 5500 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 5501 -e 6000 &
sleep 0.5
python3 taskrabbit_crawler.py -w ./chromedriver -q final_queries.json -b 6001 -e 6272 &

wait

echo "All queries completed"