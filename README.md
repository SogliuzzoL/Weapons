# Weapons — calculateur de vente GTA RP

Petite application Flask qui calcule le prix de revente d'armes et de pièces dans un serveur GTA RP, à partir d'un catalogue JSON (composants requis, volume de base, prix unitaires).

## Fonctionnement

- `weapons.json` contient deux catalogues : les **pièces** (prix unitaire) et les **armes** (volume de base et liste de composants).
- L'interface permet de choisir une arme, de régler le volume, puis de comparer le coût des composants au prix de vente calculé.
- Un second onglet fait le calcul inverse pour une pièce seule.

## Lancer

```bash
uv sync
uv run app.py
```

L'application écoute sur `http://127.0.0.1:5000`. Le catalogue se modifie directement dans `weapons.json`, sans toucher au code.

## Limites

- Une seule page, aucun stockage en base : les prix vivent dans le JSON.
- Bootstrap est chargé depuis un CDN, l'interface ne fonctionne pas hors ligne.
- Pas de tests automatisés.
