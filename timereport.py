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
    """
    m = line_re.search(line)
    if m:
        date, start, stop, p = m.groups()
        duration = to_minutes(stop) - to_minutes(start)
        pause = int(p) if p else 0
        return duration - pause
    return None

def main():
    total_duration = 0

    for line in sys.stdin:
        line = line[:-1]
        if line:
            minutes = minutes_from_line(line)
            total_duration += minutes
            print(f"{line} ({minutes} min)")

    total_h = total_duration // 60
    total_m = total_duration % 60
    print(f"Total {total_duration} min, {total_h:02}:{total_m:02}")

if __name__ == '__main__':
    main()
