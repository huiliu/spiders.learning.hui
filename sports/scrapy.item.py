import scrapy

                                                                                
class FootballTeamNormalItem(scrapy.Item):                                      
    # 常规数据
    c_type = scrapy.Field()     # 比赛类型
    result = scrapy.Field()     # 赛季战况（胜/负/平）
    jingqiu = scrapy.Field()    # 总进球数
    shiqiu  = scrapy.Field()    # 失球数
    chuanqiu = scrapy.Field()   # 传球数
    redcard = scrapy.Field()    # 红牌
    yellowcard = scrapy.Field()     # 黄牌
    zhugong = scrapy.Field()      # 助攻
    qiangduan   = scrapy.Field()    # 抢断
    yuewei  = scrapy.Field()        # 越位
    fangui  = scrapy.Field()    # 犯规
    JiaoQiu = scrapy.Field()    # 角球
    RenYiQiu = scrapy.Field()   # 任意球
                                                                                
                                                                                
#class FootballTeamAttackItem(scrapy.Item):                                      
    # 进攻数据
    c_type = scrapy.Field()     # 比赛类型
    touqiu  = scrapy.Field()    # 头球得分
    renyiqiu = scrapy.Field()   # 任意球得分
    shezhen = scrapy.Field()    # 射正
    shemen = scrapy.Field()     # 射门
    menkuang = scrapy.Field()   # 击中门框
    chuanzhong = scrapy.Field()    # 传中
    guanjianchuanqiu    = scrapy.Field()    # 关键传球
    guoren = scrapy.Field()     # 过人
                                                                                
#class FootboolDefenseItem(scrapy.Item):                                         
    # 防守数据
    c_type = scrapy.Field()     # 比赛类型
    lanjie = scrapy.Field()     # 拦截
    jiewei = scrapy.Field()     # 解围
    touqiujiewei = scrapy.Field()   # 头球解围
    houChangJieWei = scrapy.Field() # 后场解围
    TouQiuZhengDing = scrapy.Field()    # 头球争顶成功
    HuiQiang = scrapy.Field() # 回抢
    WulongQiu = scrapy.Field() # 乌龙球
                                                                                
#class FootballNo1Item(scrapy.item):                                             
    # 守门员数据
    ChuChang = scrapy.Field()   # 出场/首发
    ChuChangTime = scrapy.Field()   # 出场时间
    ShiQiu = scrapy.Field()     # 失球数
    ChuQiu = scrapy.Field()     # 角球数
    ChuJi  = scrapy.Field()     # 出击
    PuJiu  = scrapy.Field()     # 扑救
    PuDian = scrapy.Field()     # 扑点球
    PuBiJinQiu = scrapy.Field() # 扑改进球
    Ying1v1 = scrapy.Field()    # 赢得1v1
    FanGui = scrapy.Field()     # 犯规
    red_yellow_card = scrapy.Field()    # 红黄牌
