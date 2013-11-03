
USE enviroment_spider
CREATE TABLE IF NOT EXISTS ifengHeadline (
                                            id      INT AUTO_INCREMENT,  -- 编号
                                            title   CHAR(255)   NOT NULL, -- 新闻标题
                                            href    CHAR(255)   NOT NULL,   -- 相应的连接
                                            uptime  DATETIME,  -- 插入时间，非网站发布时间
                                            pri     TINYINT(1)  UNSIGNED,    -- 优先级,重要性
                                            content TEXT    DEFAULT NULL,
                                            PRIMARY KEY (id, title)
                                            )
