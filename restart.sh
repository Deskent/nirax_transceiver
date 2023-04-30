#!/bin/sh
docker-compose down --remove-orphans &&
docker-compose up --build -d &&
docker logs -f nirax_transceiver | ccze -A
