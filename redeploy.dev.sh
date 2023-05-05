export $(cat .swarm.dev.env) && docker stack deploy -c ./docker-swarm.dev.yml transceiver_dev
