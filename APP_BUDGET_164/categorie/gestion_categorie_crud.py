"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_compte_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_BUDGET_164 import app
from APP_BUDGET_164.database.database_tools import DBconnection
from APP_BUDGET_164.erreurs.exceptions import *
from APP_BUDGET_164.categorie.gestion_categorie_wtf_forms import FormWTFAjouterCategorie, FormWTFDeleteCategorie, \
    FormWTFUpdateCategorie
from APP_BUDGET_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre, FormWTFDeleteGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /categorie_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/categorie_afficher/<string:order_by>/<int:id_categorie_sel>", methods=['GET', 'POST'])
def categorie_afficher(order_by, id_categorie_sel):
    data_categorie = []  # Variable par défaut
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # Vérifiez les valeurs pour 'order_by' et 'id_categorie_sel'
                if order_by == "ASC":
                    if id_categorie_sel == 0:
                        strsql_categorie_afficher = """SELECT * FROM t_categorie"""
                    else:
                        # Remplacez "t_genre" par le nom correct de la table
                        strsql_categorie_afficher = """SELECT * FROM t_categorie WHERE id_categorie = %(value_id_genre_selected)s"""
                        valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_categorie_sel}

                    mc_afficher.execute(strsql_categorie_afficher,
                                        valeur_id_genre_selected_dictionnaire if id_categorie_sel > 0 else None)
                    data_categorie = mc_afficher.fetchall()

                elif order_by == "DESC":
                    strsql_categorie_afficher = """SELECT * FROM t_categorie ORDER BY id_categorie DESC"""
                    mc_afficher.execute(strsql_categorie_afficher)
                    data_categorie = mc_afficher.fetchall()

                if not data_categorie:
                    flash("Aucune catégorie trouvée", "warning")

        except Exception as e:
            flash(f"Erreur lors de l'affichage des catégories: {str(e)}", "danger")

    return render_template("categorie/categorie_afficher.html", data=data_categorie)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/categorie_ajouter", methods=['GET', 'POST'])
def categorie_ajouter_wtf():
    form = (FormWTFAjouterCategorie())
    if request.method == "POST":
        try:
            if form.validate_on_submit():

                # Récupérer les données du formulaire
                nom_categorie = form.nom_categorie.data.lower()

                # Préparer le dictionnaire des valeurs à insérer
                valeurs_insertion_dictionnaire = {
                    "nom_categorie": nom_categorie
                }

                strsql_insert_genre = """INSERT INTO t_categorie
                                                (id_categorie, nom_categorie) 
                                                VALUES (null, %(nom_categorie)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")

                return redirect(url_for('categorie_afficher', order_by='DESC', id_categorie_sel=0))

        except Exception as Exception_categorie_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(
                f"fichier : {Path(__file__).name} ; {categorie_ajouter_wtf.__name__} ; {Exception_categorie_ajouter_wtf}"
            )

    return render_template("categorie/categorie_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "compte_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/categories_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/categorie_update", methods=['GET', 'POST'])
def categorie_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_categorie"
    id_categorie_update = request.values['id_categorie_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateCategorie()
    try:
        if request.method == "POST" and form_update.validate_on_submit():
            # Récupérer la valeur du champ depuis "categories_update_wtf.html" après avoir cliqué sur "SUBMIT".
            name_categorie_update = form_update.nom_genre_update_wtf.data
            name_categorie_update = name_categorie_update.lower()

            valeur_update_dictionnaire = {
                "value_id_categorie": id_categorie_update,
                "value_name_categorie": name_categorie_update
            }

            str_sql_update_categorie = """UPDATE t_categorie 
                                          SET nom_categorie = %(value_name_categorie)s
                                          WHERE id_categorie = %(value_id_categorie)s"""

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_categorie, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")

            return redirect(url_for('categorie_afficher', order_by="ASC", id_categorie_sel=0))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer les données de la catégorie à mettre à jour
            str_sql_id_categorie = "SELECT id_categorie, nom_categorie FROM t_categorie " \
                                   "WHERE id_categorie = %(value_id_categorie)s"
            valeur_select_dictionnaire = {"value_id_categorie": id_categorie_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_categorie, valeur_select_dictionnaire)
                data_nom_categorie = mybd_conn.fetchone()

            # Afficher la valeur sélectionnée dans les champs du formulaire "categories_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_categorie["nom_categorie"]

    except Exception as Exception_categorie_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{categorie_update_wtf.__name__} ; "
                                          f"{Exception_categorie_update_wtf}")

    return render_template("categorie/categorie_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "compte_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/categories_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/categorie_delete", methods=['GET', 'POST'])
def categorie_delete_wtf():
    data_depenses_attribuees_categorie_delete = None
    btn_submit_del = None

    id_categorie_delete = request.values['id_categorie_btn_delete_html']

    # Création d'une instance de formulaire pour la suppression de la catégorie sélectionnée
    form_delete = FormWTFDeleteCategorie()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("categorie_afficher", order_by="ASC", id_categorie_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupérer les données pour afficher à nouveau le formulaire de confirmation de suppression
                data_depenses_attribuees_categorie_delete = session['data_depenses_attribuees_categorie_delete']

                flash(f"Supprimer la catégorie de manière définitive de la base de données !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_categorie": id_categorie_delete}

                # Requête SQL pour supprimer les dépenses associées à cette catégorie
                str_sql_delete_depenses_categorie = """DELETE FROM t_depense WHERE id_categorie = %(value_id_categorie)s"""

                # Requête SQL pour supprimer la catégorie
                str_sql_delete_idcategorie = """DELETE FROM t_categorie WHERE id_categorie = %(value_id_categorie)s"""

                # Exécution des requêtes
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_depenses_categorie, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcategorie, valeur_delete_dictionnaire)

                flash(f"Catégorie définitivement supprimée !!", "success")

                # Rediriger vers l'affichage des catégories après la suppression
                return redirect(url_for('categorie_afficher', order_by="ASC", id_categorie_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_categorie": id_categorie_delete}

            # Requête pour récupérer les dépenses associées à cette catégorie
            str_sql_depenses_categorie_delete = """SELECT id_depense, Montant_depense, date_depense, description_depense, lieu_depense 
                                                  FROM t_depense WHERE id_categorie = %(value_id_categorie)s"""

            # Exécution de la requête
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_depenses_categorie_delete, valeur_select_dictionnaire)
                data_depenses_attribuees_categorie_delete = mydb_conn.fetchall()

                # Mémorisation des données pour afficher à nouveau le formulaire de confirmation de suppression
                session['data_depenses_attribuees_categorie_delete'] = data_depenses_attribuees_categorie_delete

        # Rendre le template avec les données nécessaires
        return render_template("categorie/categorie_delete_wtf.html",
                               form_delete=form_delete,
                               btn_submit_del=btn_submit_del,
                               data_depenses_attribuees=data_depenses_attribuees_categorie_delete)

    except Exception as Exception_categorie_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{categorie_delete_wtf.__name__} ; "
                                      f"{Exception_categorie_delete_wtf}")