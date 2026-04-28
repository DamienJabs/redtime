from .redmine_request import redmine_request
from rich.console import Console

def reopen_ticket(redmine_url, redmine_api_key, ticket):
    # Closed → Launcher is allowed by the workflow; Launcher → Do is then possible
    redmine_request(redmine_url, redmine_api_key, f"/issues/{ticket}.json", method="PUT", data={"issue": {"status_id": 1}})
    redmine_request(redmine_url, redmine_api_key, f"/issues/{ticket}.json", method="PUT", data={"issue": {"status_id": 2}})
    Console().print(f"Ticket [blue]{ticket}[/blue] reopened and set to [green]Do[/green]")
