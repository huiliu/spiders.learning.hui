CREATE DATABASE IF NOT EXISTS spider DEFAULT CHARACTER SET 'utf8';
USE spider

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

CREATE TABLE IF NOT EXISTS ifengHeadline (
                                            id      INT AUTO_INCREMENT,  -- 编号
                                            title   CHAR(255)   NOT NULL, -- 新闻标题
                                            href    CHAR(255)   NOT NULL,   -- 相应的连接
                                            uptime  DATETIME,  -- 插入时间，非网站发布时间
                                            pri     TINYINT(1)  UNSIGNED,   -- 优先级,重要性
                                            content TEXT    DEFAULT NULL,   -- 报道内容
                                            src     CHAR(25)    DEFAULT NULL,   -- 来源
                                            editor  CHAR(25)    DEFAULT NULL,   -- 编辑
                                            tags    CHAR(255)   DEFAULT NULL,   -- TAG
                                            PRIMARY KEY (id, title)
                                            );

GRANT ALL PRIVILEGES ON spider.* TO 'spider'@'localhost' IDENTIFIED BY 'spider';
FLUSH PRIVILEGES;
