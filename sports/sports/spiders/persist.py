#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import datetime

class PersistentObj:
    def __init__(self):
        self.conn = None
        self.cursor = None
        pass

    def __del__(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def _init(self):
        self.conn = MySQLdb.connect(
                host='10.1.0.6',
                user='viivgame',
                passwd='viivgame',
                charset='utf8',
                db='sports'
                )
        self.cursor = self.conn.cursor()

    def _check_curson(self):
        if not self.cursor:
            self._init()
            assert self.cursor

    def InsertPlayerInfo(self, data):
        self._check_curson()
        SQL_Template = """INSERT INTO players (
                            uuid,
                            name,
                            position,
                            club,
                            heigh,
                            birthday,
                            weight,
                            country,
                            number,
                            url
                        ) VALUES (
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            %d,
                            '%s'
                        )"""
        try:
            sql = SQL_Template % (
                                    data['uuid'],
                                    data['name'],
                                    data['position'],
                                    data['club'],
                                    data['heigh'],
                                    data['birthday'],
                                    data['weight'],
                                    data['country'],
                                    data['number'],
                                    data['url'],
                                )
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(' '.join(data.items))


    def InsertTeamSeasonSummary(self, name, season, data, url):
        self._check_curson()
        InsertSql = """insert into team_season_summary (
                        name,
                        season,
                        type,
                        result,
                        jinqiu,
                        shiqiu,
                        chuanqiu,
                        redcard,
                        yellowcard,
                        zhugong,
                        qiangduan,
                        yuewei,
                        fangui,
                        touqiu,
                        renyiqiudefen,
                        shezheng,
                        shemen,
                        jizhongmenkuang,
                        chuanzhong,
                        guanjianchuanqiu,
                        guoren,
                        lanjie,
                        jiewei,
                        touqiujiewei,
                        houchangjiewei,
                        menxianjiewei,
                        touqiuzhengding,
                        huiqiang,
                        wulongqiu,
                        url
                        ) VALUES (
                        '%s',
                        %d,
                        '%s',
                        '%s',
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        '%s'
                    )"""
        for records in data:
            try:
                row = InsertSql % (
                        name,
                        int(season),
                        records[0],
                        records[1],
                        int(records[2]),
                        int(records[3]),
                        int(records[4]),
                        int(records[5]),
                        int(records[6]),
                        int(records[7]),
                        int(records[8]),
                        int(records[9]),
                        int(records[10]),
                        int(records[11]),
                        int(records[12]),
                        int(records[13]),
                        int(records[14]),
                        int(records[15]),
                        int(records[16]),
                        int(records[17]),
                        int(records[18]),
                        int(records[19]),
                        int(records[20]),
                        int(records[21]),
                        int(records[22]),
                        int(records[23]),
                        int(records[24]),
                        int(records[25]),
                        int(records[26]),
                        url
                        )
                self.cursor.execute(row)
            except Exception as err:
                msg = u'出错了！\t%s %s %s %s\n' % (name, season, ' '.join(records), url)
                print(err)
                print(msg)
        self.conn.commit()

    def InsertTeamSeasonDetailData(self, name, season, data, url):
        self._check_curson()
        InsertSql = """INSERT INTO team_season_detail_summary (
                        name,
                        season,
                        timestamp,
                        type,
                        team_a,
                        result,
                        team_b,
                        jinqiu,
                        zhugong,
                        jiaoqiu,
                        renyiqiu,
                        chuanqiu,
                        qiangduan,
                        yuewei,
                        fangui,
                        redcard,
                        yellowcard,
                        touqiu,
                        renyiqiudefen,
                        shezheng,
                        shemen,
                        jizhongmenkuang,
                        chuanzhong,
                        guanjianchuanqiu,
                        guoren,
                        lanjie,
                        jiewei,
                        touqiujiewei,
                        houchangjiewei,
                        menxianjiewei,
                        touqiuzhengding,
                        huiqiang,
                        wulongqiu,
                        url
                    ) VALUES (
                        '%s',
                        %d,
                        %d,
                        '%s',
                        '%s',
                        '%s',
                        '%s',
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        %d,
                        '%s'
                    )"""
        for records in data:
            assert len(records) == 31
            try:
                sql = InsertSql % (
                        name,
                        int(season),
                        int(datetime.datetime.strptime(records[0], '%Y-%m-%d %H:%M').strftime('%s')),
                        records[1],
                        records[2],
                        records[3],
                        records[4],
                        int(records[5]),
                        int(records[6]),
                        int(records[7]),
                        int(records[8]),
                        int(records[9]),
                        int(records[10]),
                        int(records[11]),
                        int(records[12]),
                        int(records[13]),
                        int(records[14]),
                        int(records[15]),
                        int(records[16]),
                        int(records[17]),
                        int(records[18]),
                        int(records[19]),
                        int(records[20]),
                        int(records[21]),
                        int(records[22]),
                        int(records[23]),
                        int(records[24]),
                        int(records[25]),
                        int(records[26]),
                        int(records[27]),
                        int(records[28]),
                        int(records[29]),
                        int(records[30]),
                        url
                        )
                self.cursor.execute(sql)
            except Exception as err:
                msg = u'出错了！\t%s %s %s %s\n' % (name, season, ' '.join(records), url)
                print(err)
                print(msg)
        self.conn.commit()

    def InsertPlayerSeasonSummary(self, info, data):
        self._check_curson()
        SQL_Template = """INSERT INTO player_season_summary(
                            uuid,
                            season,
                            type,
                            position,
                            chuchang,
                            shoufa,
                            chuchangtime,
                            jinqiu,
                            chuanqiu,
                            redcard,
                            yellowcard,
                            zhugong,
                            qiangduan,
                            yuewei,
                            fangui,
                            shemen,
                            shezheng,
                            jizhongmenkuang,
                            zhunquechuanzhong,
                            chuanzhong,
                            guoren,
                            beiqinfan,
                            yingdedianqiu,
                            lanjie,
                            jiewei,
                            touqiujiewei,
                            houchangjiewei,
                            menxianjiewei,
                            touqiuzhengding,
                            huiqiang,
                            wulongqiu,
                            url
                        ) VALUES (
                            '%s',
                            %d,
                            '%s',
                            '%s',
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            '%s'
                        )"""
        for records in data:
            try:
                chuchang = records[2].split('/')
                sql = SQL_Template % (
                    info['uuid'],
                    info['season'],
                    records[0],
                    records[1],
                    int(chuchang[0]),
                    int(chuchang[1]),
                    int(records[3]),
                    int(records[4]),
                    int(records[5]),
                    int(records[6]),
                    int(records[7]),
                    int(records[8]),
                    int(records[9]),
                    int(records[10]),
                    int(records[11]),
                    int(records[12]),
                    int(records[13]),
                    int(records[14]),
                    int(records[15]),
                    int(records[16]),
                    int(records[17]),
                    int(records[18]),
                    int(records[19]),
                    int(records[20]),
                    int(records[21]),
                    int(records[22]),
                    int(records[23]),
                    int(records[24]),
                    int(records[25]),
                    int(records[26]),
                    int(records[27]),
                    info['url']
                    )
                self.cursor.execute(sql)
            except Exception as err:
                print(err)
                print(records)
                print(' '.join(records))
        self.conn.commit()

    def InsertPlayerSeasonDetailData(self, info, data):
        self._check_curson()
        SQL_Template = """INSERT INTO player_season_detail_summary (
                            uuid,
                            season,
                            timestamp,
                            type,
                            team_a,
                            result,
                            team_b,
                            isshoufa,
                            chuchangtime,
                            jinqiu,
                            zhugong,
                            chuanqiu,
                            qiangduan,
                            yuewei,
                            fangui,
                            redcard,
                            yellowcard,
                            shemen,
                            shezheng,
                            jizhongmenkuang,
                            zhunquechuanzhong,
                            chuanzhong,
                            guoren,
                            beiqinfan,
                            lanjie,
                            jiewei,
                            touqiujiewei,
                            houchangjiewei,
                            menxianjiewei,
                            touqiuzhengding,
                            huiqiang,
                            url
                        ) VALUES (
                            '%s',
                            %d,
                            %d,
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            '%s'
                        )"""

        for records in data:
            try:
                sql = SQL_Template % (
                        info['uuid'],
                        info['season'],
                        int(datetime.datetime.strptime(records[0], '%Y-%m-%d %H:%M').strftime('%s')),
                        records[1],
                        records[2],
                        records[3],
                        records[4],
                        records[5],
                        int(records[6]),
                        int(records[7]),
                        int(records[8]),
                        int(records[9]),
                        int(records[10]),
                        int(records[11]),
                        int(records[12]),
                        int(records[13]),
                        int(records[14]),
                        int(records[15]),
                        int(records[16]),
                        int(records[17]),
                        int(records[18]),
                        int(records[19]),
                        int(records[20]),
                        int(records[21]),
                        int(records[22]),
                        int(records[23]),
                        int(records[24]),
                        int(records[25]),
                        int(records[26]),
                        int(records[27]),
                        int(records[28]),
                        info['url']
                        )

                self.cursor.execute(sql)
            except Exception as err:
                print(err)
                print(' '.join(records))
        self.conn.commit()

    def InsertGoalkeeperSeasonDetailData(self, info, data):
        """
        守门员赛季详细数据
        """
        self._check_curson()
        SQL_Template = """INSERT INTO goalkeeper_season_detail_summary (
                            uuid,
                            season,
                            timestamp,
                            type,
                            team_a,
                            result,
                            team_b,
                            isshoufa,
                            chuchangshijian,
                            shiqiu,
                            chuqiu,
                            chuji,
                            pujiu,
                            pudianqiu,
                            pubijinqiu,
                            fangui,
                            redcard,
                            yellowcard,
                            url
                        ) VALUES (
                            '%s',
                            %d,
                            %d,
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            '%s',
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            '%s'
                        )"""

        for records in data:
            try:
                cards = records[14].split('/')
                sql = SQL_Template % (
                        info['uuid'],
                        info['season'],
                        int(datetime.datetime.strptime(records[0], '%Y-%m-%d %H:%M').strftime('%s')),
                        records[1],
                        records[2],
                        records[3],
                        records[4],
                        records[5],
                        int(records[6]),
                        int(records[7]),
                        int(records[8]),
                        int(records[9]),
                        int(records[10]),
                        int(records[11]),
                        int(records[12]),
                        int(records[13]),
                        int(cards[0]),
                        int(cards[1]),
                        info['url']
                        )

                self.cursor.execute(sql)
            except Exception as err:
                print(err)
                print(records)
                print(' '.join(records))
        self.conn.commit()

    def InsertGoalkeeperSeasonSummary(self, info, data):
        """
        守门员赛季总数据
        """

        self._check_curson()
        SQL_Template = """INSERT INTO goalkeeper_season_summary (
                            uuid,
                            season,
                            type,
                            position,
                            shoufa,
                            chuchang,
                            chuchangshijian,
                            shiqiu,
                            chuqiu,
                            chuji,
                            pujiu,
                            pudianqiu,
                            pubijinqiu,
                            fangui,
                            redcard,
                            yellowcard,
                            url
                        ) VALUES (
                            '%s',
                            %d,
                            '%s',
                            '%s',
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            %d,
                            '%s'
                        )"""

        #print(info)
        #print(data)
        for records in data:
            try:
                chuchang = records[2].split('/')
                cards = records[11].split('/')
                sql = SQL_Template % (
                        info['uuid'],
                        info['season'],
                        records[0],
                        records[1],
                        int(chuchang[0]),
                        int(chuchang[1]),
                        int(records[3]),
                        int(records[4]),
                        int(records[5]),
                        int(records[6]),
                        int(records[7]),
                        int(records[8]),
                        int(records[9]),
                        int(records[10]),
                        int(cards[0]),
                        int(cards[1]),
                        info['url']
                        )

                self.cursor.execute(sql)
            except Exception as err:
                print(err)
                print(' '.join(records))
        self.conn.commit()

    def InsertComptitionSchedules(self, data):
        """
        插入赛程信息
        """
        self._check_curson()
        SQL_Template = """INSERT INTO competition_schedules (
                                uuid,
                                type,
                                rand,
                                start_time,
                                team_a,
                                score,
                                team_b,
                                address,
                                url
                        ) VALUES (
                                '%s',
                                '%s',
                                %d,
                                %d,
                                '%s',
                                '%s',
                                '%s',
                                '%s',
                                '%s'
                        )"""
        for record in data:
            try:
                sql = SQL_Template % (
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5],
                        record[6],
                        record[7],
                        record[8]
                        )
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                print(sql)
                print(record)
                #print(' '.join(record))
        self.conn.commit()
