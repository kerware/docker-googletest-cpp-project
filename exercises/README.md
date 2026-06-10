# Exercices d'application Docker + GoogleTest

Ces exercices prolongent les slides de formation. Ils doivent être réalisés dans le conteneur Docker pour éviter les écarts d'environnement Windows/Linux.

## Exercice 1 — Ajouter l'opération modulo

Objectif : ajouter `Calculator::modulo(int left, int right)`.

Contraintes :
- `10 % 3` doit retourner `1` ;
- modulo par zéro doit lever `std::invalid_argument` ;
- ajouter au moins 2 tests GoogleTest ;
- lancer les tests avec `docker compose run --rm cpp-tests`.

## Exercice 2 — Ajouter le parsing du modulo

Objectif : permettre à `ExpressionParser` d'évaluer `10%3`.

Contraintes :
- accepter les espaces : `10 % 3` ;
- conserver les tests existants ;
- ajouter un cas paramétré.

## Exercice 3 — Ajouter un test GoogleMock

Objectif : vérifier que `CalculatorService` journalise un succès pour `10%3`.

Contraintes :
- utiliser `StrictMock<MockOperationLogger>` ;
- vérifier `logSuccess("10%3", 1)`.

## Exercice 4 — Qualité conteneurisée

Objectif : lancer les contrôles qualité dans Docker.

Commandes attendues :

```bash
docker compose run --rm cpp-tests
docker compose run --rm static-analysis
docker compose run --rm coverage
```

Sous Windows PowerShell :

```powershell
.\scripts\test.ps1
.\scripts\analysis.ps1
.\scripts\coverage.ps1
```
