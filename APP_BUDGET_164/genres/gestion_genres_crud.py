"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genre_crud.py
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
from APP_BUDGET_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_BUDGET_164.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_BUDGET_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_utilisateur_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_utilisateur_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_utilisateur_sel == 0:
                    strsql_genres_afficher = """SELECT * FROM t_utilisateur"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_utilisateur_sel}
                    strsql_genres_afficher = """SELECT id_utilisateur, nom_utilisateur FROM t_utilisateur WHERE id_utilisateur = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT id_utilisateur, nom_utilisateur FROM t_utilisateur ORDER BY id_utilisateur DESC"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_utilisateur_sel == 0:
                    flash("""La table "t_utilisateur" est vide. !!""", "warning")
                elif not data_genres and id_utilisateur_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le t_utilisateur demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_utilisateur" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données utilisateurs affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/genres_afficher.html", data=data_genres)


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


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                # Récupérer les données du formulaire
                nom_utilisateur = form.nom_utilisateur.data.lower()
                prénom_utilisateur = form.prenom_utilisateur.data.lower()
                password_utilisateur = form.password_utilisateur.data
                email_utilisateur = form.email_utilisateur.data

                # Préparer le dictionnaire des valeurs à insérer
                valeurs_insertion_dictionnaire = {
                    "nom_utilisateur": nom_utilisateur,
                    "prénom_utilisateur": prénom_utilisateur,
                    "password_utilisateur": password_utilisateur,
                    "email_utilisateur": email_utilisateur
                }

                strsql_insert_genre = """INSERT INTO t_utilisateur 
                                                (id_utilisateur, prenom_utilisateur, nom_utilisateur, password_utilisateur, email_utilisateur) 
                                                VALUES (null, %(prénom_utilisateur)s, %(nom_utilisateur)s, %(password_utilisateur)s,  %(email_utilisateur)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")

                return redirect(url_for('genres_afficher', order_by='ASC', id_utilisateur_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(
                f"fichier : {Path(__file__).name} ; {genres_ajouter_wtf.__name__} ; {Exception_genres_ajouter_wtf}"
            )

    return render_template("genres/genres_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genre_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genres_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_utilisateur"
    id_user_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur des champs depuis "user_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_user_update = form_update.nom_user_update_wtf.data
            prenom_user_update = form_update.prenom_user_update_wtf.data
            email_user_update = form_update.email_user_update_wtf.data
            password_user_update = form_update.password_user_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_user": id_user_update,
                "value_nom_user": nom_user_update,
                "value_prenom_user": prenom_user_update,
                "value_email_user": email_user_update,
                "value_password_user": password_user_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_user = """
                UPDATE t_utilisateur SET
                nom_utilisateur = %(value_nom_user)s,
                prenom_utilisateur = %(value_prenom_user)s,
                email_utilisateur = %(value_email_user)s,
                password_utilisateur = %(value_password_user)s
                WHERE id_utilisateur = %(value_id_user)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_user, valeur_update_dictionnaire)

            flash(f"Utilisateur mis à jour !!", "success")
            print(f"Utilisateur mis à jour !!")

            # Redirection après mise à jour
            return redirect(url_for('genres_afficher', order_by="ASC", id_utilisateur_sel=0))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer toutes les informations de l'utilisateur
            str_sql_id_user = """
                SELECT id_utilisateur, nom_utilisateur, prenom_utilisateur, email_utilisateur, password_utilisateur
                FROM t_utilisateur
                WHERE id_utilisateur = %(value_id_user)s
            """
            valeur_select_dictionnaire = {"value_id_user": id_user_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_user, valeur_select_dictionnaire)
            data_user = mybd_conn.fetchone()
            print("data_user ", data_user, " type ", type(data_user))

            # Remplir le formulaire avec les valeurs actuelles de l'utilisateur
            form_update.nom_user_update_wtf.data = data_user["nom_utilisateur"]
            form_update.prenom_user_update_wtf.data = data_user["prenom_utilisateur"]
            form_update.email_user_update_wtf.data = data_user["email_utilisateur"]
            form_update.password_user_update_wtf.data = data_user["password_utilisateur"]

    except Exception as Exception_user_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_user_update_wtf}")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genre_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genres_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""
@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_depenses_attribuees_genre_delete = None
    btn_submit_del = None

    id_genre_delete = request.values['id_genre_btn_delete_html']

    # Création d'une instance de formulaire pour la suppression de la catégorie sélectionnée
    form_delete = FormWTFDeleteGenre()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_utilisateur_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupérer les données pour afficher à nouveau le formulaire de confirmation de suppression
                data_depenses_attribuees_genre_delete = session['data_depenses_attribuees_genre_delete']

                flash(f"Supprimer la catégorie de manière définitive de la base de données !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}

                # Suppression des enregistrements liés dans t_utilisateur_comptes
                str_sql_delete_utilisateur_comptes = """DELETE FROM t_utilisateur_comptes WHERE id_utilisateur = %(value_id_genre)s """

                # Requête pour supprimer les dépenses associées à cet utilisateur
                str_sql_delete_depenses_utilisateur = """DELETE FROM t_depense WHERE id_utilisateur = %(value_id_genre)s """

                # Requête pour supprimer les revenus associés à cet utilisateur
                str_sql_delete_revenus_utilisateur = """DELETE FROM t_revenu WHERE id_utilisateur = %(value_id_genre)s """

                # Requête pour supprimer les comptes associés à cet utilisateur
                str_sql_delete_comptes_utilisateur = """DELETE FROM t_compte WHERE id_utilisateur = %(value_id_genre)s """

                # Requête pour supprimer l'utilisateur lui-même
                str_sql_delete_utilisateur = """DELETE FROM t_utilisateur WHERE id_utilisateur = %(value_id_genre)s """

                # Exécution des requêtes dans le bon ordre
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_utilisateur_comptes, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_depenses_utilisateur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_revenus_utilisateur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_comptes_utilisateur, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_utilisateur, valeur_delete_dictionnaire)

                flash(f"Utilisateur définitivement supprimé !!", "success")

                # Rediriger vers l'affichage des catégories après la suppression
                return redirect(url_for('genres_afficher', order_by="ASC", id_utilisateur_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}

            # Requête pour récupérer les dépenses associées à cet utilisateur
            str_sql_depenses_genre_delete = """SELECT id_depense, Montant_depense, date_depense, description_depense, lieu_depense 
                                                  FROM t_depense WHERE id_utilisateur  = %(value_id_genre)s"""

            # Exécution de la requête
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_depenses_genre_delete, valeur_select_dictionnaire)
                data_depenses_attribuees_genre_delete = mydb_conn.fetchall()

                # Mémorisation des données pour afficher à nouveau le formulaire de confirmation de suppression
                session['data_depenses_attribuees_genre_delete'] = data_depenses_attribuees_genre_delete

        # Rendre le template avec les données nécessaires
        return render_template("genres/genre_delete_wtf.html",
                               form_delete=form_delete,
                               btn_submit_del=btn_submit_del,
                               data_depenses_attribuees=data_depenses_attribuees_genre_delete)

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")
