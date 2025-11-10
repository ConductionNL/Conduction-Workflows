# Orchestrator (Org maintenance poke)

Workflow: `.github/workflows/poke-all.yml`

Doel:
- Workflows in org-repos wekelijks "aanstippen" zodat `schedule`-workflows niet langdurig gepauzeerd blijven na repo-inactiviteit.
- Optioneel workflows opnieuw enablen en gericht triggeren via `workflow_dispatch`, met fallback naar `repository_dispatch`.

Triggers:
- `schedule`: `0 5 * * 1` (elke maandag 05:00 UTC)
- `workflow_dispatch`

Benodigde secrets (org of repo secrets):
- `GITHUB_APP_ID`
- `GITHUB_APP_PRIVATE_KEY`
  - De GitHub App moet geïnstalleerd zijn op de gewenste org/repos met minimaal `actions: write` en `metadata: read`.

Permissions:
- `contents: read`
- `actions: write`

Globale werkwijze:
1) Maak een GitHub App aan (org-breed), download de private key en noteer de App ID.  
2) Installeer de App op de org (en de doel-repositories).  
3) Zet de secrets in je org of in deze repo.  
4) Pas de lijst van te poken repos en workflow-bestanden aan (zie workflow file).  


