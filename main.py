# crontab to run this program:
import yahoo_earnings_calendar
import datetime
from functools import reduce
import email, smtplib, ssl
import sys
import getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


date_from = datetime.datetime.now()
date_to = date_from + datetime.timedelta(days=7)
y = yahoo_earnings_calendar.YahooEarningsCalendar()

FORMAT_STRING = \
    lambda x: f"""<b>{x['ticker']}</b>
<a href='https://google.com/search?q={'+'.join(x['companyshortname'].split(' '))}'>{x['companyshortname']}</a>
<p>est. eps: {x['epsestimate']}<br>
Day: {datetime.datetime.strptime(x['startdatetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%A')} 
- {x['startdatetimetype']} </p><br><br>
"""


def format_report(list_of_companies):
    print(FORMAT_STRING(list_of_companies[0]))
    list_of_companies.sort(key=lambda x: x['startdatetime'])
    return reduce(lambda x,y: x+FORMAT_STRING(y), list_of_companies, "<h1> Upcoming Earnings </h1>")


open("output.html", 'w').write(format_report(y.earnings_between(date_from, date_to)))

message = MIMEMultipart()
message['From'] = sys.argv[1]
message["To"] = sys.argv[1]
message["Subject"] = "Your weekly upcoming earnings report"

message.attach(MIMEText(format_report(y.earnings_between(date_from, date_to)), "HTML"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(sys.argv[1], getpass.getpass("Enter email password:"))
    server.sendmail(sys.argv[1], sys.argv[1], message.as_string())