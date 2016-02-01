#! /usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib, urllib2, json
from smtp import smtp
from email.mime.text import MIMEText

mailto_list=['recipient@example.com']
mail_host="smtp.example.com"
mail_pass="PASSWORD"
me = "me@example.com"

def send_mail(to_list, sub, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    try:
        smtpObj = smtp(mail_host)
        smtpObj.ehlo()
        smtpObj.login(me, mail_pass)
        smtpObj.sendmail(me, to_list, msg.as_string().encode('ascii'))
        smtpObj.quit()
        return True
    except Exception, e:
        print str(e)
        return False


def getMessage():
    u = "http://api.map.baidu.com/telematics/v3/weather?location=%E4%B8%8A%E6%B5%B7&output=json&ak=aQbiXLKYETCsTDSuVmljaBX7"
    html = urllib2.urlopen(u).read()
    j = json.loads(html)
    if j['status'] == 'success':
        if u'雨' in j['results'][0]['weather_data'][0]['weather'] or 1==1:
            m = u'今天天气:' + j['results'][0]['weather_data'][0]['weather'] + u'，请注意带好雨具哦！'
        else:
            return False
    else:
        m = j['status']

    return m



if __name__ == '__main__':
    subject = "Umbrella Reminder"
    content = getMessage()
    if content is not False:
        if send_mail(mailto_list, subject, content):
            print "done!"
        else:
            print "failed!"
