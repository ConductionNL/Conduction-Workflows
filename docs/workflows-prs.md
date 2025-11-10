# PRs Slack Notifier

Workflow: `.github/workflows/get-pr-data.yml`  
Script: `scripts/get_pr_data_to_slack.py`  
Config: `repo_config.yaml`

Wat het doet:
- Haalt open pull requests op per repo en post een compacte samenvatting naar Slack.

Triggers:
- `schedule`: `*/30 * * * *`
- `workflow_dispatch`

Benodigde secrets:
- `SLACK_WEBHOOK_URL`: Slack incoming webhook URL.
- `GITHUB_APP_ID` en `GITHUB_APP_PRIVATE_KEY`: om via een GitHub App installation token te authenticeren.

Permissions:
- `contents: read`
- `pull-requests: read`

Opmerkingen:
- Gebruikt een GitHub App token i.p.v. een persoonlijke PAT, zodat er geen persoonlijke tokens nodig zijn in de org.
- Oorspronkelijke inspiratie/code: `https://github.com/MWest2020/get-pr-data`


