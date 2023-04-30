docker stack rm nirax_transceiver \
&& sleep 2 \
&& docker network rm nirax_transceiver_default -f
export $(cat .swarm.dev.env) && docker stack deploy -c ./docker-swarm.dev.yml nirax_transceiver
