from datetime import datetime, timezone, timedelta

def parse_moment(s: str) -> datetime:
    date_part, tz_part = s.split()

    dt = datetime.strptime(date_part, "%Y-%m-%d")

    sign = 1 if tz_part[3] == "+" else -1
    hh, mm = tz_part[4:].split(":")
    offset = timedelta(hours=int(hh), minutes=int(mm)) * sign

    return dt.replace(tzinfo=timezone(offset)).astimezone(timezone.utc)

a = parse_moment(input().strip())
b = parse_moment(input().strip())

delta_seconds = abs((a - b).total_seconds())
full_days = int(delta_seconds // 86400)

print(full_days)