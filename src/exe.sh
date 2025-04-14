#!/bin/bash

docker-compose up
fastapi dev main.py --reload --port 8000
