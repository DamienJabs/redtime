from rich.console import Console
from rich.table import Table
from .redmine_request import redmine_request
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

def list_tickets(redmine_url, redmine_api_key, redmine_project_id, status):
    lists = redmine_request(redmine_url, redmine_api_key, f"issues.json?project_id={redmine_project_id}&assigned_to_id=me&status_id={status}").json()
    tz = ZoneInfo("Europe/Paris")
    now_date = datetime.now(tz).date()
    console = Console()

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold", width=8)
    table.add_column("Client", style="italic", width=20)
    table.add_column("Name", justify="left")
    table.add_column("Time", justify="right")
    table.add_column("Due date", justify="right")
    for issue in lists["issues"]:
        ticket_id = str(issue['id'])
        author = issue['author']['name']
        subject = issue['subject']
        time = issue['spent_hours']
        if not issue['due_date']:
            table.add_row(ticket_id, author, subject, f"[blue]{time}[/blue]", "N/A")
            continue
        due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d").date()
        delta = due_date - now_date
        if delta < timedelta(days=-2):
            table.add_row(ticket_id, author, subject, f"[blue]{time}[/blue]", f"[red]{issue['due_date']}[/red]")
        elif delta < timedelta(days=2):
            table.add_row(ticket_id, author, subject, f"[blue]{time}[/blue]", f"[yellow]{issue['due_date']}[/yellow]")
        else:
            table.add_row(ticket_id, author, subject, f"[blue]{time}[/blue]", f"[green]{issue['due_date']}[/green]")

    console.print(table)
