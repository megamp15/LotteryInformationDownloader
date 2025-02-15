from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_default_dates(date):
        """Calculate default start and end dates.
        Start date is first of previous month.
        End date is the first Saturday after the last day of previous month."""
        d = datetime.today() if not date else date

        # Calculate the first day of the previous month
        start_date = d - relativedelta(months=1)
        start_date = start_date.replace(day=1)

        # Calculate the last day of the previous month
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        
        # Add days until we reach Saturday (where 5 = Saturday)
        while end_date.weekday() != 5:
            end_date += timedelta(days=1)

        first_day = "{0}/{1}/{2}".format(str(start_date.month).zfill(2), str(start_date.day).zfill(2), start_date.year)
        last_day = "{0}/{1}/{2}".format(str(end_date.month).zfill(2), str(end_date.day).zfill(2), end_date.year)
        
        return first_day, last_day

def get_week_ranges(start_date_str, end_date_str):
        """Calculate week ranges from start to end date"""
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')

        # Calculate the first Saturday of the month
        days_to_saturday = (5 - start_date.weekday()) % 7
        first_saturday = start_date + timedelta(days=days_to_saturday)

        week_ranges = []
        current_start = start_date

        # Generate full week ranges
        while current_start <= end_date:
            week_end = min(first_saturday, end_date)
            week_ranges.append((
                week_end.strftime('%Y%m%d'),
                current_start.strftime('%Y-%m-%d'),
                week_end.strftime('%Y-%m-%d')
            ))
            current_start = first_saturday + timedelta(days=1)
            first_saturday += timedelta(days=7)
            
        return week_ranges

if __name__ == "__main__":
    first_day, last_day = calculate_default_dates(datetime(2025, 2, 1))
    print(first_day, last_day)
    print(get_week_ranges(first_day, last_day))
