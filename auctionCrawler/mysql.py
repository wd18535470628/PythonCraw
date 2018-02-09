#coding=utf-8
import MySQLdb
import time

class Mysql:
    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('192.168.1.189', 'root', '123456', 'python2.1')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def dateFormat(self,msec):
        date = '"' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msec/1000)) + '"'
        return date
    def insertData(self, cache_table,table, my_dict,kind,user_id):
        try:
            self.db.set_character_set('utf8')
            for col in my_dict.keys():
                if type(col) == unicode:
                    col = col.decode("utf-8").encode("utf-8")
                    if col == 'end':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'start':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'itemUrl':
                        my_dict[col] = my_dict[col][2:]
            sqlCourt = 'select id from auction_court where user_id='+ user_id
            self.cur.execute(sqlCourt)
            court_id = self.cur._rows[0][0]
            sqlKind = 'select id from auction_kind where kind_desc="'+ kind+'"'
            self.cur.execute(sqlKind)
            kind_id = self.cur._rows[0][0]
            sqlCheck = 'SELECT count(*) FROM '+ cache_table +' where auction_id='+ str(my_dict['id'])
            self.cur.execute(sqlCheck)
            if self.cur._rows[0][0] == 0:
                #缓存表
                sqlAche = "INSERT INTO "+ cache_table +" (auction_id) value ("+ str(my_dict['id'])  +")"
                sqlInfo = "insert into %s (%s) VALUES (%s)" % (table, "auction_id,status,current_price,start,end,kind_id,court_id",str(my_dict['id'])+",'"+my_dict['status'].decode('utf-8').encode('utf-8')+"',"+ str(my_dict['currentPrice'])+","+ my_dict['start']+","+my_dict['end']+","+str(kind_id)+","+str(court_id))
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
                sqlUpdate = sqlUpdate + 'status="' + my_dict['status'] + '",current_price='+str(my_dict['currentPrice'])+',start='+ my_dict['start'] + ',end='+my_dict['end']+',kind_id='+ str(kind_id)+',court_id='+str(court_id)+' where id='+str(my_dict['id'])
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
    def insertDataProvince(self, cache_table,table, my_dict,kind,user_id,circile):
        try:
            self.db.set_character_set('utf8')
            for col in my_dict.keys():
                if type(col) == unicode:
                    col = col.decode("utf-8").encode("utf-8")
                    if col == 'end':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'start':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'itemUrl':
                        my_dict[col] = my_dict[col][2:]
            sqlCourt = 'select id from auction_court_province where user_id='+ user_id
            self.cur.execute(sqlCourt)
            court_id = self.cur._rows[0][0]
            sqlKind = 'select id from auction_kind where kind_desc="'+ kind+'"'
            self.cur.execute(sqlKind)
            kind_id = self.cur._rows[0][0]
            sqlCheck = 'SELECT count(*) FROM '+ cache_table +' where auction_id='+ str(my_dict['id'])
            self.cur.execute(sqlCheck)
            if self.cur._rows[0][0] == 0:
                #缓存表
                sqlAche = "INSERT INTO "+ cache_table +" (auction_id) value ("+ str(my_dict['id'])  +")"
                sqlInfo = "insert into %s (%s) VALUES (%s)" % (table, "auction_id,status,current_price,start,end,kind_id,court_id",str(my_dict['id'])+",'"+my_dict['status'].decode('utf-8').encode('utf-8')+"',"+ str(my_dict['currentPrice'])+","+ my_dict['start']+","+my_dict['end']+","+str(kind_id)+","+str(court_id))
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
                sqlUpdate = sqlUpdate + 'status="' + my_dict['status'] + '",current_price='+str(my_dict['currentPrice'])+',start='+ my_dict['start'] + ',end='+my_dict['end']+',kind_id='+ str(kind_id)+',court_id='+str(court_id)+' where id='+str(my_dict['id'])
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