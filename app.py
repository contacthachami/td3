"""
TD Flask - Application de gestion de tâches (Todo List)
École Supérieure de Technologie d'Essaouira
Filière 3IASD

Ce fichier contient l'application Flask complète avec :
- Configuration de Flask et SQLAlchemy
- Modèle ORM Task
- Routes pour CRUD (Create, Read, Update, Delete)
- API JSON (bonus)
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ====================
# Configuration de l'application Flask
# ====================

app = Flask(__name__)

# Configuration de la base de données SQLite
# Le fichier todo.db sera créé dans le répertoire du projet
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

# Désactive le système de suivi des modifications (non nécessaire ici)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation de l'extension SQLAlchemy
# db est l'objet qui permet d'interagir avec la base de données
db = SQLAlchemy(app)


# ====================
# Modèle ORM : Task
# ====================

class Task(db.Model):
    """
    Modèle représentant une tâche dans la base de données.
    
    Attributs:
        id (int): Identifiant unique de la tâche (clé primaire)
        title (str): Titre de la tâche (maximum 200 caractères)
        done (bool): Statut de la tâche (True = faite, False = non faite)
        created_at (datetime): Date et heure de création (bonus)
    """
    
    # Colonnes de la table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Bonus: timestamp
    
    def __repr__(self):
        """Représentation textuelle de l'objet Task (utile pour le debugging)"""
        return f"<Task {self.id}: {self.title} (done={self.done})>"
    
    def to_dict(self):
        """
        Convertit l'objet Task en dictionnaire Python.
        Utile pour l'API JSON et la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant tous les attributs de la tâche
        """
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ====================
# Routes de l'application
# ====================

@app.route("/")
def home():
    """
    Route principale : affiche la liste de toutes les tâches.
    
    Flux de rendu :
    1. Interrogation de la base de données via Task.query.all()
    2. Tri des tâches par date de création (bonus)
    3. Passage de la liste au template home.html
    4. Jinja2 génère le HTML final
    
    Returns:
        str: HTML généré par le template home.html
    """
    # Récupération de toutes les tâches, triées par date de création (bonus: tri)
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    
    # Rendu du template avec la liste des tâches
    return render_template("home.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """
    Route pour ajouter une nouvelle tâche.
    Méthode HTTP : POST uniquement
    
    Flux :
    1. Lecture du titre depuis le formulaire (request.form)
    2. Création d'un nouvel objet Task
    3. Ajout à la session SQLAlchemy (db.session.add)
    4. Validation dans la base (db.session.commit)
    5. Redirection vers la page d'accueil (pattern Post/Redirect/Get)
    
    Returns:
        Response: Redirection vers la route home()
    """
    # Récupération du titre depuis le formulaire
    task_title = request.form.get("title")
    
    # Validation : vérifier que le titre n'est pas vide
    if task_title and task_title.strip():
        # Création d'une nouvelle tâche
        new_task = Task(title=task_title.strip())
        
        # Ajout à la session (prépare l'insertion)
        db.session.add(new_task)
        
        # Validation dans la base de données (exécute l'INSERT)
        db.session.commit()
    
    # Redirection vers la page d'accueil (méthode PRG: Post/Redirect/Get)
    # Cela évite la resoumission du formulaire si l'utilisateur actualise la page
    return redirect(url_for("home"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    """
    Route pour basculer l'état d'une tâche (fait ↔ non fait).
    
    Args:
        task_id (int): ID de la tâche à modifier
        
    Returns:
        Response: Redirection vers la page d'accueil
    """
    # Récupération de la tâche par son ID
    # get_or_404() retourne 404 si la tâche n'existe pas
    task = Task.query.get_or_404(task_id)
    
    # Inversion de l'état (True → False ou False → True)
    task.done = not task.done
    
    # Validation de la modification
    db.session.commit()
    
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """
    Route pour supprimer une tâche.
    
    Args:
        task_id (int): ID de la tâche à supprimer
        
    Returns:
        Response: Redirection vers la page d'accueil
    """
    # Récupération de la tâche
    task = Task.query.get_or_404(task_id)
    
    # Suppression de la tâche
    db.session.delete(task)
    
    # Validation de la suppression
    db.session.commit()
    
    return redirect(url_for("home"))


# ====================
# API JSON (Bonus)
# ====================

@app.route("/api/tasks", methods=["GET"])
def api_tasks():
    """
    Route API : retourne la liste des tâches au format JSON.
    (Exercice bonus)
    
    Cette route permet à d'autres applications ou scripts d'accéder
    aux données au format JSON.
    
    Returns:
        Response: JSON contenant la liste des tâches
    """
    # Récupération de toutes les tâches, triées par date
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    
    # Conversion en liste de dictionnaires
    tasks_list = [task.to_dict() for task in tasks]
    
    # Retour au format JSON
    return jsonify({
        "success": True,
        "count": len(tasks_list),
        "tasks": tasks_list
    })


# ====================
# Initialisation de la base de données
# ====================

def init_db():
    """
    Initialise la base de données et insère quelques tâches de démonstration.
    Cette fonction est appelée au démarrage de l'application.
    """
    with app.app_context():
        # Création de toutes les tables définies dans les modèles
        # Si les tables existent déjà, cette opération ne fait rien
        db.create_all()
        
        # Vérification : si aucune tâche n'existe, on en crée quelques-unes
        if Task.query.count() == 0:
            # Création de tâches initiales de démonstration
            tasks_init = [
                Task(title="Lire l'énoncé du TD", done=True),
                Task(title="Installer Flask", done=True),
                Task(title="Écrire le premier template", done=True),
                Task(title="Configurer SQLAlchemy", done=True),
                Task(title="Créer le modèle Task", done=True),
                Task(title="Implémenter les routes CRUD", done=False),
                Task(title="Ajouter du style CSS", done=False),
                Task(title="Tester l'application complète", done=False),
            ]
            
            # Ajout de toutes les tâches à la session
            for task in tasks_init:
                db.session.add(task)
            
            # Validation dans la base
            db.session.commit()
            
            print("✓ Base de données initialisée avec des tâches de démonstration")


# ====================
# Point d'entrée de l'application
# ====================

# Initialisation de la base de données au démarrage
# (Important pour les déploiements en production avec gunicorn)
init_db()

if __name__ == "__main__":
    # Lancement de l'application en mode debug (développement local uniquement)
    # debug=True permet :
    # - Le rechargement automatique en cas de modification du code
    # - L'affichage détaillé des erreurs dans le navigateur
    app.run(debug=True)
