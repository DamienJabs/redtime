from .redmine_request import redmine_request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar
from rich.console import Console
from rich.table import Table

def build_time_table(redmine_url, redmine_api_key, user_id, date_start, date_end, now_date):
    total_days_month = calendar.monthrange(now_date.year, now_date.month)
    table = Table(show_header=True, header_style="bold cyan")

    lists = redmine_request(redmine_url, redmine_api_key, f"time_entries.json?user_id={user_id}&spent_on=><{date_start}|{date_end}&offset=0&limit=100").json()
    total_time_day = {}

    for ticket in lists["time_entries"]:
        date = ticket['spent_on']
        time = ticket['hours']
        if date in total_time_day:
            total_time_day[date] += time
        else:
            total_time_day[date] = time

    row = []
    total_hours = 0

    for i in range(1, total_days_month[1] + 1):
        format_data = datetime(now_date.year, now_date.month, i).strftime("%a %d")
        table.add_column(format_data)
        date = datetime(now_date.year, now_date.month, i).strftime("%Y-%m-%d")
        if date in total_time_day:
            if total_time_day[date] == 8:
                row.append(f"[green]{total_time_day[date]}[/green]")
            else:
                row.append(f"[yellow]{total_time_day[date]}[/yellow]")
        elif datetime(now_date.year, now_date.month, i).weekday() >= 5:
            row.append("[dim]-[/dim]")
        else:
            row.append("[red]0[/red]")
        if datetime(now_date.year, now_date.month, i).weekday() < 5:
            total_hours += 8

    total_time = sum(total_time_day.values())
    table.add_column("Total", style="bold", width=10, justify="right")
    table.add_row(*row, f"{int(total_time)}/{total_hours}")

    return table

def show_time(redmine_url, redmine_api_key, previous):
    userinfo = redmine_request(redmine_url, redmine_api_key, f"users/current.json").json()
    user_id = userinfo['user']['id']

    tz = ZoneInfo("Europe/Paris")
    now_date = datetime.now(tz).date()

    console = Console()
    
    if not previous:
        days = calendar.monthrange(now_date.year, now_date.month)
        date_start = datetime(now_date.year, now_date.month, 1).strftime("%Y-%m-%d")
        date_end = datetime(now_date.year, now_date.month, days[1]).strftime("%Y-%m-%d")

        table = build_time_table(redmine_url, redmine_api_key, user_id, date_start, date_end, now_date)

    else:
        last_day_prev = now_date.replace(day=1) - timedelta(days=1)
        prev_days = calendar.monthrange(last_day_prev.year, last_day_prev.month)
        date_start = datetime(last_day_prev.year, last_day_prev.month, 1).strftime("%Y-%m-%d")
        date_end = datetime(last_day_prev.year, last_day_prev.month, prev_days[1]).strftime("%Y-%m-%d")

        table = build_time_table(redmine_url, redmine_api_key, user_id, date_start, date_end, last_day_prev)

    console.print(table)
