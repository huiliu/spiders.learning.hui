计算球员比赛表现得分
*********************

scrapy爬虫目录结构为：

.. code-block:: text

    ├── addons
    │   ├── calc.py
    │   ├── config.ini
    │   ├── export_fixtures.py
    │   ├── rules.py
    │   └── score_rules.py
    ├── scrapy.cfg
    └── sports
        ├── __init__.py
        ├── items.py
        ├── pipelines.py
        ├── settings.py
        └── spiders
            ├── 2017.py
            ├── calc.py
            ├── fixtures.py
            ├── images.py
            ├── __init__.py
            ├── live.py
            ├── PersistMongo.py
            ├── premier_league.py
            └── rules.py

其中"*sports/spiders*"目录下是爬虫的源码。当前有五个spider:

1.  **2017**        从腾讯“看直播”来抓取赛程
2.  **fixtures**    抓取赛程
3.  **images**      下载头像
4.  **live**        抓取赛事详细统计
5.  **pulselive**   从英超官网抓取赛程

另包含一些后期处理辅助脚本：

1.  **export_fixtures.py**  将爬虫抓取的赛程数据导出为XML模板表
2.  **score_rules.py**      定义了策划给出的球员各表现参数的得分值
3.  **rules.py**            球员得分计算公式的实现
4.  **calc.py**             根据腾讯图文直播数据计算某场比赛球员的得分。当前实\
                            现依赖于腾讯数据，可以重新实现一个更为通用的形式。

命令："``scrapy crawl fixtures(spider name)``\ 即可运行爬虫。

spider抓取的数据都被存储在\ **10.1.0.6**\ 上的\ ``MongoDB``\ 中。

.. warnning::

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
1.  ``time``\ 为赛季第一场比赛开始的日志，格式为：\ ``YYYY-MM-DD``\ ，如：\
    *2016-03-24*\ 
2.  ``compid``\ 为赛事类型ID。当前网站定义为（此值由被爬网站定义的，勿猜）：\
    8: 英超；22: 德甲；21：意甲；23 ：西甲；24：法甲；208：中超；5：欧冠；\
    6：欧联；605：亚冠

攫取新赛季赛程
---------------
准备抓取赛季赛程前，先根据实际情况修改爬虫相关参数。爬虫"**fixtures**"的源文件\
为"*fixtures.py*"，打开之前可以看到一系列的URL列表，将不同赛事本赛季第一场比赛\
开始日期修改即可运行爬虫"``scrapy crawl fixtures``"抓取数据。

.. note::

    1.  第一次可能不会抓取到整个赛季的数据，因为腾讯没有全部更新。
    2.  注意将不需要的URL删除，以免抓到不需要的数据。

抓取的数据会存放在"*football/fixtures*"和"*football/clubs*"中。

抓取到的赛程信息中包含有\ ``赛季``\ 、 ``日期``\ 等信息可以过滤查找。

导出赛程数据
-------------
使用脚本"**addons/export_fixtures.py**"将mongo中的赛程数据导出为XML文件\
"**赛程模板表**"，最后由"*赛程模板表导入工具*"(见SVN中的服务端工具)将赛程信息导\
入到服务端数据库中。如果

1.  赛程发生调整(少量直接修改XML模板表更方便)
2.  得到比赛结果

可以直接修改"**赛程模板表**"，然后将其导入即可，不必重新抓取数据。

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
    
        def __init__(self):
            urls = []
            match_ids = db.get_downloaded_match_id()
            for match in db.get_fixture_match_id({}):
                if match['id'] not in match_ids:
                    urls.append(self.url_tpl % match['id'])
    
            return
            self.start_urls = set(urls)
    
初始化时，爬虫从赛程表中读取记录，根据赛程ID构造新的URL，然后交给爬虫抓取数据。
所以日常运行中，通过一次只有几场比赛产生结果，所以没有必要去抓取所有，只需要手
动构造所需比赛的URL，交给爬虫抓取即可。

计算球员得分
-------------
根据获取的比赛详细统计信息，计算球员相应的得分，利用脚本"**addons/calc.py**"即\
可完成，球员的得分信息存放在"*football/player_score*"中，球员信息存放在\
"*football/player_template*"中。

脚本"**addons/calc.py**"可以有多个参数控制其行为（有部分功能待扩展）：

.. code-block:: text

    [liuhui@viiv spiders]$ python calc.py -h
    usage: calc.py [-h] [-t TYPE] [-r RULE] [mid]
    
    计算球员得分
    
    positional arguments:
      mid                   赛事ID (default: 默认计算所有)
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TYPE, --type TYPE  运动类型.(1:足球;2:篮球)
      -r RULE, --rule RULE  得分计算规则

获取图像
=========
爬虫"**images**"会从\ ``球员信息模板(player_template), 俱乐部信息表(clusb)``\
中读取球员唯一ID，俱乐部唯一ID构造URL下载图像。

此爬虫通常只须要运行一次，如果数据缺失，直接从网站下载。甚至不需要此数据，伪造\
HTTP请求头，直接从腾讯网站加载。
