# Projet C++ GoogleTest exécuté avec Docker

Ce projet illustre une chaîne professionnelle pour exécuter des tests C++ avec **GoogleTest/GoogleMock** dans un conteneur Docker, y compris sous **Windows avec Docker Desktop**.

L'objectif est de garantir que tous les développeurs et la CI utilisent le même environnement Linux de compilation, de test et d'analyse.

## 1. Contenu du projet

```text
.
├── CMakeLists.txt
├── Dockerfile
├── docker-compose.yml
├── include/
│   ├── Calculator.hpp
│   ├── ExpressionParser.hpp
│   └── OperationLogger.hpp
├── src/
│   ├── Calculator.cpp
│   ├── CalculatorService.cpp
│   ├── ExpressionParser.cpp
│   └── main.cpp
├── tests/
│   ├── CalculatorTest.cpp
│   ├── ExpressionParserTest.cpp
│   ├── CalculatorParameterizedTest.cpp
│   └── CalculatorMockTest.cpp
├── scripts/
│   ├── build.sh
│   ├── test.sh
│   ├── docker-test.sh
│   ├── docker-coverage.sh
│   ├── docker-analysis.sh
│   ├── test.ps1
│   ├── coverage.ps1
│   └── analysis.ps1
├── exercises/
├── solutions/
├── .github/workflows/docker-cpp-tests.yml
└── .gitlab-ci.yml
```

## 2. Prérequis Windows

Installer :

1. **Docker Desktop for Windows** ;
2. activer le backend **WSL2** ;
3. installer Git ;
4. ouvrir PowerShell dans le dossier du projet.

Vérification :

```powershell
docker --version
docker compose version
```

## 3. Lancer les tests sous Windows

Depuis PowerShell :

```powershell
.\scripts\test.ps1
```

Ou directement :

```powershell
docker compose run --rm cpp-tests
```

Cette commande :

1. construit l'image Docker ;
2. configure CMake ;
3. compile le projet ;
4. lance les tests GoogleTest via CTest ;
5. génère un rapport JUnit dans `reports/ctest-junit.xml` ;
6. convertit ce résultat en HTML visible dans `reports/googletest/index.html`.

## 4. Lancer les tests sous Linux/macOS

```bash
./scripts/docker-test.sh
```

Ou :

```bash
docker compose run --rm cpp-tests
```

## 5. Commandes Docker Compose disponibles

### Tests unitaires et mocks

```bash
docker compose run --rm cpp-tests
```

### Couverture de code

```bash
docker compose run --rm coverage
```

Rapport généré :

```text
reports/coverage/index.html
```

Sous Windows :

```powershell
.\scripts\coverage.ps1
```

### Analyse statique

```bash
docker compose run --rm static-analysis
```

Sous Windows :

```powershell
.\scripts\analysis.ps1
```

### Sanitizers

```bash
docker compose run --rm sanitizers
```

### Shell interactif dans l'environnement C++

```bash
docker compose run --rm shell
```

Puis dans le conteneur :

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

### Jenkins dans Docker

Le projet inclut désormais un service Jenkins dans `docker-compose.yml` et un `Jenkinsfile` à la racine.

Démarrage du conteneur Jenkins :

```bash
docker compose up -d jenkins
```

Puis ouvrir l'interface Jenkins sur :

```text
http://localhost:8080
```

Créez un job Pipeline/Multi-branch Pipeline pointant sur ce dépôt. Le pipeline utilisera le `Jenkinsfile` et exécutera les commandes :

```bash
docker compose build

docker compose run --rm cpp-tests

docker compose run --rm static-analysis

docker compose run --rm clang-tidy

docker compose run --rm valgrind

docker compose run --rm coverage

docker compose run --rm sanitizers
```

Les artefacts générés sont accessibles dans `reports/`.

> Pour déclencher l'exécution sur un commit, configurez un webhook Git ou activez la détection périodique dans Jenkins.

## 6. Dockerfile expliqué

Le `Dockerfile` utilise Ubuntu 24.04 et installe :

- `build-essential` : compilateur GCC/G++ ;
- `cmake` : configuration du build ;
- `ninja-build` : générateur rapide ;
- `libgtest-dev` et `libgmock-dev` : GoogleTest/GoogleMock ;
- `lcov` et `gcovr` : couverture ;
- `cppcheck` et `clang-tidy` : analyse statique ;
- `valgrind` : diagnostic mémoire.

Extrait :

```dockerfile
FROM ubuntu:24.04 AS cpp-test-env

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        libgtest-dev \
        libgmock-dev \
        lcov \
        gcovr \
        cppcheck \
        clang-tidy \
        valgrind
```

## 7. docker-compose.yml expliqué

Le fichier `docker-compose.yml` définit plusieurs services spécialisés :

| Service | Rôle |
|---|---|
| `cpp-tests` | configure, compile et lance les tests |
| `coverage` | compile avec couverture et génère un rapport HTML |
| `static-analysis` | lance `cppcheck` |
| `sanitizers` | compile avec AddressSanitizer et UndefinedBehaviorSanitizer |
| `shell` | ouvre un shell dans l'environnement C++ |

Le volume :

```yaml
volumes:
  - .:/workspace
```

permet de monter le projet Windows dans le conteneur Linux.

## 8. Tests inclus

### Tests GoogleTest simples

```cpp
TEST(CalculatorTest, AddsTwoPositiveNumbers) {
    Calculator calculator;
    EXPECT_EQ(calculator.add(2, 3), 5);
}
```

### Tests d'exception

```cpp
TEST(CalculatorTest, ThrowsWhenDividingByZero) {
    Calculator calculator;
    EXPECT_THROW(static_cast<void>(calculator.divide(10, 0)), std::invalid_argument);
}
```

### Tests paramétrés

```cpp
class ExpressionParameterizedTest : public ::testing::TestWithParam<ExpressionCase> {};

TEST_P(ExpressionParameterizedTest, EvaluatesExpression) {
    ExpressionParser parser;
    const auto& param = GetParam();
    EXPECT_EQ(parser.evaluate(param.expression), param.expected);
}
```

### Tests GoogleMock

```cpp
class MockOperationLogger : public OperationLogger {
public:
    MOCK_METHOD(void, logSuccess, (const std::string& expression, int result), (override));
    MOCK_METHOD(void, logFailure, (const std::string& expression, const std::string& reason), (override));
};
```

```cpp
EXPECT_CALL(logger, logSuccess("2+3", 5)).Times(1);
```

## 9. Pipeline GitHub Actions

Le workflow `.github/workflows/docker-cpp-tests.yml` :

1. construit l'image Docker ;
2. lance les tests ;
3. lance l'analyse statique ;
4. lance les sanitizers ;
5. génère la couverture ;
6. publie les rapports en artefacts.

## 10. Pipeline GitLab CI

Le fichier `.gitlab-ci.yml` utilise Docker-in-Docker pour lancer les mêmes services Docker Compose dans GitLab CI.

## 11. Exercices et corrigés

Les exercices sont disponibles dans :

```text
exercises/README.md
```

Les corrigés indicatifs sont disponibles dans :

```text
solutions/
```

L'exercice principal consiste à ajouter l'opération modulo dans :

- `Calculator` ;
- `ExpressionParser` ;
- les tests GoogleTest ;
- les tests GoogleMock.

## 12. Commande de validation complète

Sous Windows PowerShell :

```powershell
.\scripts\test.ps1
.\scripts\analysis.ps1
.\scripts\coverage.ps1
docker compose run --rm sanitizers
```

Sous Linux/macOS :

```bash
./scripts/docker-test.sh
./scripts/docker-analysis.sh
./scripts/docker-coverage.sh
docker compose run --rm sanitizers
```

## 13. Points d'attention sous Windows

- Utiliser Docker Desktop avec WSL2.
- Éviter les chemins avec caractères spéciaux ou espaces excessifs.
- Lancer les scripts depuis PowerShell dans le dossier racine du projet.
- Le premier build peut prendre du temps car l'image Ubuntu installe les dépendances.
- Les fichiers générés dans `reports/` sont visibles directement depuis Windows.

## 14. Nettoyage

```bash
docker compose down --remove-orphans
docker image rm docker-googletest-cpp:latest
rm -rf build build-coverage build-asan reports
```

Sous PowerShell :

```powershell
docker compose down --remove-orphans
Remove-Item -Recurse -Force build, build-coverage, build-asan, reports -ErrorAction SilentlyContinue
```
