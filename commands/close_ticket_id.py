from .redmine_request import redmine_request
from rich.console import Console

def close_ticket_id(redmine_url, redmine_api_key, ticket, bdpc):
    if bdpc:
        bdpc = "Oui"
        bpdc_color = "[green]Oui[/green]"
    else: 
        bdpc = "Non"
        bpdc_color = "[red]Non[/red]"
    ticket_info = redmine_request(redmine_url, redmine_api_key, f"issues.json?issue_id={ticket}").json()
    ticket_status = ticket_info["issues"][0]["status"]["id"]
    
    for status in range(ticket_status + 1, 5):
        if status == 3:
            redmine_request(redmine_url, redmine_api_key, f"issues/{ticket}.json", method="PUT", data={"issue": {"custom_fields": [{"id": 7, "value": bdpc}]}})   
        redmine_request(redmine_url, redmine_api_key, f"issues/{ticket}.json", method="PUT", data={"issue": {"status_id": status}})   
    Console().print(f"Ticket [blue]{ticket}[/blue] closed with BDPC status: {bpdc_color}")
