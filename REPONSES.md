# 📘 Réponses aux Questions du TD Flask

**TD : Flask, Jinja2 et ORM avec SQLAlchemy**  
**Filière** : 3IASD - École Supérieure de Technologie d'Essaouira

---

## 🔹 Partie A : Mise en place de Flask et Jinja2

### Exercice 1 : Structure minimale du projet

#### Question 1 : Expliquez, en quelques phrases, le rôle de l'objet `app`.

**Réponse :**

L'objet `app` (créé par `app = Flask(__name__)`) est **l'instance centrale de l'application Flask**. Il joue plusieurs rôles essentiels :

1. **Point d'entrée de l'application** : C'est l'objet principal qui reçoit toutes les requêtes HTTP et les dirige vers les bonnes fonctions.

2. **Conteneur de configuration** : Il stocke toutes les configurations de l'application (base de données, mode debug, clés secrètes, etc.).

3. **Routeur** : Il associe les URLs aux fonctions Python grâce aux décorateurs `@app.route()`.

4. **Gestionnaire de contexte** : Il maintient le contexte de l'application pendant son exécution, permettant l'accès aux requêtes, sessions, etc.

Le paramètre `__name__` permet à Flask de déterminer l'emplacement racine de l'application pour localiser les ressources (templates, fichiers statiques).

---

#### Question 2 : Que se passe-t-il lorsqu'on accède à l'URL `/` dans le navigateur ?

**Réponse :**

Lorsqu'un utilisateur accède à `http://127.0.0.1:5000/` dans son navigateur :

1. **Le navigateur envoie une requête HTTP GET** vers le serveur Flask.

2. **Flask analyse la requête** et cherche une route correspondant à `/`.

3. **Flask trouve la route décorée par `@app.route("/")`** et exécute la fonction associée.

4. **La fonction retourne une chaîne de caractères** (dans l'exercice 1 : "Hello Flask TD").

5. **Flask crée une réponse HTTP** avec cette chaîne comme corps de réponse.

6. **Le navigateur reçoit la réponse** et affiche le texte "Hello Flask TD".

**Flux simplifié :**

```
Navigateur → HTTP GET / → Flask → route("/") → fonction → "Hello Flask TD" → Réponse HTTP → Navigateur
```

---

### Exercice 2 : Premier template Jinja2

#### Question 3 : Décrivez le flux de rendu entre la route `/` et le fichier `home.html`.

**Réponse :**

Le flux de rendu suit les étapes suivantes :

1. **Requête HTTP** : Le client (navigateur) envoie une requête GET vers `/`.

2. **Routage Flask** : Flask identifie la route `@app.route("/")` et exécute la fonction `home()`.

3. **Appel de `render_template()`** : La fonction appelle `render_template("home.html")`.

4. **Recherche du template** : Flask cherche le fichier dans le dossier `templates/` (convention Flask).

5. **Traitement par Jinja2** : Le moteur Jinja2 :
   - Lit le fichier HTML
   - Interprète les balises Jinja2 (`{% %}`, `{{ }}`)
   - Remplace les variables par leurs valeurs
   - Génère le HTML final

6. **Retour de la réponse** : Flask envoie le HTML généré au navigateur.

7. **Affichage** : Le navigateur interprète le HTML et affiche la page.

**Schéma :**

```
Client → GET / → Route Flask → render_template("home.html")
     → Jinja2 traite le template → HTML généré → Réponse HTTP → Client
```

---

#### Question 4 : Que se passe-t-il si vous changez le nom du fichier `home.html` sans modifier la route ?

**Réponse :**

Si on renomme `home.html` en `accueil.html` par exemple, mais que la route continue à appeler `render_template("home.html")`, **Flask lèvera une exception** :

```
jinja2.exceptions.TemplateNotFound: home.html
```

**Raison :** Flask cherche le fichier `home.html` dans le dossier `templates/`, ne le trouve pas, et génère une erreur 500 (Internal Server Error).

**Solution :** Modifier la route pour correspondre au nouveau nom :

```python
return render_template("accueil.html")
```

**Apprentissage :** Il est important de maintenir la cohérence entre les noms de fichiers et les appels dans le code.

---

### Exercice 3 : Variables et structures de contrôle dans le template

#### Question 5 : Donnez un exemple de condition Jinja2 que vous utilisez pour distinguer l'affichage fait / non fait.

**Réponse :**

Dans le template `home.html`, nous utilisons une structure conditionnelle `{% if %}` pour distinguer les tâches faites et non faites :

**Exemple 1 : Barrer le texte des tâches terminées**

```jinja2
{% if task.done %}
    <s>{{ task.title }}</s>
{% else %}
    {{ task.title }}
{% endif %}
```

**Exemple 2 : Changer l'icône selon l'état**

```jinja2
<span class="task-icon">
    {% if task.done %}
        ✅
    {% else %}
        ⭕
    {% endif %}
</span>
```

**Exemple 3 : Ajouter une classe CSS conditionnelle**

```jinja2
<li class="task-item {% if task.done %}task-done{% endif %}">
```

**Syntaxe générale :**

```jinja2
{% if condition %}
    <!-- code si vrai -->
{% else %}
    <!-- code si faux -->
{% endif %}
```

---

#### Question 6 : Expliquez pourquoi la liste `tasks` doit être construite en Python et non directement dans le template.

**Réponse :**

La liste `tasks` doit être construite en Python pour plusieurs raisons importantes :

1. **Séparation des responsabilités (MVC)** :
   - **Python (Contrôleur)** : Logique métier, accès aux données, calculs
   - **Jinja2 (Vue)** : Affichage uniquement, présentation
   - Cette séparation rend le code plus maintenable et testable

2. **Limitation de Jinja2** :
   - Jinja2 est un **moteur de templates**, pas un langage de programmation complet
   - Il ne peut pas accéder à la base de données directement
   - Il ne peut pas effectuer de requêtes SQL ou ORM

3. **Sécurité** :
   - Les templates sont souvent modifiés par des designers
   - Limiter la logique dans les templates réduit les risques d'erreurs

4. **Réutilisabilité** :
   - La même logique Python peut être utilisée pour différentes vues (HTML, JSON, etc.)
   - Facilite les tests unitaires

5. **Performance** :
   - Les opérations complexes sont plus rapides en Python
   - Jinja2 est optimisé pour le rendu, pas pour le traitement de données

**Exemple de mauvaise pratique (impossible en Jinja2) :**

```jinja2
{# IMPOSSIBLE : Jinja2 ne peut pas faire cela #}
{% tasks = Task.query.all() %}
```

**Bonne pratique :**

```python
# Python (app.py)
tasks = Task.query.all()
return render_template("home.html", tasks=tasks)
```

---

### Exercice 4 : Héritage de templates (base.html)

#### Question 7 : Expliquez en quoi l'héritage de modèles rend votre application plus facile à maintenir.

**Réponse :**

L'héritage de templates Jinja2 apporte plusieurs avantages majeurs pour la maintenabilité :

1. **DRY (Don't Repeat Yourself)** :
   - Le code HTML commun (header, footer, navigation) est écrit **une seule fois** dans `base.html`
   - Évite la duplication de code sur plusieurs pages
   - Exemple : modification du titre du site → 1 seule modification au lieu de 10+

2. **Cohérence visuelle** :
   - Toutes les pages partagent la même structure de base
   - Garantit une interface utilisateur uniforme
   - Changements globaux appliqués automatiquement partout

3. **Facilité de maintenance** :
   - Modifier le design global = modifier uniquement `base.html`
   - Ajouter un lien de navigation = modification dans un seul fichier
   - Réduit drastiquement le temps de maintenance

4. **Modularité** :
   - Chaque page enfant se concentre uniquement sur son contenu spécifique
   - Les blocs (`{% block %}`) définissent clairement les zones personnalisables
   - Code plus lisible et organisé

5. **Scalabilité** :
   - Facile d'ajouter de nouvelles pages tout en conservant la cohérence
   - Possibilité de créer plusieurs niveaux d'héritage

**Exemple concret :**

**base.html** (structure commune)

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header><!-- menu commun --></header>
    {% block content %}{% endblock %}
    <footer><!-- pied de page commun --></footer>
</body>
</html>
```

**home.html** (contenu spécifique)

```jinja2
{% extends "base.html" %}
{% block title %}Accueil{% endblock %}
{% block content %}
    <h1>Bienvenue</h1>
{% endblock %}
```

**Bénéfice :** Si nous devons ajouter Google Analytics, nous l'ajoutons dans `base.html` et **toutes les pages** l'auront automatiquement.

---

## 🔹 Partie B : Introduction à l'ORM avec SQLAlchemy

### Exercice 5 : Installation et configuration de Flask-SQLAlchemy

#### Question 8 : Expliquez le rôle de l'objet `db`.

**Réponse :**

L'objet `db` (créé par `db = SQLAlchemy(app)`) est **l'interface principale entre Flask et SQLAlchemy**. Ses rôles sont :

1. **Gestionnaire de connexions** :
   - Établit et maintient la connexion avec la base de données
   - Gère le pool de connexions pour optimiser les performances

2. **Factory de modèles** :
   - Fournit `db.Model` comme classe de base pour tous les modèles ORM
   - Exemple : `class Task(db.Model):`

3. **Définition des types de colonnes** :
   - Fournit les types : `db.Integer`, `db.String`, `db.Boolean`, etc.
   - Exemple : `title = db.Column(db.String(200))`

4. **Gestion des sessions** :
   - `db.session` : session pour les transactions
   - `db.session.add()` : ajouter un objet
   - `db.session.commit()` : valider les changements
   - `db.session.rollback()` : annuler en cas d'erreur

5. **Opérations DDL** :
   - `db.create_all()` : créer toutes les tables
   - `db.drop_all()` : supprimer toutes les tables

6. **Requêtes** :
   - Permet d'effectuer des requêtes via `Model.query.all()`, `Model.query.get()`, etc.

**Analogie :** `db` est comme un **pont** entre le monde Python (objets) et le monde SQL (tables).

---

### Exercice 6 : Définition du modèle Task

#### Question 9 : Où est créé le fichier de base de données ?

**Réponse :**

Le fichier de base de données `todo.db` est créé **dans le répertoire racine du projet**, là où se trouve `app.py`.

**Explication du chemin :**

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
```

- `sqlite:///` : protocole SQLite avec chemin relatif (3 slashes)
- `todo.db` : nom du fichier

**Chemin complet :** `c:\Users\HP\Desktop\web avancée\PROJECTS\TD3\todo.db`

**Alternatives :**

- Chemin absolu : `sqlite:///C:/path/to/todo.db`
- Mémoire (temporaire) : `sqlite:///:memory:`

**Note :** Le fichier est créé lors du premier appel à `db.create_all()`.

---

#### Question 10 : Que se passe-t-il si vous réexécutez `db.create_all()` alors que la table existe déjà ?

**Réponse :**

Si on réexécute `db.create_all()` alors que la table existe déjà :

**Comportement :** **Rien ne se passe** - SQLAlchemy **n'écrase pas** les tables existantes.

**Raison :** `create_all()` vérifie d'abord si la table existe :

- Si elle existe → ignore
- Si elle n'existe pas → crée

**Implications :**

1. ✅ **Sécurité** : Les données existantes sont **préservées**
2. ❌ **Limitations** : Si le modèle change (nouvelle colonne), `create_all()` **ne met pas à jour** la table

**Exemple :**

```python
# Première exécution
db.create_all()  # Crée la table 'task'

# Deuxième exécution
db.create_all()  # Ne fait rien, table déjà présente

# Modification du modèle (ajout d'une colonne)
class Task(db.Model):
    priority = db.Column(db.Integer)  # Nouvelle colonne

db.create_all()  # Ne met PAS à jour la table !
```

**Solution pour les migrations :** Utiliser **Flask-Migrate** (extension Alembic) pour gérer les modifications de schéma.

**Pour forcer la recréation :**

```python
db.drop_all()   # Supprime toutes les tables (PERTE DE DONNÉES !)
db.create_all() # Recrée les tables
```

---

### Exercice 7 : Insérer quelques tâches en base

#### Question 11 : Expliquez le rôle de `db.session.add()` et `db.session.commit()`.

**Réponse :**

Ces deux méthodes sont essentielles pour gérer les **transactions** avec la base de données.

---

**1. `db.session.add(objet)` :**

**Rôle :** **Ajoute un objet à la session** en attente.

**Caractéristiques :**

- L'objet est **marqué** pour être inséré dans la base
- **Aucune écriture** dans la base à ce stade
- Les objets sont stockés dans un "buffer" temporaire
- Permet de préparer plusieurs opérations avant validation

**Exemple :**

```python
t1 = Task(title="Tâche 1")
db.session.add(t1)  # t1 est en "pending", pas encore en base
```

**État :** L'objet est dans la session mais **pas encore dans la base de données**.

---

**2. `db.session.commit()` :**

**Rôle :** **Valide toutes les modifications** en attente et les écrit dans la base.

**Caractéristiques :**

- Exécute les requêtes SQL (INSERT, UPDATE, DELETE)
- Finalise la transaction
- Rend les changements **permanents**
- Libère les verrous de la base

**Exemple :**

```python
t1 = Task(title="Tâche 1")
t2 = Task(title="Tâche 2")
db.session.add(t1)
db.session.add(t2)
db.session.commit()  # Exécute 2 INSERT en base
```

---

**Workflow complet :**

```python
# 1. Créer des objets Python
task1 = Task(title="Lire le cours")
task2 = Task(title="Faire le TD")

# 2. Ajouter à la session (préparation)
db.session.add(task1)
db.session.add(task2)
# À ce stade : objets en mémoire, pas en base

# 3. Valider (écriture en base)
db.session.commit()
# Maintenant : objets enregistrés en base

# SQLAlchemy génère et exécute :
# INSERT INTO task (title, done) VALUES ('Lire le cours', 0);
# INSERT INTO task (title, done) VALUES ('Faire le TD', 0);
```

---

**Analogie du panier d'achat :**

- `add()` = ajouter un article au panier
- `commit()` = valider la commande et payer

---

**Gestion des erreurs :**

```python
try:
    task = Task(title="Test")
    db.session.add(task)
    db.session.commit()
except Exception as e:
    db.session.rollback()  # Annule toutes les modifications
    print(f"Erreur : {e}")
```

**`rollback()`** annule toutes les modifications en attente en cas d'erreur.

---

## 🔹 Partie C : Lier templates et ORM

### Exercice 8 : Liste des tâches depuis la base de données

#### Question 12 : Comparez les deux versions : sans ORM (liste de dicts) et avec ORM (liste d'objets). Quels avantages voyez-vous à la version ORM ?

**Réponse :**

**Comparaison :**

| Aspect                | Sans ORM (liste de dicts) | Avec ORM (objets SQLAlchemy)     |
| --------------------- | ------------------------- | -------------------------------- |
| **Type de données**   | `[{}, {}, ...]`           | `[Task(), Task(), ...]`          |
| **Accès aux données** | `task["title"]`           | `task.title`                     |
| **Modification**      | Dictionnaire mutable      | Objet avec méthodes              |
| **Validation**        | Manuelle                  | Automatique (types, contraintes) |
| **Relations**         | Gestion manuelle          | Relations automatiques           |

---

**Avantages de la version ORM :**

**1. Syntaxe plus claire et pythonique**

```python
# Sans ORM (dict)
title = task["title"]  # Risque de KeyError

# Avec ORM
title = task.title     # Plus lisible, autocomplétion IDE
```

**2. Validation automatique des types**

```python
# ORM valide automatiquement
task = Task(title=123)  # Sera converti en string
task.done = "oui"       # Erreur ou conversion selon config
```

**3. Méthodes et logique métier**

```python
class Task(db.Model):
    # ...

    def to_dict(self):
        """Conversion personnalisée"""
        return {...}

    def is_overdue(self):
        """Logique métier"""
        return self.deadline < datetime.now()
```

**4. Relations entre tables**

```python
class Task(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='tasks')

# Accès facile
task.user.name  # Pas besoin de JOIN manuel
```

**5. Requêtes expressives**

```python
# Sans ORM : SQL brut
cursor.execute("SELECT * FROM task WHERE done = 0")
rows = cursor.fetchall()

# Avec ORM : Python
tasks = Task.query.filter_by(done=False).all()
```

**6. Abstraction de la base de données**

- Changement de SQLite → PostgreSQL = modification de la config uniquement
- Pas de réécriture des requêtes SQL

**7. Protection contre les injections SQL**

```python
# ORM échappe automatiquement
title = request.form.get("title")
task = Task(title=title)  # Sécurisé

# vs SQL brut risqué :
# query = f"INSERT INTO task (title) VALUES ('{title}')"  # DANGER !
```

**8. Facilité de test**

```python
# Facile de mocker des objets ORM
from unittest.mock import Mock

mock_task = Mock(spec=Task)
mock_task.title = "Test"
```

**Inconvénients mineures de l'ORM :**

- Légère surcharge de performance (négligeable pour la plupart des apps)
- Courbe d'apprentissage initiale

**Conclusion :** L'ORM apporte **structure, sécurité, et maintenabilité** au prix d'une légère complexité initiale, largement compensée sur le long terme.

---

### Exercice 9 : Ajout d'une tâche via un formulaire

#### Question 13 : Pourquoi est-il préférable d'utiliser une redirection après le POST ?

**Réponse :**

L'utilisation d'une **redirection après POST** suit le pattern **PRG (Post/Redirect/Get)**. Voici pourquoi c'est une bonne pratique :

---

**Problème sans redirection :**

```python
@app.route("/add", methods=["POST"])
def add_task():
    # Traitement
    db.session.commit()
    return render_template("home.html", tasks=tasks)  # ❌ MAUVAIS
```

**Conséquence :** Si l'utilisateur **actualise la page** (F5), le navigateur affiche :

```
Confirmer la nouvelle soumission du formulaire
    [Renvoyer]  [Annuler]
```

Et si l'utilisateur clique "Renvoyer", **la même tâche sera ajoutée deux fois** !

---

**Solution avec redirection (PRG) :**

```python
@app.route("/add", methods=["POST"])
def add_task():
    # Traitement
    db.session.commit()
    return redirect(url_for("home"))  # ✅ BON
```

**Résultat :** Après la redirection, l'URL change vers `/` avec une requête GET.

---

**Avantages du pattern PRG :**

1. **Évite les doubles soumissions** :
   - Actualiser → recharge GET, pas POST
   - Pas de duplication de données

2. **URL propre** :
   - Après l'ajout, l'utilisateur est sur `/` (pas sur `/add`)
   - L'URL reflète ce que l'utilisateur voit

3. **Historique cohérent** :
   - Bouton "Retour" fonctionne correctement
   - Pas de comportement inattendu

4. **Respect des conventions HTTP** :
   - POST = modifier des données
   - GET = afficher des données

---

**Flux détaillé :**

```
1. Utilisateur soumet le formulaire
   → POST /add

2. Serveur traite et renvoie redirection 302
   → Location: /

3. Navigateur suit la redirection
   → GET /

4. Serveur renvoie la page mise à jour
   → affichage HTML

5. Utilisateur actualise (F5)
   → GET / (pas de resoumission !)
```

---

**Code complet :**

```python
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()

    # Redirection avec url_for (génère dynamiquement l'URL)
    return redirect(url_for("home"))  # → GET /
```

**Alternatives (moins bonnes) :**

```python
return redirect("/")  # Fonctionne mais moins flexible
```

---

#### Question 14 : Quelle méthode HTTP est utilisée pour le formulaire ? Aurait-on pu utiliser GET ici ?

**Réponse :**

**Méthode utilisée : POST**

```html
<form action="{{ url_for('add_task') }}" method="POST"></form>
```

---

**Pourquoi POST et pas GET ?**

| Critère        | POST                        | GET                            |
| -------------- | --------------------------- | ------------------------------ |
| **Visibilité** | Dans le corps de la requête | Dans l'URL (`?title=...`)      |
| **Sécurité**   | Caché dans les logs         | Visible dans l'historique/logs |
| **Taille**     | Illimitée (pratiquement)    | Limitée (~2000 caractères)     |
| **Cache**      | Jamais mis en cache         | Peut être mis en cache         |
| **Usage**      | Modifier des données        | Récupérer des données          |

---

**Réponse : NON, on ne devrait PAS utiliser GET ici.**

**Raisons :**

**1. Violation de la sémantique HTTP** :

- GET = demander des données (safe, idempotent)
- POST = modifier/créer des données
- Ajouter une tâche **modifie** la base → POST obligatoire

**2. Problèmes de sécurité** :

```
GET /add?title=Tâche%20importante
```

- L'URL apparaît dans l'historique du navigateur
- Visible dans les logs du serveur
- Peut être indexée par les moteurs de recherche (si mal configuré)

**3. Effets de bord non désirés** :

- Rafraîchir la page → nouvel ajout
- Préchargement des liens par certains navigateurs → ajouts accidentels
- Crawlers → ajouts non intentionnels

**4. Conventions RESTful** :

- POST /tasks → créer
- GET /tasks → lire
- PUT /tasks/:id → modifier
- DELETE /tasks/:id → supprimer

---

**Exemple du problème avec GET :**

```python
@app.route("/add", methods=["GET"])  # ❌ MAUVAIS
def add_task():
    title = request.args.get("title")
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("home"))

# URL : /add?title=Test
# Problème : rafraîchir = nouveau "Test"
# Google Bot visite /add?title=Spam → ajout en base !
```

---

**Quand utiliser GET ?**

GET convient pour :

- Recherche : `/search?q=flask`
- Filtres : `/tasks?status=done`
- Pagination : `/tasks?page=2`
- Partage d'URL : `/article?id=123`

**Règle d'or :** Si l'action **modifie** la base, utilisez **POST** (ou PUT/DELETE).

---

## 🔹 Partie D : Questions de synthèse

### Question 15 : Décrivez le flux complet lorsqu'un utilisateur...

#### a) Accède à la page d'accueil pour voir la liste des tâches

**Flux détaillé :**

```
1. Action utilisateur
   └─> Navigateur envoie : GET http://127.0.0.1:5000/

2. Réception par Flask
   └─> Serveur Flask reçoit la requête HTTP

3. Routage
   └─> Flask cherche la route correspondant à "/"
   └─> Trouve @app.route("/")
   └─> Exécute la fonction home()

4. Traitement côté Python
   └─> Exécution : tasks = Task.query.order_by(Task.created_at.desc()).all()
   └─> SQLAlchemy génère SQL : SELECT * FROM task ORDER BY created_at DESC
   └─> Récupère les résultats → liste d'objets Task

5. Rendu du template
   └─> Appel : render_template("home.html", tasks=tasks)
   └─> Jinja2 charge templates/home.html
   └─> Jinja2 traite :
       - {% extends "base.html" %} → charge base.html
       - {% for task in tasks %} → boucle sur la liste
       - {{ task.title }} → remplace par valeurs réelles
       - {% if task.done %} → conditions
   └─> Génère HTML final complet

6. Réponse HTTP
   └─> Flask crée réponse HTTP 200 OK
   └─> Corps : HTML généré
   └─> Headers : Content-Type: text/html; charset=utf-8

7. Affichage navigateur
   └─> Navigateur reçoit HTML
   └─> Parse le HTML
   └─> Demande style.css (GET /static/style.css)
   └─> Applique le CSS
   └─> Rend la page visible
```

**Chronologie :**

```
Client → GET / → Flask routing → home() → SQLAlchemy → DB
       ↓
DB → Objets Python → Jinja2 → HTML → HTTP Response → Client
```

---

#### b) Soumet le formulaire d'ajout de tâche

**Flux détaillé :**

```
1. Action utilisateur
   └─> Remplit le champ "title"
   └─> Clique sur "Ajouter"
   └─> Navigateur soumet : POST http://127.0.0.1:5000/add
       Body: title=Nouvelle+tâche

2. Réception par Flask
   └─> Serveur Flask reçoit POST /add

3. Routage
   └─> Flask cherche @app.route("/add", methods=["POST"])
   └─> Exécute add_task()

4. Traitement des données
   └─> task_title = request.form.get("title")
       Valeur : "Nouvelle tâche"
   └─> Validation : if task_title and task_title.strip()

5. Création de l'objet
   └─> new_task = Task(title=task_title.strip())
   └─> Objet Task créé en mémoire (id=None pour l'instant)

6. Persistance en base
   └─> db.session.add(new_task)
       → Task ajouté à la session SQLAlchemy
   └─> db.session.commit()
       → SQLAlchemy génère et exécute :
          INSERT INTO task (title, done, created_at)
          VALUES ('Nouvelle tâche', 0, '2026-02-13 15:30:00')
       → Base de données retourne l'ID généré
       → new_task.id est maintenant défini

7. Redirection (Pattern PRG)
   └─> return redirect(url_for("home"))
   └─> Flask renvoie HTTP 302 Found
       Location: http://127.0.0.1:5000/

8. Navigateur suit la redirection
   └─> GET http://127.0.0.1:5000/
   └─> (Passe directement au flux (c) ci-dessous)
```

---

#### c) Est redirigé vers la liste mise à jour

**Flux détaillé :**

```
1. Redirection automatique
   └─> Suite de (b) : navigateur reçoit 302
   └─> Lit header Location: /
   └─> Envoie automatiquement GET /

2. Nouvelle requête GET /
   └─> Même flux que (a)
   └─> MAIS cette fois la base contient la nouvelle tâche

3. Récupération avec nouvelle tâche
   └─> SQLAlchemy : SELECT * FROM task ORDER BY created_at DESC
   └─> Résultat inclut la tâche fraîchement ajoutée

4. Rendu
   └─> Boucle {% for task in tasks %}
   └─> Affiche TOUTES les tâches, y compris la nouvelle

5. Affichage final
   └─> Utilisateur voit sa nouvelle tâche en haut de la liste
   └─> URL dans la barre = http://127.0.0.1:5000/
       (et non /add)

6. Sécurité PRG
   └─> Si utilisateur appuie sur F5 :
       → Recharge GET / (affichage)
       → PAS de resoumission du formulaire
       → Pas de doublon créé
```

**Résumé visuel :**

```
[Formulaire] → POST /add → DB INSERT → Redirect 302
                                            ↓
                                        GET /
                                            ↓
                                       DB SELECT
                                            ↓
                                    [Liste complète]
```

---

### Question 16 : Citez trois avantages d'utiliser un ORM comme SQLAlchemy plutôt que du SQL brut partout.

**Réponse :**

**1. Abstraction et portabilité de la base de données**

**Sans ORM (SQL brut) :**

```python
# SQLite
cursor.execute("SELECT * FROM task LIMIT 10")

# PostgreSQL
cursor.execute("SELECT * FROM task LIMIT 10")

# SQL Server (syntaxe différente !)
cursor.execute("SELECT TOP 10 * FROM task")
```

**Avec ORM :**

```python
# Fonctionne sur SQLite, PostgreSQL, MySQL, SQL Server, Oracle...
tasks = Task.query.limit(10).all()
```

**Avantages :**

- Changement de SGBD = modification de l'URI uniquement
- Code réutilisable entre projets
- Syntaxe unifiée

---

**2. Sécurité contre les injections SQL**

**Sans ORM (DANGEREUX) :**

```python
user_input = request.form.get("title")

# ❌ VULNÉRABLE AUX INJECTIONS SQL
query = f"INSERT INTO task (title) VALUES ('{user_input}')"
cursor.execute(query)

# Si user_input = "'); DROP TABLE task; --"
# → Requête exécutée : INSERT INTO task (title) VALUES (''); DROP TABLE task; --')
# → TABLE SUPPRIMÉE ! 💀
```

**Avec ORM (SÛR) :**

```python
user_input = request.form.get("title")

# ✅ PROTÉGÉ AUTOMATIQUEMENT
task = Task(title=user_input)
db.session.add(task)
db.session.commit()

# SQLAlchemy échappe automatiquement les caractères dangereux
# Même avec input malveillant → inséré comme texte normal
```

**Avantages :**

- Protection automatique
- Pas besoin de se souvenir d'échapper les valeurs
- Réduction drastique des failles de sécurité

---

**3. Productivité et maintenabilité du code**

**Sans ORM :**

```python
# Requête complexe manuelle
query = """
    SELECT t.id, t.title, t.done, u.name
    FROM task t
    JOIN user u ON t.user_id = u.id
    WHERE t.done = 0 AND t.deadline < ?
    ORDER BY t.created_at DESC
"""
cursor.execute(query, (datetime.now(),))
rows = cursor.fetchall()

# Traitement manuel
tasks = []
for row in rows:
    tasks.append({
        'id': row[0],
        'title': row[1],
        'done': bool(row[2]),
        'user_name': row[3]
    })
```

**Avec ORM :**

```python
# Requête expressive et pythonique
tasks = Task.query\
    .join(User)\
    .filter(Task.done == False)\
    .filter(Task.deadline < datetime.now())\
    .order_by(Task.created_at.desc())\
    .all()

# Accès direct aux attributs
for task in tasks:
    print(task.title, task.user.name)
```

**Avantages :**

- Code plus lisible et pythonique
- Autocomplétion dans l'IDE
- Moins d'erreurs (types vérifiés)
- Relations gérées automatiquement (`task.user`)
- Réutilisable et testable
- Refactoring facilité

---

**Bonus : trois autres avantages**

**4. Gestion automatique des relations**

```python
# Définir une fois
user = db.relationship('User', backref='tasks')

# Utiliser partout
task.user.email  # Pas besoin de JOIN manuel
user.tasks       # Liste des tâches de l'utilisateur
```

**5. Migrations de schéma (avec Flask-Migrate)**

```bash
flask db migrate -m "Ajout colonne priority"
flask db upgrade
# Schéma mis à jour sans perte de données
```

**6. Lazy loading et optimisation**

```python
# Charge seulement si nécessaire
task.user  # SELECT user si pas déjà chargé

# Optimisation
Task.query.options(joinedload(Task.user)).all()  # Un seul SELECT
```

---

### Question 17 : Citez trois bonnes pratiques pour les templates Jinja2 dans une application Flask.

**Réponse :**

**1. Utiliser l'héritage de templates pour éviter la duplication**

**Mauvaise pratique :**

```jinja2
<!-- page1.html -->
<!DOCTYPE html>
<html>
<head><title>Page 1</title></head>
<body>
    <header><!-- menu copié --></header>
    <main>Contenu page 1</main>
    <footer><!-- footer copié --></footer>
</body>
</html>

<!-- page2.html -->
<!DOCTYPE html>
<html>
<head><title>Page 2</title></head>
<body>
    <header><!-- menu copié (duplication !) --></header>
    <main>Contenu page 2</main>
    <footer><!-- footer copié (duplication !) --></footer>
</body>
</html>
```

**Bonne pratique :**

```jinja2
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <header><!-- menu unique --></header>
    {% block content %}{% endblock %}
    <footer><!-- footer unique --></footer>
</body>
</html>

{# page1.html #}
{% extends "base.html" %}
{% block title %}Page 1{% endblock %}
{% block content %}Contenu page 1{% endblock %}

{# page2.html #}
{% extends "base.html" %}
{% block title %}Page 2{% endblock %}
{% block content %}Contenu page 2{% endblock %}
```

**Avantages :**

- Modification du header → un seul endroit
- Cohérence garantie
- Code DRY (Don't Repeat Yourself)

---

**2. Séparer la logique métier (Python) de la présentation (Jinja2)**

**Mauvaise pratique :**

```jinja2
{# Logique complexe dans le template ❌ #}
{% set total_price = 0 %}
{% for item in cart %}
    {% if item.discount %}
        {% set price = item.price * (1 - item.discount) %}
    {% else %}
        {% set price = item.price %}
    {% endif %}
    {% set total_price = total_price + (price * item.quantity) %}
{% endfor %}
<p>Total : {{ total_price }}€</p>
```

**Bonne pratique :**

```python
# app.py (logique métier)
@app.route("/cart")
def cart():
    items = get_cart_items()
    total_price = calculate_total(items)  # Logique ici
    return render_template("cart.html",
                         items=items,
                         total_price=total_price)
```

```jinja2
{# cart.html (affichage simple) #}
<p>Total : {{ total_price }}€</p>
```

**Avantages :**

- Templates lisibles
- Logique testable (tests unitaires Python)
- Réutilisable (API JSON, CLI, etc.)
- Séparation des responsabilités

---

**3. Utiliser `url_for()` au lieu de chemins codés en dur**

**Mauvaise pratique :**

```jinja2
{# Chemins en dur ❌ #}
<a href="/">Accueil</a>
<a href="/tasks/add">Ajouter</a>
<form action="/tasks/delete/5" method="POST">
<link rel="stylesheet" href="/static/style.css">
```

**Problèmes :**

- Si on change `/tasks/add` → `/add` : il faut modifier tous les templates
- Difficile de trouver toutes les occurrences
- Erreurs de frappe

**Bonne pratique :**

```jinja2
{# Utiliser url_for() ✅ #}
<a href="{{ url_for('home') }}">Accueil</a>
<a href="{{ url_for('add_task') }}">Ajouter</a>
<form action="{{ url_for('delete_task', task_id=task.id) }}" method="POST">
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

**Avantages :**

- Changement de route → modification dans app.py uniquement
- Flask génère l'URL correcte automatiquement
- Autocomplete dans l'IDE
- Erreurs détectées au démarrage (route inexistante)

---

**Bonus : trois autres bonnes pratiques**

**4. Échapper les variables pour éviter les failles XSS**

```jinja2
{# Jinja2 échappe automatiquement #}
{{ user_input }}  <!-- Sûr par défaut -->

{# Si besoin de HTML brut (ATTENTION !) #}
{{ safe_html | safe }}  <!-- Seulement si vous êtes SÛR que c'est sûr -->
```

**5. Utiliser des filtres Jinja2 pour formater les données**

```jinja2
{# Python : task.created_at = datetime(2026, 2, 13) #}

{# Mauvais : logique dans template #}
{{ task.created_at.strftime('%d/%m/%Y') }}  <!-- OK mais répétitif -->

{# Bon : filtre personnalisé #}
{{ task.created_at | date_format }}  <!-- Défini dans app.py -->
```

**6. Commenter le code template pour les mainteneurs**

```jinja2
{# Boucle sur les tâches actives uniquement #}
{% for task in tasks if not task.done %}
    {# Affichage de la tâche avec bouton d'action #}
    <li>{{ task.title }}</li>
{% endfor %}
```

---

### Question 18 : Proposez une amélioration possible de cette mini application.

**Réponse :**

Voici **une amélioration détaillée** (parmi de nombreuses possibilités) :

---

**Amélioration proposée : Système de catégories/tags pour organiser les tâches**

---

**1. Fonctionnalités ajoutées :**

- Créer des catégories (Travail, Personnel, Urgent, etc.)
- Assigner une ou plusieurs catégories à chaque tâche
- Filtrer les tâches par catégorie
- Afficher des statistiques par catégorie
- Couleurs visuelles pour chaque catégorie

---

**2. Modifications du modèle :**

```python
# Nouvelle table Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default="#3b82f6")  # Couleur hexadécimale

# Table d'association many-to-many
task_categories = db.Table('task_categories',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

# Modification du modèle Task
class Task(db.Model):
    # ... colonnes existantes ...

    # Relation many-to-many
    categories = db.relationship('Category',
                                secondary=task_categories,
                                backref='tasks')
```

---

**3. Nouvelles routes :**

```python
# Filtrer par catégorie
@app.route("/category/<int:category_id>")
def tasks_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    tasks = category.tasks
    return render_template("home.html", tasks=tasks, category=category)

# Gérer les catégories
@app.route("/categories")
def manage_categories():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)
```

---

**4. Interface utilisateur :**

```jinja2
{# Affichage des catégories sur chaque tâche #}
<li class="task-item">
    <span>{{ task.title }}</span>

    {# Badges de catégories #}
    <div class="categories">
        {% for category in task.categories %}
            <span class="badge" style="background-color: {{ category.color }}">
                {{ category.name }}
            </span>
        {% endfor %}
    </div>
</li>

{# Menu de filtrage #}
<nav>
    <a href="{{ url_for('home') }}">Toutes</a>
    {% for category in all_categories %}
        <a href="{{ url_for('tasks_by_category', category_id=category.id) }}">
            {{ category.name }} ({{ category.tasks|length }})
        </a>
    {% endfor %}
</nav>
```

---

**5. Avantages de cette amélioration :**

✅ **Organisation** : Tâches groupées logiquement  
✅ **Productivité** : Filtrage rapide par contexte  
✅ **Visibilité** : Vue d'ensemble par domaine  
✅ **Flexibilité** : Une tâche peut appartenir à plusieurs catégories  
✅ **Scalabilité** : Fonctionne avec des centaines de tâches

---

**Autres améliorations possibles :**

1. **Dates d'échéance** (deadline) avec alertes
2. **Niveaux de priorité** (haute, moyenne, basse)
3. **Authentification multi-utilisateurs**
4. **Partage de tâches entre utilisateurs**
5. **Recherche full-text**
6. **Export CSV/PDF**
7. **Notifications par email**
8. **Statistiques et graphiques**
9. **Glisser-déposer pour réorganiser**
10. **Application mobile (React Native/Flutter)**

---

## 📝 Conclusion

Ce TD a permis de mettre en pratique les concepts fondamentaux de Flask, Jinja2 et SQLAlchemy :

- ✅ Architecture MVC
- ✅ Routage HTTP et méthodes
- ✅ Templates et héritage
- ✅ ORM et opérations CRUD
- ✅ Bonnes pratiques (PRG, séparation logique/présentation)
- ✅ API REST JSON

L'application développée démontre une compréhension complète du flux de rendu Flask et de la persistance des données avec SQLAlchemy.

---

**Date de réalisation :** 13 février 2026  
**Filière :** 3IASD - EST Essaouira
