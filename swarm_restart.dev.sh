docker stack rm dev \
&& sleep 2 \
&& docker network rm dev_default -f
export $(cat .swarm.dev.env) && docker stack deploy -c ./docker-swarm.dev.yml dev
