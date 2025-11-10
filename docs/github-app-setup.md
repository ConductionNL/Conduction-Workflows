# GitHub App: aanmaken, installeren en gebruiken

Deze gids beschrijft hoe je een GitHub App voor je organisatie aanmaakt, installeert en gebruikt als veilige vervanger voor persoonlijke PATs in workflows.

## 1) App aanmaken
1. Ga naar `Organization settings` → `Developer settings` → `GitHub Apps` → `New GitHub App`.
2. Vul basisgegevens in:
   - GitHub App name: bijvoorbeeld `Conduction Orchestrator`.
   - Homepage URL: je org-site of repo-URL.
   - Webhook (optioneel): niet vereist voor de hier gebruikte flows.
   - Webhook secret: alleen als je webhooks gebruikt.
3. Repository permissions (minimaal):
   - `Metadata`: Read-only (verplicht door GitHub).
   - `Contents`: Read-only.
   - `Actions`: Read & write (nodig voor enable/dispatch in orchestrator).
   - Voor PR-notifier: `Pull requests`: Read-only.
4. Organization permissions: niet nodig voor de basis, tenzij je org-brede acties wil doen buiten repo-scope.
5. Subscribe to events: niet vereist voor deze use-cases.
6. Klik `Create GitHub App`.

## 2) Private key genereren
1. In de App-instellingen: `Generate a private key`.
2. Bewaar het `.pem`-bestand veilig (inhoud kopieer je later naar een secret).
3. Noteer de `App ID` (numeriek).

## 3) App installeren op de organisatie
1. In de App-instellingen klik `Install App`.
2. Kies je organisatie (bijv. `ConductionNL`).
3. Selecteer:
   - `All repositories` of
   - `Only select repositories` (aanbevolen als je scope wilt beperken).
4. Rond de installatie af. De installatie creëert een `Installation ID` (deze hoef je niet handmatig in te vullen voor de gebruikte Action).

## 4) Secrets configureren
Zet de volgende secrets op het niveau waar je workflows draaien:
- In deze repo (of org-wide secrets wanneer meerdere repos het delen):
  - `GITHUB_APP_ID`: de numerieke App ID (bijv. `123456`).
  - `GITHUB_APP_PRIVATE_KEY`: de volledige PEM-inhoud (inclusief `-----BEGIN/END PRIVATE KEY-----`).

Tip: gebruik org secrets als meerdere repos dezelfde App gebruiken.

## 5) Workflows laten inloggen als de App
Deze repo gebruikt `actions/create-github-app-token@v1` om een installation token aan te maken:

```yaml
- name: Create GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.GITHUB_APP_ID }}
    private-key: ${{ secrets.GITHUB_APP_PRIVATE_KEY }}
    owner: ConductionNL   # vervang met jouw org-naam
```

Daarna wordt het token doorgegeven aan jobs/CLI:

```yaml
env:
  GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
```

In deze repo is dat al toegepast in:
- `.github/workflows/get-pr-data.yml` (PR-notifier)
- `.github/workflows/notify.yml` (issues-notifier)
- `.github/workflows/poke-all.yml` (orchestrator)

Pas waar nodig `owner: ConductionNL` aan naar jouw org.

## 6) Testen
1. Zet de secrets (`GITHUB_APP_ID`, `GITHUB_APP_PRIVATE_KEY`).
2. Ga naar de workflow in GitHub Actions en kies `Run workflow` (workflow_dispatch).
3. Controleer de logs:
   - Token-steps zouden slagen.
   - API-calls (enable/dispatch, PR- of issue-calls) moeten 200/201 opleveren.

## 7) Beveiliging en rotatie
- Houd `Actions: write` alleen aan wanneer echt nodig (orchestrator). Voor alleen lezen volstaat `Actions: read`.
- Beperk repo-toegang tot een subset als niet alle repos nodig zijn.
- Regenerate private key bij incidenten of periodiek voor rotatie.
- Verwijder persoonlijke PATs; gebruik de App organisatiebreed.

## 8) Veelvoorkomende fouten
- 403 Forbidden bij `gh api`: App niet geïnstalleerd op het doelrepo of permissies missen.
- 404 bij workflow endpoints: bestandsnaam/branch klopt niet (`ref=main` aanpassen indien je `default` anders is).
- Invalid key: PEM niet correct geplakt (inclusief header/footers).


