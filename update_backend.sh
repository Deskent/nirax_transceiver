if [ $1 ];
then VERSION=$1
else VERSION=latest
fi

REPOSITORY_NAME=gendocs.nirax.ru:5055/nirax
STACK=transceiver
PROJECT_NAME=nirax_transceiver

docker pull $REPOSITORY_NAME/$PROJECT_NAME:$VERSION
docker service update --image $REPOSITORY_NAME/$PROJECT_NAME:$VERSION ${STACK}_${PROJECT_NAME}
