"""Gestion des "routes" FLASK et des données pour les films.
Fichier : gestion_films_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_BUDGET_164.database.database_tools import DBconnection
from APP_BUDGET_164.erreurs.exceptions import *
from APP_BUDGET_164.films.gestion_films_wtf_forms import FormWTFUpdateFilm, FormWTFAddFilm, FormWTFDeleteFilm

"""Ajouter un film grâce au formulaire "film_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "categorie_depense_update" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""

@app.route("/film_add", methods=['GET', 'POST'])
def film_add_wtf():
    # Objet formulaire pour AJOUTER une dépense
    form = FormWTFAddFilm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():

                # Récupérer les données du formulaire
                montant_depense = form.montant_depense.data.lower()
                date_depense = form.date_depense.data.lower()
                id_utilisateur = form.id_utilisateur.data.lower()
                id_compte = form.id_compte.data.lower()
                id_categorie = form.id_categorie.data.lower()
                description_depense = form.description_depense.data.lower()
                lieu_depense = form.lieu_depense.data.lower()

                # Préparer le dictionnaire des valeurs à insérer
                valeurs_insertion_dictionnaire = {
                    "id_utilisateur": id_utilisateur,
                    "id_categorie": id_categorie,
                    "id_compte": id_compte,
                    "montant_depense": montant_depense,
                    "date_depense": date_depense,
                    "description_depense": description_depense,
                    "lieu_depense": lieu_depense
                }

                strsql_insert_depense = """INSERT INTO t_depense (id_utilisateur, id_categorie, id_compte, Montant_depense, date_depense, description_depense, lieu_depense)
VALUES (%(id_utilisateur)s, %(id_categorie)s, %(id_compte)s, %(montant_depense)s, %(date_depense)s, %(description_depense)s, %(lieu_depense)s);"""

                # Utilisation d'une connexion à la base de données
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_depense, valeurs_insertion_dictionnaire)

                flash("Dépense ajoutée avec succès !", "success")
                return redirect(url_for('depense_afficher', order_by='DESC', id_depense_sel=0))

        except Exception as Exception_film_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(
                f"fichier : {Path(__file__).name} ; {film_add_wtf.__name__} ; {Exception_film_ajouter_wtf}"
            )

    return render_template("films/film_add_wtf.html", form=form)



"""Editer(update) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "compte_afficher.html"

Remarque :  Dans le champ "categorie_depense_update" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""
"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""
