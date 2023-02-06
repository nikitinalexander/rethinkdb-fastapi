# rethinkdb-fastapi

docker build -t rethinkdb-fastapi .

docker tag rethinkdb-fastapi alexandernikitin/rethinkdb-fastapi

docker push alexandernikitin/rethinkdb-fastapi

docker compose up -d

docker compose down