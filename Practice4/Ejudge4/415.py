import sys
import re
from datetime import datetime, date, timezone, timedelta

def parse_line(s: str):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})\s+UTC([+-])(\d{2}):(\d{2})", s.strip())
    y, mo, d = map(int, m.group(1, 2, 3))
    sign = 1 if m.group(4) == '+' else -1
    hh = int(m.group(5))
    mm = int(m.group(6))
    offset_minutes = sign * (hh * 60 + mm)

    tz = timezone(timedelta(minutes=offset_minutes))
    return datetime(y, mo, d, 0, 0, 0, tzinfo=tz), tz

def is_leap(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def birthday_for_year(month: int, day: int, year: int) -> date:
    if month == 2 and day == 29 and not is_leap(year):
        return date(year, 2, 28)
    return date(year, month, day)

def main():
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    birth_dt, birth_tz = parse_line(lines[0])
    curr_dt, _ = parse_line(lines[1])

    birth_month, birth_day = birth_dt.month, birth_dt.day

    curr_utc = curr_dt.astimezone(timezone.utc)

    best = None
    for year in range(curr_dt.year - 1, curr_dt.year + 3):
        bd = birthday_for_year(birth_month, birth_day, year)
        candidate = datetime(bd.year, bd.month, bd.day, 0, 0, 0, tzinfo=birth_tz)
        candidate_utc = candidate.astimezone(timezone.utc)

        if candidate_utc >= curr_utc:
            if best is None or candidate_utc < best:
                best = candidate_utc

    diff_seconds = int((best - curr_utc).total_seconds())

    if diff_seconds <= 0:
        print(0)
    else:
        days = (diff_seconds + 86400 - 1) // 86400
        print(days)

if __name__ == "__main__":
    main()