from django.utils import timezone

def calculate(started_date):
    now = timezone.now()
    duration = now - started_date
    days = duration.days
    years = days // 365
    months = (days % 365) // 30
    remaining_days = (days % 365) % 30

    duration_str = ""
    if years > 0:
        duration_str += f"{years} year{'s' if years > 1 else ''} "
    if months > 0:
        duration_str += f"{months} month{'s' if months > 1 else ''} "
    if remaining_days > 0:
        duration_str += f"{remaining_days} day{'s' if remaining_days > 1 else ''} "

    # Exclude hours from the duration string if the duration is more than a month
    if months == 0:
        hours = duration.seconds // 3600
        if hours > 0:
            duration_str += f"{hours} hour{'s' if hours > 1 else ''}"

    # If the duration is less than one day, set the duration string as "today"
    if not duration_str:
        duration_str = "today"

    return duration_str.strip()