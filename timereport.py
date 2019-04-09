"""timereport.py

This script parses standard input on the format

    yyyy-mm-dd h1:mm1-h2:mm2 (x min...) ...
    ...

And prints out the total duration of the timespans h2:mm2 - h1:mm1 - x.
It's useful for generating time reports.

To run tests:

    python -m doctest timereport.py
"""

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

line_re = re.compile(r'^((?:\d{4}-\d{2}-\d{2})) (\d{1,2}:\d{1,2})-(\d{1,2}:\d{1,2})(?: \((\d+) min.*\))?')
def minutes_from_line(line):
    """Given a line, extract the number of minutes worked, or None if failing to parse.
    >>> minutes_from_line('2019-04-09 8:00-17:00 (50 min lunch) jobbade med data')
    490
    >>> minutes_from_line('2019-04-09 8:00-17:00 jobbade med data')
    540
    >>> minutes_from_line('2019/04/09 8.00-17.00 jobbade med data') is None
    True
    >>> minutes_from_line('') is None
    True
    """
    m = line_re.search(line)
    if m:
        date, start, stop, p = m.groups()
        duration = to_minutes(stop) - to_minutes(start)
        pause = int(p) if p else 0
        return duration - pause
    return None

def minutes_from_file(f):
    """Given a file, return number of minutes worked.
    >>> minutes_from_file(['2019-04-09 8:00-17:00 (50 min lunch) jobbade med data', '2019-04-09 9:15-16:30 (75 min lunch) mer data'])
    850
    """
    total_duration = 0
    for line in f:
        line = line[:-1]
        if line:
            minutes = minutes_from_line(line)
            total_duration += minutes
            print(f"{line} ({minutes} min)", file=sys.stderr)
    return total_duration

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
    >>> timereport(['2019-04-09 8:00-17:00 (50 min lunch) jobbade med data', '2019-04-09 9:15-16:30 (75 min lunch) mer data'])
    'Total 850 min, 14:10'
    """
    duration = minutes_from_file(f)
    return f"Total {duration} min, {format_duration(duration)}"

def main():
    print(timereport(sys.stdin))

if __name__ == '__main__':
    main()
