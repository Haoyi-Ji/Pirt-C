import os
import datetime
import sys

def main(startdate, enddate):
    d = startdate
    delta = datetime.timedelta(days=1)
    while(d <= enddate):
        dt = str(d)
        query = """hive -e \"
            insert overwrite table Tmp_AnalysisQueryDB.Jhy_General_GPSData partition(d='%s')
            select
                b.UID,
                a.Time,
                avg(a.Longitude) as Longitude,
                avg(a.Latitude) as Latitude
            from
                (
                    select
                        ClientCode,
                        hour(ActionDate) as Time,
                        coalesce(cast(regexp_extract(ActionRemark,'(.*?latlong:)([0-9]+\\.[0-9]+),([0-9]+\\.[0-9]+)|',3) as float), 
                                 cast(regexp_extract(ActionRemark,'(.*?latlong:)([0-9]+\\.[0-9]+),([0-9]+\\.[0-9]+)|',3) as float)
                                ) as Longitude,
                        coalesce(cast(regexp_extract(ActionRemark,'(.*?latlong:)([0-9]+\\.[0-9]+),([0-9]+\\.[0-9]+)|',2) as float),
                                 cast(regexp_extract(ActionRemark,'(.*?latlong:)([0-9]+\\.[0-9]+),([0-9]+\\.[0-9]+)|',2) as float)
                                ) as Latitude
                    from DW_MobDB.FactMbActionTrace5
                    where d = '%s' and to_date(ActionDate) = '%s' and PageCode = 'o_lat_long'
                ) a
                inner join
                (
                    select distinct ClientCode, UID
                    from Olap_MobDB.OlapClientSource
                    where
                        d = '%s' and
                        UID is not null and UID <> '' and UID <> '\N' and
                        ClientCode is not null and ClientCode <> '' and ClientCode <> '00000000000000000000'
                ) b on a.ClientCode = b.ClientCode
            where
                a.Longitude <> 0 and abs(a.Longitude) <= 180 and
                a.Latitude <> 0 and abs(a.Latitude) <= 90
            group by b.UID, a.Time;\"
            """ % (dt, dt, dt, dt)
            #print query
        os.system(query)
        d += delta


def parseDate(dstring):
    l = dstring.split('-')
    return datetime.date(int(l[0]), int(l[1]), int(l[2]))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print " ---------------------------------------------------------------"
        print "| Usage: python rollback_GPSData1.py <starttime> <endtime>      |"
        print "| Time format: yyyy-mm-dd (e.g. 2015-12-20)                     |"
        print " ---------------------------------------------------------------"
    else:
        t1 = parseDate(str(sys.argv[1]))
        t2 = parseDate(str(sys.argv[2]))
        main(t1, t2)
