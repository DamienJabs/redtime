import typer
import os
from commands.list_tickets import list_tickets
from commands.list_project_tickets import list_project_tickets
from commands.show_time import show_time
from commands.add_time import add_time_ticket
from commands.close_ticket_id import close_ticket_id
from datetime import datetime

app = typer.Typer()

redmine_url = os.getenv("REDMINE_URL")
redmine_api_key = os.getenv("REDMINE_API_KEY")
redmine_project = os.getenv("REDMINE_PROJECT")

if not redmine_api_key or not redmine_project or not redmine_url:
    print("Error: REDMINE_API_KEY, REDMINE_PROJECT, and REDMINE_URL environment variables must be set.")
    exit(1)

@app.command("list")
def list(status: str = typer.Argument("open", help="Ticket status filter: 'open' (default) or 'closed'")):
    """List your assigned tickets."""
    list_tickets(redmine_url, redmine_api_key, status)


@app.command("project")
def project(project: str = typer.Option(redmine_project, help="Project slug (default: $REDMINE_PROJECT)")):
    """List all open tickets for a project."""
    list_project_tickets(redmine_url, redmine_api_key, project)

@app.command("time")
def time(time: bool = typer.Option(False, "--previous", help="Show previous month instead of current month")):
    """Show your time entries for the current or previous month."""
    show_time(redmine_url, redmine_api_key, time)

@app.command("add")
def add_time(ticket: str = typer.Argument(..., help="Ticket ID to log time on"),
        time: int = typer.Argument(..., help="Number of hours to log"),
        spent_on: str = typer.Option(datetime.now().strftime("%Y-%m-%d"), help="Date in DD-MM format (default: today)")):
    """Log time on a ticket."""
    add_time_ticket(redmine_url, redmine_api_key, ticket, time, spent_on)

@app.command("off")
def add_day_off(time: int = typer.Argument(..., help="Number of hours to log as absence"),
        spent_on: str = typer.Option(datetime.now().strftime("%Y-%m-%d"), help="Date in DD-MM format (default: today)")):
    """Log absence time."""
    add_time_ticket(redmine_url, redmine_api_key, "1", time, spent_on)

@app.command("close")
def close_ticket(ticket: str = typer.Argument(..., help="Ticket ID to close"),
          bdpc: bool = typer.Argument(..., help="'Bon du premier coup': True = Oui, False = Non")):
    """Close a ticket and go through all workflow transitions."""
    if ticket == "1":
        print("You cannot close this ticket")
        exit(1)
    close_ticket_id(redmine_url, redmine_api_key, ticket, bdpc)

if __name__ == '__main__':
  app()
