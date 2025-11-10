# Issues Slack Notifier

Workflow: `.github/workflows/notify.yml`  
Script: `scripts/notify.py`  
Config: `repo_config.yaml`

Wat het doet:
- Checkt elke 10 minuten nieuwe issues in opgegeven repos en meldt ze in Slack.

Triggers:
- `schedule`: `*/10 * * * *`
- `workflow_dispatch`

Benodigde secrets:
- `SLACK_WEBHOOK_URL`: Slack incoming webhook URL.
- `GITHUB_APP_ID` en `GITHUB_APP_PRIVATE_KEY`: om via een GitHub App installation token te authenticeren.

Permissions:
- `contents: read`

Opmerkingen:
- Het script gebruikt `GITHUB_TOKEN`/`GH_TOKEN` indien aanwezig voor GitHub API-calls.
- Schedules kunnen pauzeren na ~60–90 dagen repo-inactiviteit. Overweeg de orchestrator (zie `docs/orchestrator.md`).


