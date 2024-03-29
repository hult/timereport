"""timereport.py

This script parses standard input on the format

    yyyy-mm-dd h1:mm1-h2:mm2 (x min...) ...
    ...

And prints out the total duration of the timespans h2:mm2 - h1:mm1 - x.
It's useful for generating time reports.

You can also provide a string as the first command-line argument to read
from instead of standard input

    python timereport.py "2021-09-14 8:00-17:00 (60 min lunch) did stuff"

To run tests:

    python -m doctest timereport.py
"""

import io
import re
import sys

def to_minutes(s):
    """
    Convert a time specification on the form hh:mm to minutes.
    >>> to_minutes('8:05')
    485
    """
    h, m = s.split(':')
    return int(h) * 60 + int(m)

line_re = re.compile(r'^((?:\d{4}-\d{2}-\d{2})) ((?:\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}(?:, *)?)+)(?: \((\d+) min.*\))?')
def minutes_from_line(line):
    """Given a line, extract the number of minutes worked, or None if failing to parse.
    >>> minutes_from_line('2019-04-09 8:00-17:00 (50 min lunch) jobbade med data')
    490
    >>> minutes_from_line('2019-04-09 8:00-17:00 (50 min lunch + 10 min call) jobbade med data')
    480
    >>> minutes_from_line('2019-08-16 7:10-8:10, 9:00-9:10, 9:30-10:00, 11:25-11:45, 13:35-13:45 (15 min lunch) jobbade')
    115
    >>> minutes_from_line('2019-04-09 8:00-17:00 jobbade med data')
    540
    >>> minutes_from_line('2019/04/09 8.00-17.00 jobbade med data') is None
    True
    >>> minutes_from_line('') is None
    True
    """
    m = line_re.search(line)
    if m:
        date, intervals, p = m.groups()
        duration = 0
        for interval in re.split(r', *', intervals):
            start, stop = interval.split('-')
            duration += to_minutes(stop) - to_minutes(start)
        pause = int(p) if p else 0
        return duration - pause
    return None

def stats_from_file(f):
    """Given a file, return a tuple of number of days (lines) worked, and number of minutes worked.
    >>> stats_from_file(["2019-04-09 8:00-17:00 (50 min lunch) jobbade med data\\n", "2019-04-09 9:15-16:30 (75 min lunch) mer data\\n"])
    2019-04-09 8:00-17:00 (50 min lunch) jobbade med data (490 min)
    2019-04-09 9:15-16:30 (75 min lunch) mer data (360 min)
    (2, 850)
    >>> stats_from_file(["\\n"])
    (0, 0)
    >>> stats_from_file(["ill-formatted line\\n"])
    * ill-formatted line
    (0, 0)
    >>> stats_from_file(["2021-09-14 8:00-11:00 a string does not end in a newline"])
    2021-09-14 8:00-11:00 a string does not end in a newline (180 min)
    (1, 180)
    """
    total_days = 0
    total_duration = 0
    for line in f:
        line = line.rstrip('\n')
        if line:
            minutes = minutes_from_line(line)
            if minutes:
                total_days += 1
                total_duration += minutes
                print(f"{line} ({minutes} min)")
            else:
                print(f"* {line}")
    return (total_days, total_duration)

def format_duration(duration):
    """Given a duration in minutes, return a string on the format h:mm.
    >>> format_duration(75)
    '1:15'
    >>> format_duration(4)
    '0:04'
    >>> format_duration(601)
    '10:01'
    """
    h = duration // 60
    m = duration % 60
    return f"{h}:{m:02}"

def timereport(f):
    """Given a file, return its time report.
    >>> timereport(["2019-04-09 8:00-17:00 (50 min lunch) jobbade med data\\n", "2019-04-10 11:00-14:00 (40 min lunch) jobbade med data\\n"])
    2019-04-09 8:00-17:00 (50 min lunch) jobbade med data (490 min)
    2019-04-10 11:00-14:00 (40 min lunch) jobbade med data (140 min)
    'Total 2 days, 630 min, 315 mins/day, 10:30'
    """
    days, duration = stats_from_file(f)
    duration_per_day = duration // days
    return f"Total {days} days, {duration} min, {duration_per_day} mins/day, {format_duration(duration)}"

def main():
    if len(sys.argv) == 2:
        print(timereport(io.StringIO(sys.argv[1])))
    else:
        print(timereport(sys.stdin))

if __name__ == '__main__':
    main()
