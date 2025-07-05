from datetime import datetime
import pytz
from typing import Tuple

def convert_datetime_to_target_timezone(
    date_str: str,
    time_str: str,
    source_timezone_str: str,
    target_timezone_str: str
) -> Tuple[str, str]:
    """
    Converts a naive datetime string from a source timezone to a target timezone.

    Args:
        date_str (str): Date in 'YYYY-MM-DD' format.
        time_str (str): Time in 'HH:MM' format.
        source_timezone_str (str): String representation of the source timezone
                                   (e.g., "Asia/Kolkata").
        target_timezone_str (str): String representation of the target timezone
                                   (e.g., "America/New_York").

    Returns:
        Tuple[str, str]: A tuple containing the converted date ('YYYY-MM-DD')
                         and time ('HH:MM') strings in the target timezone.
                         Returns original date/time if timezone conversion fails.
    """
    try:
        source_tz = pytz.timezone(source_timezone_str)
        target_tz = pytz.timezone(target_timezone_str)

        # Combine date and time into a single datetime object
        dt_combined_str = f"{date_str} {time_str}"
        naive_dt = datetime.strptime(dt_combined_str, "%Y-%m-%d %H:%M")

        # Localize the naive datetime to the source timezone
        aware_dt_source = source_tz.localize(naive_dt)

        # Convert to the target timezone
        aware_dt_target = aware_dt_source.astimezone(target_tz)

        return aware_dt_target.strftime("%Y-%m-%d"), aware_dt_target.strftime("%H:%M")
    except pytz.UnknownTimeZoneError:
        print(f"Warning: Unknown timezone string encountered: {source_timezone_str} or {target_timezone_str}. Returning original time.")
        return date_str, time_str
    except Exception as e:
        print(f"Error during timezone conversion: {e}. Returning original time.")
        return date_str, time_str