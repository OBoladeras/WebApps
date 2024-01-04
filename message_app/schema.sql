/*

docker run -d --name mysql_messages -e MYSQL_ROOT_PASSWORD=123 -p 3306:3306 mysql
docker exec -it mysql_messages mysql -uroot -p

*/

DROP DATABASE IF EXISTS messageDatabase;
CREATE DATABASE messageDatabase;
USE messageDatabase;

CREATE TABLE user (
    id VARCHAR(20) NOT NULL UNIQUE,

    username VARCHAR(255) NOT NULL,
    public_key VARCHAR(3) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    status VARCHAR(255),
    last_seen TIMESTAMP,

    PRIMARY KEY (id)
);

CREATE TABLE contacts (
    id VARCHAR(20) NOT NULL,
    user1 VARCHAR(20) NOT NULL,
    user2 VARCHAR(20) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (user1) REFERENCES user(id),
    FOREIGN KEY (user2) REFERENCES user(id)
);

CREATE TABLE messages (
    id INT NOT NULL AUTO_INCREMENT,
    sender VARCHAR(20) NOT NULL,
    receiver VARCHAR(20) NOT NULL,
    message VARCHAR(255) NOT NULL,
    time TIMESTAMP NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (sender) REFERENCES user(id),
    FOREIGN KEY (receiver) REFERENCES user(id)
);

commit;
