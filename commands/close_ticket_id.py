from .redmine_request import redmine_request

def close_ticket_id(redmine_url, redmine_api_key, ticket, bdpc):
    if bdpc:
        bdpc = "Oui"
    else: 
        bdpc = "Non"
    ticket_info = redmine_request(redmine_url, redmine_api_key, f"issues.json?issue_id={ticket}").json()
    ticket_status = ticket_info["issues"][0]["status"]["id"]
    
    for status in range(ticket_status + 1, 5):
        if status == 3:
            redmine_request(redmine_url, redmine_api_key, f"/issues/{ticket}.json", method="PUT", data={"issue": {"custom_fields": [{"id": 7, "value": bdpc}]}})   
        redmine_request(redmine_url, redmine_api_key, f"/issues/{ticket}.json", method="PUT", data={"issue": {"status_id": status}})   
