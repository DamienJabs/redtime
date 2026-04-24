import typer
import os
from commands.list_tickets import list_tickets
from commands.list_project_tickets import list_project_tickets
from commands.show_time import show_time

app = typer.Typer()

redmine_url = os.getenv("REDMINE_URL")
redmine_api_key = os.getenv("REDMINE_API_KEY")
redmine_project = os.getenv("REDMINE_PROJECT")

if not redmine_api_key or not redmine_project or not redmine_url:
    print("Error: REDMINE_API_KEY, REDMINE_PROJECT, and REDMINE_URL environment variables must be set.")
    exit(1)

@app.command("list")
def list(status: str = typer.Argument("open", help="List open or closed items")):
    list_tickets(redmine_url, redmine_api_key, redmine_project, status)


@app.command("project")
def project(project: str = typer.Option(redmine_project, help="Project slug to show")):
    list_project_tickets(redmine_url, redmine_api_key, project)

@app.command("time")
def time(time: bool = typer.Option(False, "--previous", help="Show time for this month or previous month")):
    show_time(redmine_url, redmine_api_key, time)

@app.command("add")
def add(ticket: str = typer.Argument(..., help="Ticket to add time for"), 
        time: float = typer.Argument(..., help="Time in hours to add")):
    print("add time...")

@app.command("close")
def close(ticket: str = typer.Argument(..., help="Ticket to close"),
          bdpc: bool = typer.Argument(..., help="Close ticket with BDPC status")):
    print("close ticket...")

if __name__ == '__main__':
  app()
