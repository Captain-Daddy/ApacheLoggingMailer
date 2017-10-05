#!usr/bin/python
import smtplib
import sys
import re
import json
from urllib.request import urlopen
from logobject import LogObject

main_pattern = '(.*)\s-\s-\s\[(.*)\]\s\"([^\"]*)\"\s(\d{3})\s\d{3,5}\s\"([^\"]*)\"\s\"([^\"]*)\"'
reg_ex_main = re.compile(main_pattern)

def mail_apache_logs(filepath):
    log_objects = list()
    with open(filepath) as f:
        for line in f:
            data = reg_ex_main.match(line)
            if data:
                log_objects.append(LogObject(data.group(1), data.group(2), data.group(3), 
                                             data.group(4), data.group(5), data.group(6)))
                
    portfolio_accesses = get_portfolio_accesses(log_objects)
    client_error_accesses = get_client_error_accesses(log_objects)
    server_error_accesses = get_server_error_accesses(log_objects)

    get_country_city_tuple(portfolio_accesses[0].ip_address)


def get_portfolio_accesses(log_objects):
    return [log for log in log_objects if "GET /portfolio/ " in log.request]

def get_client_error_accesses(log_objects):
    return [log for log in log_objects if re.match("(4\d{2})", log.status_code)]

def get_server_error_accesses(log_objects):
    return [log for log in log_objects if re.match("(5\d{2})", log.status_code)]

def get_country_city_tuple(ip_address):
    url = 'http://ipinfo.io/' + ip_address + '/json'
    response = urlopen(url)
    data = json.load(response)

    return (data['city'], data['country'])

mail_apache_logs(sys.argv[0])

#msg = dict()
#msg['Subject'] = "fug"
#msg['From'] = "pi@dhein.ddns.net"
#msg['To'] = "dimitri.hein@outlook.de"

# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('127.0.0.1')
#s.sendmail(me, [you], msg.as_string())
#s.quit()

