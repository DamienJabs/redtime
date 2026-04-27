from .redmine_request import redmine_request
from datetime import datetime
from rich.console import Console

def add_time_ticket(redmine_url, redmine_api_key, ticket, time, spent_on):
        if len(spent_on) == 5 and spent_on[2] == "-":
            try:
                spent_on = datetime.strptime(spent_on, "%d-%m").replace(year=datetime.now().year).strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use DD-MM.")
                exit(1)
        elif len(spent_on) == 10:
            pass
        else:
            print("Invalid date format. Please use DD-MM.")
            exit(1)
        redmine_request(redmine_url, redmine_api_key, f"/time_entries.json", method="POST", data={"issue_id": ticket, "time_entry": {"hours": time, "spent_on": spent_on}}).json()

        ticket_info = redmine_request(redmine_url, redmine_api_key, f"issues.json?issue_id={ticket}").json()
        ticket_name = ticket_info["issues"][0]["subject"]
        ticket_spent_time = ticket_info["issues"][0]["spent_hours"]
        Console().print(f"Added [green]{time}h[/green] to ticket [blue]{ticket}[/blue] on [yellow]{spent_on}[/yellow] - {ticket_name} (total: [cyan]{ticket_spent_time}h[/cyan])")
