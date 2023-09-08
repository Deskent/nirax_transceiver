if [ $1 ];
then VERSION=$1
else VERSION=latest
fi

REPOSITORY_NAME=gendocs.nirax.ru:5055/nirax
STACK=transceiver
PROJECT_NAME=nirax_transceiver

docker pull $REPOSITORY_NAME/$PROJECT_NAME:$VERSION

mkdir -p \
        logs

export $(cat .env) && docker stack deploy -c docker-swarm-${STACK}.yml ${STACK}
