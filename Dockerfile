FROM mariadb:11.6.1-rc

VOLUME [ "/var/lib/mysql", "/app/instance/upload_files" ]

ENTRYPOINT [ "/bin/bash" ]

EXPOSE 8000

RUN <<EOF
apt-get update
apt-get install -y iputils-ping
apt-get install netcat-traditional
apt-get install bash
EOF

RUN <<EOF
mariadb-install-db --user=mysql --ldata=/var/lib/mysql
EOF

RUN <<EOF
apt-get install -y git
apt-get install -y tmux
apt-get install -y python3.12-full
EOF

WORKDIR /app

COPY . ./

ARG DATABASE_NAME='web11'
ARG DATABASE_PASSWORD='1AaBbCc#'

RUN <<EOF
service mariadb start
mariadb -e "CREATE DATABASE ${DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mariadb ${DATABASE_NAME} < database/dump-web11.sql
mariadb -e "SET PASSWORD FOR 'root'@localhost = PASSWORD('${DATABASE_PASSWORD}');"
mariadb -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '${DATABASE_PASSWORD}' WITH GRANT OPTION;"
EOF

RUN chmod +x run.sh
RUN chmod +x podman_init_cmd.sh

#CMD [ "/usr/bin/python3.12", "-m", "http.server" ]
#CMD ["/usr/bin/nc", "-l", "8000"]
CMD ["./podman_init_cmd.sh"]