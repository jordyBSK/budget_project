"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_BUDGET_164.database.database_tools import DBconnection
from APP_BUDGET_164.erreurs.exceptions import *
from APP_BUDGET_164.films.gestion_films_wtf_forms import FormWTFUpdateFilm, FormWTFDeleteFilm

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@app.route("/films_genres_afficher/<int:id_film_sel>", methods=['GET', 'POST'])
def films_genres_afficher(id_film_sel):
    print(" films_genres_afficher id_film_sel ", id_film_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_films_afficher_data = """
SELECT 
    d.id_depense,
    u.nom_utilisateur,
    u.prenom_utilisateur,
    c.nom_categorie, 
    a.nom_compte,
    d.Montant_depense,
    d.date_depense,
    d.description_depense,
    d.lieu_depense
FROM 
    t_depense d
    INNER JOIN t_utilisateur u
    ON d.id_utilisateur = u.id_utilisateur
    INNER JOIN t_categorie c
    ON d.id_categorie = c.id_categorie
    INNER JOIN t_compte a
    ON d.id_compte = a.id_compte
"""

                if id_film_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_genres_films_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_film_selected": id_film_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_films_afficher_data += """ HAVING id_depense= %(value_id_film_selected)s"""

                    mc_afficher.execute(strsql_genres_films_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_films_afficher = mc_afficher.fetchall()
                print("data_genres ", data_genres_films_afficher, " Type : ", type(data_genres_films_afficher))

                # Différencier les messages.
                if not data_genres_films_afficher and id_film_sel == 0:
                    flash("""La table "t_depense" est vide. !""", "warning")
                elif not data_genres_films_afficher and id_film_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"La depense {id_film_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données dépenses affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {films_genres_afficher.__name__} ;"
                                               f"{Exception_films_genres_afficher}")

    print("films_genres_afficher  ", data_genres_films_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("films_genres/films_genres_afficher.html", data=data_genres_films_afficher)




"""
    nom: update_genre_film_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@app.route("/film_update", methods=['GET', 'POST'])
def film_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_depense"
    id_depense_update = request.values['id_film_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_film = FormWTFUpdateFilm()
    try:
        if request.method == "POST" and form_update_film.submit.data:
            # Récupèrer la valeur du champ depuis "categories_update_wtf.html" après avoir cliqué sur "SUBMIT".
            categorie_depense_update = form_update_film.categorie_depense_update_wtf.data
            id_compte_update = form_update_film.id_compte_update_wtf.data
            montant_depense_update = form_update_film.montant_depense_update_wtf.data
            lieu_depense_update = form_update_film.cover_link_film_update_wtf.data
            date_depense_update = form_update_film.date_depense_update_wtf.data

            valeur_update_dictionnaire = {
                "categorie": categorie_depense_update,
                "compte": id_compte_update,
                "montant": montant_depense_update,
                "date": date_depense_update,
                "lieu": lieu_depense_update,
                "id_depense": id_depense_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_film = """UPDATE t_depense SET id_categorie = %(categorie)s,
                                                            id_compte = %(compte)s,
                                                            Montant_depense = %(montant)s,
                                                            date_depense = %(date)s,
                                                            lieu_depense = %(lieu)s
                                                            WHERE id_depense = %(id_depense)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_film, valeur_update_dictionnaire)

            flash("Donnée mise à jour !!", "success")
            print("Donnée mise à jour !!")

            return redirect(url_for('films_genres_afficher', id_film_sel=0))

        elif request.method == "GET":
            str_sql_id_film = "SELECT * FROM t_depense WHERE id_depense = %(value_id_film)s"
            valeur_select_dictionnaire = {"value_id_film": id_depense_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_film, valeur_select_dictionnaire)

            data_film = mybd_conn.fetchone()
            print("data_film ", data_film, " type ", type(data_film))

            # Vérifiez la présence de chaque clé avant de les utiliser
            form_update_film.categorie_depense_update_wtf.data = data_film.get("id_categorie", None)
            form_update_film.id_compte_update_wtf.data = data_film.get("id_compte", None)
            form_update_film.montant_depense_update_wtf.data = data_film.get("Montant_depense", None)
            form_update_film.cover_link_film_update_wtf.data = data_film.get("lieu_depense", None)
            form_update_film.date_depense_update_wtf.data = data_film.get("date_depense", None)
            form_update_film.description_depense_update_wtf.data = data_film.get("description_depense", None)

    except Exception as Exception_film_update_wtf:
        print(f"Erreur: {Exception_film_update_wtf}")
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_update_wtf.__name__} ; "
                                     f"{Exception_film_update_wtf}")

    return render_template("films/film_update_wtf.html", form_update_film=form_update_film)


@app.route("/film_delete", methods=['GET', 'POST'])
def film_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_film_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_depense"
    id_depense_delete = request.values['id_film_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_film = FormWTFDeleteFilm()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_film.submit_btn_annuler.data:
            return redirect(url_for("films_genres_afficher", id_film_sel=0))

        if form_delete_film.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_film_delete = session['data_film_delete']
            print("data_film_delete ", data_film_delete)

            flash(f"Effacer la dépense de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_film.submit_btn_del_film.data:
            valeur_delete_dictionnaire = {"value_id_depense": id_depense_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_utilisateur_depenses = """DELETE FROM t_utilisateur_depenses WHERE id_depense = %(value_id_depense)s"""
            str_sql_delete_film = """DELETE FROM t_depense WHERE id_depense = %(value_id_depense)s"""

            # Supprimer les dépendances avant de supprimer la dépense
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_utilisateur_depenses, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_film, valeur_delete_dictionnaire)

            flash(f"Dépense définitivement effacée !!", "success")
            print(f"Dépense définitivement effacée !!")

            # afficher les données
            return redirect(url_for('films_genres_afficher', id_film_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_depense": id_depense_delete}
            print(id_depense_delete, type(id_depense_delete))

            # Requête qui affiche le film qui doit être effacé.
            str_sql_genres_films_delete = """SELECT 
    d.id_depense,
    u.nom_utilisateur,
    u.prenom_utilisateur,
    c.nom_categorie, 
    a.nom_compte,
    d.Montant_depense,
    d.date_depense,
    d.description_depense,
    d.lieu_depense
FROM 
    t_depense d
    INNER JOIN t_utilisateur u
    ON d.id_utilisateur = u.id_utilisateur
    INNER JOIN t_categorie c
    ON d.id_categorie = c.id_categorie
    INNER JOIN t_compte a
    ON d.id_compte = a.id_compte
where id_depense = %(value_id_depense)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_film_delete = mydb_conn.fetchall()
                print(data_film_delete)
                print("data_film_delete...", data_film_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_film_delete'] = data_film_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("films/film_delete_wtf.html",
                           form_delete_film=form_delete_film,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_film_delete
                           )
