from datetime import datetime, timezone, timedelta

utc = datetime.now(timezone.utc)

kz_tz = timezone(timedelta(hours=6))
kz_time = utc.astimezone(kz_tz)

print(kz_time)

