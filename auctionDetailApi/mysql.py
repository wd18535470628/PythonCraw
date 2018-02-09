#coding=utf-8
import MySQLdb
import time

class Mysql:
    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('192.168.1.189', 'root', '123456', 'jd_crawler')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def insertTbData(self,cache_table,table, my_dict):
        try:
            self.db.set_character_set('utf8')
            sqlCount = 'select count(*) from '+cache_table+' where auctionId='+ my_dict['auction_id']
            self.cur.execute(sqlCount)
            count_id = self.cur._rows[0][0]
            if count_id == 0:
                sqlAche = 'insert into ' + cache_table + ' ( auctionId) value (' + my_dict['auction_id'] + ')'
                sqlInfo = 'INSERT INTO ' + table +' (' + ', '.join(my_dict.keys()) +  ') value ("'+ '"," '.join(my_dict.values()) +'")'
                print sqlInfo
                try:
                    self.cur.execute(sqlAche)
                    result = self.cur.execute(sqlInfo)
                    insert_id = self.db.insert_id()
                    self.db.commit()
                    # 判断是否执行成功
                    if result:
                        return insert_id
                    else:
                        return 0
                except MySQLdb.Error, e:
                    # 发生错误时回滚
                    self.db.rollback()
                    # 主键唯一，无法插入
                    if "key 'PRIMARY'" in e.args[1]:
                        print self.getCurrentTime(), "数据已存在，未插入数据"
                    else:
                        print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
            else:
                sqlUpdate = 'update %s set '%(table)
                for col in my_dict.keys():
                    sqlUpdate = sqlUpdate + col + '="' + my_dict[col] + '",'
                sqlUpdate = sqlUpdate[:-1] + 'where auction_id = ' + my_dict['auction_id']
                print sqlUpdate
                result = self.cur.execute(sqlUpdate)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def insertJdData(self,cache_table,table, my_dict):
        try:
            self.db.set_character_set('utf8')
            sqlCount = 'select count(*) from '+cache_table+' where auction_id='+ my_dict['id']
            self.cur.execute(sqlCount)
            count_id = self.cur._rows[0][0]
            if count_id == 0:
                sqlAche = 'insert into ' + cache_table + ' ( auction_id) value (' + my_dict['id'] + ')'
                sqlInfo = 'INSERT INTO ' + table +' (' + ', '.join(my_dict.keys()) +  ') value ('+ ','.join(my_dict.values()) +')'
                print sqlInfo
                try:
                    self.cur.execute(sqlAche)
                    result = self.cur.execute(sqlInfo)
                    insert_id = self.db.insert_id()
                    self.db.commit()
                    # 判断是否执行成功
                    if result:
                        return insert_id
                    else:
                        return 0
                except MySQLdb.Error, e:
                    # 发生错误时回滚
                    self.db.rollback()
                    # 主键唯一，无法插入
                    if "key 'PRIMARY'" in e.args[1]:
                        print self.getCurrentTime(), "数据已存在，未插入数据"
                    else:
                        print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
            else:
                sqlUpdate = 'update %s set '%(table)
                for col in my_dict.keys():
                    sqlUpdate = sqlUpdate + col + '="' + my_dict[col] + '",'
                sqlUpdate = sqlUpdate[:-1] + ' where id = ' + my_dict['id']
                print sqlUpdate
                result = self.cur.execute(sqlUpdate)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])