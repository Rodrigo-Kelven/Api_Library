#!/bin/bash

docker-compose up -d
fastapi dev main.py --reload --port 8000
