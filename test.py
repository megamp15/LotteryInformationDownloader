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

if __name__ == "__main__":
    print(calculate_default_dates(datetime(2024, 12, 1)))
