# redtime

A CLI tool to manage Redmine tickets and time entries from your terminal.

## Requirements

- Python 3.11+
- [typer](https://typer.tiangolo.com/)
- [requests](https://requests.readthedocs.io/)
- [rich](https://rich.readthedocs.io/)

```bash
pip install typer requests rich
```

## Configuration

Set the following environment variables:

```bash
export REDMINE_URL=https://your-redmine-instance.com
export REDMINE_API_KEY=your_api_key
export REDMINE_PROJECT=your_project_slug
```

## Commands

### `list`

List your assigned tickets.

```bash
python main.py list          # open tickets (default)
python main.py list closed   # closed tickets
```

### `project`

List all open tickets for a project.

```bash
python main.py project                              # uses REDMINE_PROJECT
python main.py project --project my-project         # override project
```

### `time`

Show your time entries for the current or previous month as a table.

```bash
python main.py time             # current month
python main.py time --previous  # previous month
```

### `add`

Log time on a ticket.

```bash
python main.py add 18613 8              # log 8h today
python main.py add 18613 4 --spent-on 25-04   # log 4h on April 25
```

### `off`

Log absence time.

```bash
python main.py off 8                    # log 8h absence today
python main.py off 8 --spent-on 25-04  # log 8h absence on April 25
```

### `close`

Close a ticket and go through all workflow transitions (Launcher → Do → Shop Stock → Closed).

```bash
python main.py close 18613 true   # close with "Bon du premier coup: Oui"
python main.py close 18613 false  # close with "Bon du premier coup: Non"
```
