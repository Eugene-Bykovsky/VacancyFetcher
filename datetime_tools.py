from datetime import datetime, timedelta


def get_date_offset_by_days(days):
    if days is None:
        return datetime.now().strftime('%Y-%m-%d')
    return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
