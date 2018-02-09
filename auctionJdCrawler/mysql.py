#coding=utf-8
import MySQLdb
import time

class Mysql:
    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost', 'root', '123456', 'jd_crawler')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def dateFormat(self,msec):
        date =  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msec/1000))
        return date
    def insertData(self,my_dict):
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
            sqlCheck = 'SELECT count(*) FROM auction_id  where auction_id='+ str(my_dict['id'])
            self.cur.execute(sqlCheck)
            if self.cur._rows[0][0] == 0:
                #缓存表
                sqlAche = "INSERT INTO auction_id (auction_id) value ("+ str(my_dict['id'])  +")"
                sqlInfo = "insert into %s (%s) VALUES (%s)" % ("auction_info", "id,start_time,end_time,paimai_status,paimai_times,current_price,auction_type,court_id",my_dict['id']+",'"+my_dict['start_time'] +"','"+ my_dict['end_time']+"',"+ my_dict['paimai_status']+","+my_dict['paimai_times']+","+my_dict['current_price']+","+my_dict["auction_type"]+","+my_dict['court_id'])
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
                sqlUpdate = 'update %s set '%("auction_info")
                sqlUpdate = sqlUpdate + 'start_time="' + my_dict['start_time'] + '",end_time="'+my_dict['end_time']+'",paimai_status='+ my_dict['paimai_status'] + ',paimai_times='+my_dict['paimai_times']+',current_price='+ my_dict['current_price']+',auction_type='+my_dict['auction_type'] + ',court_id='+my_dict['court_id']+ ' where id= '+my_dict['id']
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
    def getKindList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,auction_type from auction_kind "
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCourtList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,court_id from court_info"
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getStatusList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,auction_status from auction_status"
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
