CREATE DATABASE IF NOT EXISTS enviroment_spider DEFAULT CHARACTER SET 'utf8';

USE enviroment_spider

CREATE TABLE IF NOT EXISTS airq (
                                    id              integer,
                                    city_name       CHAR(25),
                                    date            Date,
                                    pollution_id    Integer,
                                    contamination   CHAR(25),
                                    qLevel          CHAR(6),
                                    qState          CHAR(25)
                                );

GRANT ALL PRIVILEGES ON enviroment_spider.* TO 'spider'@'localhost' IDENTIFIED BY 'spider';
FLUSH PRIVILEGES;
