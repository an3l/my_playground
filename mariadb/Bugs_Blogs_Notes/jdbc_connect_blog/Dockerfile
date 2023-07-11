ARG mariadb_version=latest
FROM "mariadb:$mariadb_version"

RUN apt-get update && \
    apt install openjdk-11-jdk-headless \
                mariadb-plugin-connect \
                mariadb-test-data \
                vim wget\
                libmariadb-java -y && \
    rm -rf /var/lib/apt/lists/*
