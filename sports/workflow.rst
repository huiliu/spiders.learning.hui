爬虫 - 计算球员比赛表现得分
****************************

scrapy爬虫目录结构为：

.. code-block:: text

    .
    ├── scrapy.cfg
    ├── scrapy_fixtures.sh
    ├── scrapy_live.sh
    ├── scrapy_players.sh
    ├── sports
    │   ├── __init__.py
    │   ├── items.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── 2017.py
    │       ├── addons
    │       │   ├── calc_core.py
    │       │   ├── calc.py
    │       │   ├── clubs.py
    │       │   ├── common.py
    │       │   ├── config.ini
    │       │   ├── db_match_schedule.xml
    │       │   ├── enum.py
    │       │   ├── export_team.py
    │       │   ├── fixtures.py
    │       │   ├── __init__.py
    │       │   ├── player.py
    │       │   ├── PlayerTemplate_table.xml
    │       │   ├── rules.py
    │       │   ├── score_rules.py
    │       │   └── TeamTemplate_table.xml
    │       ├── fixtures.py
    │       ├── images.py
    │       ├── __init__.py
    │       ├── live.py
    │       ├── PersistMongo.py
    │       ├── players.py
    │       └── premier_league.py
    └── workflow.rst


其中"*sports/spiders*"目录下是爬虫的源码。当前有五个spider:

1.  **2017**        从"腾讯看直播"抓取赛程(未使用), "sports/spiders/2017.py"
2.  **fixtures**    抓取赛程, "sports/spiders/fixtures.py"
3.  **images**      下载头像, "sports/spiders/images.py"
4.  **live**        抓取赛事详细统计, "sports/spiders/live.py"
5.  **players**     抓取球员数据输出球员模板表, "sports/spiders/players.py"
6.  **pulselive**   从英超官网抓取赛程(未使用), "sports/spiders/premier_league.py"

另包含一些后期处理辅助脚本：

1.  **scrapy_fixtures.sh**  抓取赛程信息(中超，亚冠，英超，西甲，法甲，德甲，意甲，欧冠，欧联)
2.  **scrapy_live.sh**      抓取比赛的详细数据，需要比赛的赛事ID
3.  **scrapy_players.sh**   抓取球员信息(依据赛程中的俱乐部ID查找某个俱乐部的球员)


1.  **sports/spiders/addons/fixtures.py**         将爬虫抓取的赛程数据导出为XML模板表
2.  **sports/spiders/addons/score_rules.py**      定义了策划给出的球员各表现参数的得分值
3.  **sports/spiders/addons/rules.py**            球员得分计算公式(策划)的实现
4.  **sports/spiders/addons/calc.py**             根据腾讯图文直播数据计算某场比赛球员的得分。当前实现依赖于腾讯数据，可以重新实现一个更为通用的形式。

命令："``scrapy crawl fixtures(spider name)``\ 即可运行爬虫。

spider抓取的数据都被存储在\ **10.1.0.6**\ 上的\ ``MongoDB``\ 中。

.. note::

    运行爬虫进行数据抓取前，请先备份MongoDB

    ``mongoexport -h 10.1.0.6 -d football -c xxxx -o football.json``

抓取赛程信息
===============
使用spider ``fixtures``\ 可以抓取相关赛季的赛程。

::

    scrapy crawl fixtures

**此爬虫通常只在有新的赛程数据时才运行**\ 。

URL分析
--------
腾讯网站上赛程的URL为：\
``http://soccerdata.sports.qq.com/s/fixture/list.action?time=%s&compid=%d``

其中：
1.  ``time``\ 为赛季第一场比赛开始的日志，格式为：\ ``YYYY-MM-DD``\ ，如：\ *2016-03-24*

2.  ``compid``\ 为赛事类型ID。当前网站定义为（此值由被爬网站定义的，勿猜）：\
    8: 英超；22: 德甲；21：意甲；23 ：西甲；24：法甲；208：中超；5：欧冠；\
    6：欧联；605：亚冠

抓取新赛季赛程
---------------
编辑"**scrapy_fixtures.sh**"，设置好联赛开赛日期，运行脚本即可。

.. note::

    1.  第一次可能不会抓取到整个赛季的数据，因为腾讯没有全部更新。
    2.  注意将不需要的URL删除，以免抓到不需要的数据。

抓取的数据会存放在MongoDB的"*football/fixtures*"和"*football/clubs*"中。

抓取到的赛程信息中包含有\ ``赛季``\ 、 ``日期``\ 等信息可以过滤查找。

导出赛程数据
-------------
使用脚本"**sports/spiders/addons/fixtures.py**"将mongo中的赛程数据导出为XML文件\
"**赛程模板表**"，最后由"*赛程模板表导入工具*"(见SVN中的服务端工具)将赛程信息导\
入到服务端数据库中。如果

1.  赛程发生调整(少量直接修改XML模板表更方便)
2.  得到比赛结果

可以直接修改"**赛程模板表**"，然后将其导入即可，不必重新抓取数据。

抓取到新的赛程数据后，由服务端工具将其导入至数据中。

抓取比赛统计
=============
爬虫"**live**"用于抓取赛事详细统计，其中包含文字直播信息（可以挖掘一下）。当\
前代码，从赛程表"*football/fixtures*"中提取所有赛事的唯一ID，构造出查询URL，\
然后抓取赛事详细统计，然后保存至"*football/mid*"中。

URL分析
--------
腾讯网站的比赛图文直播URL为：
`http://soccerdata.sports.qq.com/s/live.action?mid=810614`

其中：

1.  *mid*\ 值为赛事ID，赛程表中的ID值

抓取新的比赛统计
------------------
爬虫"**live**"的源码为"*sports/spiders/live.py*"，看一下\ ``QqLiveSpider``\ 初
始化代码：

.. code-block:: python

    class QqLiveSpider(scrapy.Spider):
        name = "live"
        allowed_domains = ["soccerdata.sports.qq.com"]
        start_urls = (
            'http://soccerdata.sports.qq.com/s/live.action?mid=810614',
        )
        # URL模板，%d比赛ID
        url_tpl = 'http://soccerdata.sports.qq.com/s/live.action?mid=%s'
    
        def __init__(self, mid=None):
            urls = []
            if mid:
                # 查询指定的比赛
                urls.append(self.url_tpl % str(mid))
                #self.start_urls = set([url])
            else:
                # 默认查询赛程表中昨天(以运行脚本所在机器时间)的比赛
                now = datetime.datetime.today()
                delta_day = datetime.timedelta(1)
    
                condition = dict()
                condition['date'] = (now - delta_day).strftime("%Y-%m-%d")
    
                Filter = {'_id': 0, 'id': 1}
                for match in db.get_record(config['fixture'], condition, Filter):
                    #if match['id'] not in match_ids:
                    urls.append(self.url_tpl % match['id'])
    
            self.start_urls = set(urls)
    
默认"**live**"爬虫会抓取昨天比赛的详细数据。如果指定比赛ID，则会抓取指定比赛的\
详细数据:"``scrapy crawl live -a mid=847885``"

现在可以使用脚本"``scrapy_live.sh``"同时完成抓取和计算得分的任务。

计算球员得分
-------------
根据获取的比赛详细统计信息，计算球员相应的得分，利用脚本"**addons/calc.py**"即\
可完成，球员的得分信息存放在"*football/player_score*"中，球员信息存放在\
"*football/player_template*"中。

脚本"**sports/spiders/addons/calc.py**"可以有多个参数控制其行为：

.. code-block:: text

    [liuhui@viiv spiders]$ python calc.py -h
    usage: calc.py [-h] [--host HOST] [-p PORT] [-d DATABASE] [-c COLLECTION]
                   [-t TYPE] --tpl TPL [-r RULE] [-o OUTPUT]
                   mid
    
    计算球员得分
    
    positional arguments:
      mid                   赛事ID (default: 默认计算所有)
    
    optional arguments:
      -h, --help            show this help message and exit
      --host HOST           Mongo服务器IP. default: 10.1.0.6
      -p PORT, --port PORT  Mongo服务器端口. default: 27017
      -d DATABASE, --database DATABASE
                            数据库名. default: football
      -c COLLECTION, --collection COLLECTION
                            collection名. default: mid
      -t TYPE, --type TYPE  运动类型.(1:足球;2:篮球) default: 1
      --tpl TPL             球员模板表 default: PlayerTemplate_table.xml
      -r RULE, --rule RULE  得分计算规则
      -o OUTPUT, --output OUTPUT
                            输入到文件. default: db_player_matchscore.xml

.. code-block:: bash

    sports/spiders/addons/calc.py --tpl PlayerTemplate_table.xml 847885

将计算比赛ID为8847885的参赛球员得分，输出到847885.xml

抓取赛事详细统计信息，并计算得到球员得分，将相关文件(847885.xml)交由服务端导\
入至数据库。

获取图像
=========
爬虫"**images**"会从\ ``球员信息模板(player_template), 俱乐部信息表(clusb)``\
中读取球员唯一ID，俱乐部唯一ID构造URL下载图像。

此爬虫通常只须要运行一次，如果数据缺失，直接从网站下载。甚至不需要此数据，伪造\
HTTP请求头，直接从腾讯网站加载。
