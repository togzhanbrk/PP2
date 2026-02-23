import sys
import re
from datetime import datetime, timezone, timedelta

def parse_datetime(s: str) -> datetime:
    m = re.fullmatch(
        r"(\d{4})-(\d{2})-(\d{2}) "
        r"(\d{2}):(\d{2}):(\d{2}) "
        r"UTC([+-])(\d{2}):(\d{2})",
        s.strip()
    )

    y, mo, d, hh, mm, ss = map(int, m.group(1,2,3,4,5,6))
    sign = 1 if m.group(7) == '+' else -1
    off_h = int(m.group(8))
    off_m = int(m.group(9))

    offset_minutes = sign * (off_h * 60 + off_m)
    tz = timezone(timedelta(minutes=offset_minutes))

    return datetime(y, mo, d, hh, mm, ss, tzinfo=tz)

def main():
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    start = parse_datetime(lines[0])
    end = parse_datetime(lines[1])

    start_utc = start.astimezone(timezone.utc)
    end_utc = end.astimezone(timezone.utc)

    diff = int((end_utc - start_utc).total_seconds())
    print(diff)

if __name__ == "__main__":
    main()