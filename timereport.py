import re
import sys

line_re = re.compile(r'^((?:\d{4}-\d{2}-\d{2})) (\d{1,2}:\d{1,2})-(\d{1,2}:\d{1,2})(?: \((\d+) min.*\))?')

def to_minutes(s):
    """
    Convert a time specification on the form hh:mm to minutes.
    >>> to_minutes('8:05')
    485
    """
    h, m = s.split(':')
    return int(h) * 60 + int(m)

def main():
    total_duration = 0

    for line in sys.stdin:
        line = line[:-1]
        if line:
            m = line_re.search(line)
            if m:
                try:
                    date, start, stop, p = m.groups()
                    duration = to_minutes(stop) - to_minutes(start)
                    pause = int(p) if p else 0
                    total_duration += duration - pause
                    print("{} ({}-{}={} min)".format(line, duration, pause, duration - pause))
                except:
                    print("* {} (crashed)".format(line))
            else:
                print("* {} (unparseable)".format(line))

    total_h = total_duration // 60
    total_m = total_duration % 60
    print("Total {} min, {:02}:{:02}".format(total_duration, total_h, total_m))

if __name__ == '__main__':
    main()
