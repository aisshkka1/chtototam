from datetime import datetime, timedelta, timezone

def parse_datetime_with_tz(s):
    # s = "YYYY-MM-DD HH:MM:SS UTC±HH:MM"
    date_part, time_part, tz_part = s.split()
    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")
    
    # Parse UTC offset
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])
    offset = timezone(timedelta(hours=sign*hours, minutes=sign*minutes))
    
    return dt.replace(tzinfo=offset)

# Read input
start_str = input()
end_str = input()

start_dt = parse_datetime_with_tz(start_str)
end_dt = parse_datetime_with_tz(end_str)

# Convert to UTC
start_utc = start_dt.astimezone(timezone.utc)
end_utc = end_dt.astimezone(timezone.utc)

# Compute duration in seconds
duration_seconds = int((end_utc - start_utc).total_seconds())
print(duration_seconds)