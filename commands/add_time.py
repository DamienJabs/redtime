from .redmine_request import redmine_request
from datetime import datetime
from rich.console import Console

def check_spent_time(redmine_url, redmine_api_key, time, spent_on):
    entries = redmine_request(redmine_url, redmine_api_key, f"time_entries.json?user_id=me&spent_on={spent_on}").json()
    total = sum(e["hours"] for e in entries["time_entries"])
    if total + time > 8:
        spent_on_display = datetime.strptime(spent_on, "%Y-%m-%d").strftime("%d-%m-%Y")
        Console().print(f"[red]Error:[/red] Would exceed 8h on {spent_on_display} (current: [yellow]{total}h[/yellow], adding: [yellow]{time}h[/yellow])")
        exit(1)

def add_time_ticket(redmine_url, redmine_api_key, ticket, time, spent_on):
    if len(spent_on) == 10 and spent_on[2] == "-" and spent_on[5] == "-":
        try:
            spent_on = datetime.strptime(spent_on, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use DD-MM or DD-MM-YYYY.")
            exit(1)
    if len(spent_on) == 5 and spent_on[2] == "-":
        try:
            spent_on = datetime.strptime(spent_on, "%d-%m").replace(year=datetime.now().year).strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use DD-MM or DD-MM-YYYY.")
            exit(1)
    elif len(spent_on) == 10:
        pass
    else:
        print("Invalid date format. Please use DD-MM or DD-MM-YYYY.")
        exit(1)
    check_spent_time(redmine_url, redmine_api_key, time, spent_on)
    redmine_request(redmine_url, redmine_api_key, "time_entries.json", method="POST", data={"issue_id": ticket, "time_entry": {"hours": time, "spent_on": spent_on}}).json()

    ticket_info = redmine_request(redmine_url, redmine_api_key, f"issues/{ticket}.json").json()
    ticket_name = ticket_info["issue"]["subject"]
    ticket_spent_time = ticket_info["issue"]["spent_hours"]
    Console().print(f"Added [green]{time}h[/green] to ticket [blue]{ticket}[/blue] on [yellow]{spent_on}[/yellow] - {ticket_name} (total: [cyan]{ticket_spent_time}h[/cyan])")
