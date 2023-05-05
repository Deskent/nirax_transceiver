export $(cat .swarm.prod.env) && docker stack deploy -c ./docker-swarm.prod.yml transceiver_prod
