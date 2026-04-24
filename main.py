import typer
import os
from commands.list_tickets import list_tickets
from commands.list_project_tickets import list_project_tickets
from commands.show_time import show_time

app = typer.Typer()

redmine_url = os.getenv("REDMINE_URL")
redmine_api_key = os.getenv("REDMINE_API_KEY")
redmine_project_id = os.getenv("REDMINE_PROJECT_ID")

if not redmine_api_key or not redmine_project_id or not redmine_url:
    print("Error: REDMINE_API_KEY, REDMINE_PROJECT_ID, and REDMINE_URL environment variables must be set.")
    exit(1)

@app.command("list")
def list(status: str = typer.Argument("open", help="List open or closed items")):
    list_tickets(redmine_url, redmine_api_key, redmine_project_id, status)


@app.command("project")
def project(project_id: str = typer.Option(redmine_project_id, help="Project ID to show")):
    list_project_tickets(redmine_url, redmine_api_key, project_id)

@app.command("time")
def time(time: bool = typer.Option(False, "--previous", help="Show time for this month or previous month")):
    show_time(redmine_url, redmine_api_key, time)

@app.command("add")
def add(ticket: str = typer.Argument(..., help="Ticket to add time for"), 
        time: float = typer.Argument(..., help="Time in hours to add")):
    print("add time...")

if __name__ == '__main__':
  app()
