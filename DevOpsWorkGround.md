
# Old settings
```bash

# Run from downloads-mariadb-python3/docker
# It doesn't work from downloads-mariadb-python3, although there is `web` service
$ docker compose up web

$ docker images 
REPOSITORY                                          TAG         IMAGE ID       CREATED          SIZE
docker-web                                          latest      940c9bc87b3e   19 minutes ago   1.48GB
docker_web                                          latest      73f6b9e2c0c9   2 hours ago      1.48GB
python                                              latest      148bdd2c547f   4 days ago       921MB
```

Got containers (without web-1 running)
```bash
CONTAINER ID   IMAGE                                                        COMMAND                  CREATED             STATUS                         PORTS     NAMES
0ce735a63187   docker-web                                                   "/usr/src/app/entryp…"   About an hour ago   Exited (1) 43 minutes ago                docker-web-1
b7ef73cab6c0   mariadb:10.6                                                 "docker-entrypoint.s…"   About an hour ago   Exited (0) 4 seconds ago                 docker-db-1
b88b13090dc7   nginx:latest                                                 "/docker-entrypoint.…"   3 hours ago         Exited (0) About an hour ago             docker_nginx_1

```


# Update docker/app/Dockerfile to use multistage env
- Got the same error as above, so moved `docker-compose.yaml` file to parent folder

## Uuse docker buildx to speedup
```bash
$ docker buildx bake -f docker-bake.hcl local
[+] Building 60.3s (15/15) FINISHED                                                                                                                                                                          
 => [internal] load build definition from Dockerfile                                                                                                                                                    0.0s
 => => transferring dockerfile: 995B                                                                                                                                                                    0.0s
 => [internal] load .dockerignore                                                                                                                                                                       0.0s
 => => transferring context: 2B                                                                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:latest                                                                                                                                        0.5s
 => CACHED [builder 1/4] FROM docker.io/library/python:latest@sha256:7adb2f6d6b0fdaf2d3029c42b5a40833589f969c18728f5b5b126a61394848b6                                                                   0.0s
 => => resolve docker.io/library/python:latest@sha256:7adb2f6d6b0fdaf2d3029c42b5a40833589f969c18728f5b5b126a61394848b6                                                                                  0.0s
 => [internal] load build context                                                                                                                                                                       0.0s
 => => transferring context: 897B                                                                                                                                                                       0.0s
 => CACHED [stage-1 2/7] WORKDIR /usr/src/app                                                                                                                                                           0.0s
 => [builder 2/4] RUN apt-get update   && apt-get install -y --no-install-recommends     libgdal-dev                                                                                                   21.0s
 => [builder 3/4] COPY ./requirements.txt /tmp/requirements.txt                                                                                                                                         0.0s
 => [builder 4/4] RUN pip install --no-cache-dir -U pip   && pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r /tmp/requirements.txt                                                         29.2s 
 => [stage-1 3/7] COPY --from=builder /usr/src/app/wheels /wheels                                                                                                                                       0.1s 
 => [stage-1 4/7] RUN pip install --no-cache /wheels/*                                                                                                                                                  7.6s 
 => [stage-1 5/7] COPY . .                                                                                                                                                                              0.0s 
 => [stage-1 6/7] COPY ./entrypoint.sh /                                                                                                                                                                0.0s 
 => [stage-1 7/7] RUN chmod +x /entrypoint.sh                                                                                                                                                           0.4s 
 => exporting to image                                                                                                                                                                                  1.2s 
 => => exporting layers                                                                                                                                                                                 1.2s 
 => => writing image sha256:434590a248eaee839f73631239daeb45d3de069d96d0519bed6596e48c926f34                                                                                                            0.0s 
 => => naming to docker.io/library/local_app_patch 
```

Image is much smaller 1.03G vs (1.48GB+921MB)
```bash
$ docker images
REPOSITORY                                          TAG         IMAGE ID       CREATED          SIZE
local_app_patch                                     latest      434590a248ea   43 seconds ago   1.03GB

```
## Check docker compose config
Note I had to remove `./docker/app/.env` and move to root direcotry `.env` file

```bash
$ docker compose config db
name: downloads-mariadb-python3
services:
  db:
    environment:
      MARIADB_DATABASE: montyprogram_web
      MARIADB_MYSQL_LOCALHOST_USER: "1"
      MARIADB_PASSWORD: randompasswordgenerator
      MARIADB_ROOT_PASSWORD: "1234"
      MARIADB_USER: webuser
    healthcheck:
      test:
      - CMD
      - mariadb-admin
      - --password=1234
      - --protocol
      - tcp
      - ping
    image: mariadb:10.6
    logging:
      driver: journald
      options:
        tag: downloads-db
    networks:
      backend: null
    restart: always
    volumes:
    - type: bind
      source: /mnt/downloads-database/prod
      target: /var/lib/mysql
      bind:
        create_host_path: true
    - type: bind
      source: /home/anel/GitLab/downloads-mariadb-python3/db/config.prod
      target: /etc/mysql/conf.d
      bind:
        create_host_path: true
networks:
  backend:
    name: downloads-mariadb-python3_backend
  default:
    name: downloads-mariadb-python3_default
  frontend:
    name: downloads-mariadb-python3_frontend
volumes:
  staticfiles:
    name: downloads-mariadb-python3_staticfiles

```
## Errors from docker buildx
```bash
# This doesn't work, need a file to specify, will use default .yaml file
$ docker buildx bake local --load
[+] Building 0.0s (0/0)                                                                                                                                                                                      
WARNING: The "ENV_WEB_APP_PORT" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_WEB_LOG_TAG" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_NGINX_PORT" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_NGINX_LOG_TAG" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_TAG" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_PASSWORD" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_USER" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_DATABASE" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_MYSQL_LOCALHOST_USER" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_ROOT_PASSWORD" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_DATADIR" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_CONFIG" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_ROOT_PASSWORD" variable is not set. Defaulting to a blank string.
WARNING: The "ENV_MARIADB_LOG_TAG" variable is not set. Defaulting to a blank string.
ERROR: 2 error(s) decoding:

* error decoding 'Volumes[0]': invalid spec: :/var/lib/mysql: empty section between colons
* error decoding 'Volumes[1]': invalid spec: :/etc/mysql/conf.d: empty section between colons

```


Below command doesn't work correctly
```bash
$ docker buildx build --platform linux/amd64,linux/arm64 \
  --file Dockerfile \
  --tag docker_web:patch \
  .
```
