# Documentation du projet

- ## Structure du Projet Flask

Ce document décrit la structure du projet Flask.

## Arborescence des fichiers
<pre>
plaintext . 
├── app/
│ ├── init.py
│ ├── routes.py 
│ ├── models.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── upload.html
│ ├── static/
│ │ ├── css/
│ │ │ ├── styles.css
│ │ ├── js/
│ │ │ ├── scripts.js
├── venv/
├── requirements.txt
├── config.py
├── run.py
</pre>
## Description des fichiers et dossiers

1. **app/** - Contient le code source de l'application Flask.
   - **__init__.py** - Initialise l'application Flask et configure les extensions.
   - **routes.py** - Définit les routes de l'application.
   - **models.py** - Contient les modèles de base de données.
   - **templates/** - Contient les fichiers HTML pour le rendu des pages.
     - **base.html** - Template de base pour les autres pages.
     - **index.html** - Page d'accueil.
     - **upload.html** - Page de téléchargement.
   - **static/** - Contient les fichiers statiques (CSS, JavaScript, images).
     - **css/** - Contient les fichiers CSS.
       - **styles.css** - Fichier de styles CSS.
     - **js/** - Contient les fichiers JavaScript.
       - **scripts.js** - Fichier de scripts JavaScript.

2. **venv/** - Environnement virtuel pour les dépendances Python.

3. **requirements.txt** - Liste des dépendances Python nécessaires pour le projet.

4. **config.py** - Fichier de configuration pour l'application Flask.

5. **run.py** - Script pour lancer l'application Flask.

## Installation et Exécution

1. Créez un environnement virtuel :
   
```bash
   python3 -m venv venv
   ```
2. Activez l'environnement vituel:
```bash
   source venv/bin/activate
   ```
3. Installer les dependances
```bash
   pip install -r requirements.txt
```
4. Lancer l'application
```bash
   python run.py
```

#### Utilisation
  -**Accédez à l'application via ```http://localhost:5000/```.**
  -**Utilisez la barre de navigation pour accéder aux différentes sections de l'application.**




## Routes de l'application Flask

Ce fichier décrit les différentes routes définies dans le fichier `routes.py` de l'application Flask.

### Routes

#### `/`

- **Méthode :** GET
- **Description :** Affiche la page de téléchargement de fichier.
- **Template :** `upload.html`
- **Paramètres :** Aucun

#### `/upload`

- **Méthode :** POST
- **Description :** Traite le fichier de transaction téléchargé et affiche les résultats.
- **Template :** `upload.html`
- **Paramètres :**
  - `name` (formulaire) : Nom de l'utilisateur.
  - `file` (formulaire) : Fichier de transaction à télécharger.
- **Réponse :** Affiche les résultats du traitement du fichier de transaction.

#### `/resultat_transactions.json`

- **Méthode :** GET
- **Description :** Renvoie le fichier JSON contenant les résultats des transactions.
- **Fichier :** `data/resultat_transactions.json`

#### `/error_lex.json`

- **Méthode :** GET
- **Description :** Renvoie le fichier JSON contenant les erreurs lexicales des transactions.
- **Fichier :** `data/error_lex.json`

#### `/history_success_transaction.json`

- **Méthode :** GET
- **Description :** Renvoie le fichier JSON contenant l'historique des transactions réussies.
- **Fichier :** `data/history_success_transaction.json`

#### `/history_error_transaction.json`

- **Méthode :** GET
- **Description :** Renvoie le fichier JSON contenant l'historique des transactions échouées.
- **Fichier :** `data/history_error_transaction.json`

#### `/success-transaction`

- **Méthode :** GET
- **Description :** Affiche la page des transactions réussies.
- **Template :** `success_transaction.html`

#### `/error-transaction`

- **Méthode :** GET
- **Description :** Affiche la page des transactions échouées.
- **Template :** `error_transaction.html`

#### `/favicon.ico`

- **Méthode :** GET
- **Description :** Renvoie le fichier de l'icône du site.
- **Fichier :** `Lexer_logo_teal.png`

# Documentation du fichier `bank_file_checker.py`

Ce fichier contient les fonctions et les définitions nécessaires pour analyser les fichiers de transactions bancaires et calculer les soldes.

## Tokens

- **SOLDE :** `:\d+,\d{2}`
- **CREDIT :** `\+\d+,\d{2}`
- **DEBIT :** `-\d+,\d{2}`
- **COMMENT :** `\#.*`
- **SEPARATOR :** `[-]{17}`

## Fonctions

### `find_column(input_text, token)`

- **Description :** Trouve la colonne d'un token dans le texte d'entrée.
- **Paramètres :**
  - `input_text` : Le texte d'entrée.
  - `token` : Le token pour lequel trouver la colonne.
- **Retour :** La colonne du token.

### `t_newline(t)`

- **Description :** Gère les nouvelles lignes dans le texte d'entrée.
- **Paramètres :**
  - `t` : Le token de nouvelle ligne.
- **Retour :** Aucun.

### `t_error(t)`

- **Description :** Gère les erreurs lexicales dans le texte d'entrée.
- **Paramètres :**
  - `t` : Le token d'erreur.
- **Retour :** Aucun.

### `calculate_balance(filename)`

- **Description :** Lit le fichier de transactions et calcule le solde.
- **Paramètres :**
  - `filename` : Le nom du fichier de transactions ou un objet `FileStorage`.
- **Retour :** "success" si le calcul est réussi, "error" sinon.

## Lexer

Le lexer est construit en utilisant `ply.lex` et est configuré pour analyser les fichiers de transactions bancaires en utilisant les tokens définis ci-dessus.

## Exemple d'utilisation

```python

from bank_file_checker import calculate_balance

result = calculate_balance('path/to/transaction/file.txt')
print(result)
```



### Détails de la fonction `calculate_balance`

La fonction `calculate_balance` lit le contenu d'un fichier de transactions et utilise un lexer pour analyser les transactions et calculer le solde. Voici les étapes principales :

1. **Lecture du fichier :** Le contenu du fichier est lu et passé au lexer.
2. **Initialisation :** Le solde initial est défini à 0.0 et une liste de transactions est créée.
3. **Analyse des tokens :** Le lexer parcourt chaque token et effectue les actions suivantes :
   - **SOLDE :** Met à jour le solde initial.
   - **CREDIT :** Ajoute la valeur du crédit au solde et enregistre la transaction.
   - **DEBIT :** Soustrait la valeur du débit du solde et enregistre la transaction.
   - **SEPARATOR :** Sépare les transactions et les enregistre dans le résultat.
   - **COMMENT :** Ignore les commentaires.
4. **Vérification du solde :** Si le solde devient négatif, une erreur est levée et enregistrée.
5. **Enregistrement des résultats :** Les résultats des transactions sont enregistrés dans des fichiers JSON.

### Gestion des erreurs

- **Erreurs lexicales :** Les erreurs lexicales sont capturées et enregistrées dans des fichiers JSON (`error_lex.json` et `history_error_transaction.json`).
- **Incohérences de solde :** Si le solde devient négatif après une transaction, une erreur est levée et enregistrée.

### Exemple de sortie

```json
{
  "solde_initial": 100.0,
  "transactions": {
    "transaction1": [
      {"transaction": "+50,00", "type": "credit", "solde_restant": 150.0},
      {"transaction": "-20,00", "type": "debit", "solde_restant": 130.0}
    ],
    "transaction2": [
      {"transaction": "+30,00", "type": "credit", "solde_restant": 160.0}
    ]
  }
}
```