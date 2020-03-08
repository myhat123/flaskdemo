import psycopg2
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List

from config import config

class SQLDB(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            config['default'].SQLALCHEMY_DATABASE_URI
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


    def write_data(self, data: str):
        for x in data:
            self.cursor.execute("""
                insert into brch_qry_dtl (
                    tran_date, timestampl, acc, 
                    amt, dr_cr_flag, rpt_sum) 
                    values (
                        %s, %s, %s, 
                        %s, %s, %s)
            """, (
                x[0], x[1], x[2], 
                Decimal(x[3]), int(x[4]), x[5]
            ))

        self.conn.commit()

    def get_time_range_dtl_apart(self, tran_date: str, dr_cr_flag: str) -> List[Dict]:
        '''时间间隔区间交易金额摘要分布汇总'''

        # datetime.strptime把str转换为date
        d = datetime.strptime(tran_date, '%Y%m%d') - timedelta(days=1)
        # datetime.strftime把date转换为str
        start = d.strftime('%Y%m%d') + '230000'
        end = tran_date[:8] + '223000'

        self.cursor.execute("""
            select t1.time, t2.rpt_sum, coalesce(t2.amt, 0) as amt
            from (
                select time from generate_series(to_timestamp(%s, 'yyyymmddhh24miss'), 
                to_timestamp(%s, 'yyyymmddhh24miss'), '30 min') as time
            ) t1

            left join (
                select p.gs, p.rpt_sum, sum(p.amt) as amt
                from (
                    select ceil_minute(to_timestamp(timestampl, 'yyyymmddhh24miss'), '30 minutes'
                ) as gs, rpt_sum, amt 
                from brch_qry_dtl 
                    where tran_date=%s
                    and dr_cr_flag=%s
                ) as p
                group by p.gs, p.rpt_sum
            ) t2
            on (t1.time=t2.gs)
            order by t1.time, amt desc
        """, (start, end, tran_date, int(dr_cr_flag))
        )

        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['time'] = row[0]
            d['rpt_sum'] = row[1]
            d['amt'] = row[2]
            results.append(d)
        
        return results


    def get_time_range_dtl(self, tran_date: str, dr_cr_flag: str) -> List[Dict]:
        '''时间间隔区间交易金额汇总'''

        d = datetime.strptime(tran_date, '%Y%m%d') - timedelta(days=1)
        start = d.strftime('%Y%m%d') + '230000'
        end = tran_date[:8] + '223000'

        self.cursor.execute("""
            select t1.time, coalesce(t2.amt, 0) as amt
            from (
                select time from generate_series(to_timestamp(%s, 'yyyymmddhh24miss'), 
                to_timestamp(%s, 'yyyymmddhh24miss'), '30 min') as time
            ) t1

            left join (
                select p.gs, sum(p.amt) as amt
                from (
                    select ceil_minute(to_timestamp(timestampl, 'yyyymmddhh24miss'), '30 minutes') as gs, 
                    timestampl, amt 
                    from brch_qry_dtl 
                    where tran_date=%s 
                        and dr_cr_flag=%s
                    order by timestampl) as p
                group by p.gs) t2
            on (t1.time=t2.gs)
            order by t1.time
        """, (start, end, tran_date, int(dr_cr_flag)))

        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['time'] = row[0]
            d['amt'] = row[1]
            results.append(d)
        
        return results


    def get_details_amt(self, tran_date: str, dr_cr_flag: str) -> List[Dict]:
        """获取所有明细"""

        self.cursor.execute("""
            select rpt_sum, sum(amt) as amt_sum 
            from brch_qry_dtl 
            where tran_date=%s
                and dr_cr_flag=%s
            group by rpt_sum
            order by amt_sum desc
        """, (tran_date, int(dr_cr_flag)))

        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['rpt_sum'] = row[0]
            d['amt'] = row[1]
            results.append(d)
        
        return results

    
    def get_members_rank(self, tran_date: str, dr_cr_flag: str) -> List[Dict]:
        """获取所有人员的排名（前十）"""

        self.cursor.execute("""
            select acc, rpt_sum, sum(amt) as amt_sum
            from brch_qry_dtl
            where tran_date=%s
                and dr_cr_flag=%s
            group by rpt_sum, acc 
            order by amt_sum desc
        """, (tran_date, int(dr_cr_flag))
        )

        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['acc'] = row[0]
            d['rpt_sum'] = row[1]
            d['amt'] = row[2]
            results.append(d)

        return results

    def get_access_log(self, date:str):
        """获取访问记录"""

        start = date + ' 080000'
        end = date + ' 220000'

        self.cursor.execute("""
            select time from generate_series(to_timestamp(%s, 'yyyymmdd hh24miss'), 
                to_timestamp(%s, 'yyyymmdd hh24miss'), '30 min') as time
        """, (start, end))
        
        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['gs'] = row[0]
            results.append(d)
    
        self.cursor.execute("""
            select floor_minute(time, '30 minutes') as gs, time, username, \"desc\"
            from accesslog
            where time>=to_timestamp(%s, 'yyyymmdd hh24miss') 
              and time<=to_timestamp(%s, 'yyyymmdd hh24miss')
            order by gs
        """, (start, end))

        results1 = []
        for row in self.cursor.fetchall():
            d = dict()
            d['gs'] = row[0]
            d['time'] = row[1]
            d['username'] = row[2]
            d['desc'] = row[3]
            results1.append(d)

        for x in results:
            x['details'] = [y for y in results1 if y['gs']==x['gs']]
            x['cnt'] = len(x['details'])

        return results

    def get_access_cnt(self, start:str, end:str):
        """获取时间段访问记录数"""

        self.cursor.execute("""
            select t1.time, coalesce(t2.cnt, 0) from (
                select time from generate_series(%s::date, %s, '1 days') as time) t1
            left join (
                select t.logdate, count(*) as cnt 
                from (
                    select time::date as logdate, * from accesslog) t
                group by logdate) t2
            on (t1.time=t2.logdate)
        """, (start, end))

        results = []
        for row in self.cursor.fetchall():
            d = dict()
            d['logdate'] = row[0].strftime('%m-%d')
            d['cnt'] = row[1]
            results.append(d)

        return results