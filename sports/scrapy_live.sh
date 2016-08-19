#!/bin/bash

# ----------------------------------------------------------------------------
#
# 抓取赛事ID并计算球员得分
#
# ----------------------------------------------------------------------------

for mid in 847885 847886 847887 847888 847889 847890 847891 847892 853139 853140 853141 853142 853143 853144 853145 853146 853147 853148 855172 855173 855174 855175 855176 855177 855178 855179 855180 855181;
do
    # 抓取数据
    #scrapy crawl live -a mid=$mid
    # 计算得分
    ./sports/spiders/addons/calc.py --tpl PlayerTemplate_table.xml $mid
done
