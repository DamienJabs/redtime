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
export REDMINE_PROJECT_ID=your_project_id
```

## Commands

### `list`

List your assigned open/closed tickets.

```bash
python main.py list          # open tickets (default)
python main.py list closed   # closed tickets
```

### `project`

List all open tickets for a project.

```bash
python main.py project                        # uses REDMINE_PROJECT_ID
python main.py project --project-id 42        # override project
```

### `time`

Show your time entries for the current or previous month as a table.

```bash
python main.py time             # current month
python main.py time --previous  # previous month
```
