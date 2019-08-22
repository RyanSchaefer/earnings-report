import yahoo_earnings_calendar
import datetime
from functools import reduce

date_from = datetime.datetime(2019, 8, 25, 0, 0)
date_to = datetime.datetime(2019, 8, 31, 0, 0)
y = yahoo_earnings_calendar.YahooEarningsCalendar()

FORMAT_STRING = \
    lambda x: f"""<bold>{x['ticker']}</bold>\r\n
<p> EST. EPS: {x['espestimate']} </p>\r\n
<p> Day: {datetime.datetime.strptime(x['startdatetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%A')} </p>\r\n
<p> Time: {x['startdatetimetype']} </p>\r\n
"""


def format_report(list_of_companies):
    print(FORMAT_STRING(list_of_companies[0]))
    return reduce(lambda x,y: y+FORMAT_STRING(x), "<h1> Upcoming Earnings </h1>", list_of_companies)


open("output.html", 'w').write(format_report(y.earnings_between(date_from, date_to)))
