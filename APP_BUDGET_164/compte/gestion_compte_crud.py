"""
    Fichier : gestion_compte_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les comptes et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_BUDGET_164.database.database_tools import DBconnection
from APP_BUDGET_164.erreurs.exceptions import *
from APP_BUDGET_164.compte.gestion_compte_wtf_forms import FormWTFAjouterCompte, FormWTFDeleteCompte, \
    FormWTFUpdateCompte

"""
    Nom : compte_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /compte_afficher
    
    But : Afficher les comptes avec les genres associés pour chaque compte.
    
    Paramètres : id_genre_sel = 0 >> tous les comptes.
                 id_genre_sel = "n" affiche le compte dont l'id est "n"
                 
"""


@app.route("/compte_afficher/<int:id_compte_sel>", methods=['GET', 'POST'])
def compte_afficher(id_compte_sel):
    print(" compte_afficher id_compte_sel ", id_compte_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_comptes_afficher_data = """SELECT 
    u.nom_utilisateur,
    u.prenom_utilisateur,
    c.id_compte,
    c.nom_compte
FROM 
    t_utilisateur u
    INNER JOIN t_compte c ON u.id_utilisateur = c.id_utilisateur;
"""

                if id_compte_sel == 0:
                    # le paramètre 0 permet d'afficher tous les comptes
                    # Sinon le paramètre représente la valeur de l'id du compte
                    mc_afficher.execute(strsql_genres_comptes_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du compte sélectionné avec un nom de variable
                    valeur_id_compte_selected_dictionnaire = {"value_id_compte_selected": id_compte_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_comptes_afficher_data += """ HAVING id_depense= %(value_id_compte_selected)s"""

                    mc_afficher.execute(strsql_genres_comptes_afficher_data, valeur_id_compte_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_comptes_afficher = mc_afficher.fetchall()
                print("data_genres ", data_genres_comptes_afficher, " Type : ", type(data_genres_comptes_afficher))

                # Différencier les messages.
                if not data_genres_comptes_afficher and id_compte_sel == 0:
                    flash("""La table "t_depense" est vide. !""", "warning")
                elif not data_genres_comptes_afficher and id_compte_sel > 0:
                    # Si l'utilisateur change l'id_compte dans l'URL et qu'il ne correspond à aucun compte
                    flash(f"La depense {id_compte_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données comptee affichés !!", "success")

        except Exception as Exception_compte_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {compte_afficher.__name__} ;"
                                               f"{Exception_compte_afficher}")

    print("compte_afficher  ", data_genres_comptes_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("compte/compte_afficher.html", data=data_genres_comptes_afficher)


@app.route("/compte_ajouter", methods=['GET', 'POST'])
def compte_ajouter_wtf():
    form = (FormWTFAjouterCompte())
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                # Récupérer les données du formulaire
                nom_compte = form.nom_compte.data.lower()
                id_utilisateur = form.id_utilisateur.data.lower()

                # Préparer le dictionnaire des valeurs à insérer
                valeurs_insertion_dictionnaire = {
                    "nom_compte": nom_compte,
                    "id_utilisateur": id_utilisateur,

                }

                strsql_insert_genre = """INSERT INTO t_compte (id_utilisateur, nom_compte) VALUES (%(id_utilisateur)s,%(nom_compte)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")

                return redirect(url_for('compte_afficher', order_by='DESC', id_compte_sel=0))

        except Exception as Exception_compte_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(
                f"fichier : {Path(__file__).name} ; {compte_ajouter_wtf.__name__} ; {Exception_compte_ajouter_wtf}"
            )

    return render_template("compte/compte_ajouter_wtf.html", form=form)


"""
    nom: edit_genre_compte_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du compte sélectionné par le bouton "MODIFIER" de "compte_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au compte selectionné.
    3) Les genres non-attribués au compte sélectionné.

    On signale les erreurs importantes

"""
@app.route("/compte_update", methods=['GET', 'POST'])
def compte_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_depense"
    id_compte_update = request.values.get('id_film_btn_edit_html')

    # Objet formulaire pour l'UPDATE
    form_update_compte = FormWTFUpdateCompte()
    try:
        if request.method == "POST" and form_update_compte.submit.data:
            # Récupèrer la valeur du champ depuis "categories_update_wtf.html" après avoir cliqué sur "SUBMIT".
            id_compte_update = form_update_compte.nom_compte_update_wtf.data
            id_utilisateur = form_update_compte.id_utilisateur_update_wtf.data

            valeur_update_dictionnaire = {
                "nom_compte": id_compte_update,
                "id_utilisateur": id_utilisateur
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_film = """UPDATE t_compte SET id_utilisateur = %(id_utilisateur)s,
                                                            nom_compte = %(nom_compte)s
                                                            WHERE id_compte = %(id_utilisateur)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_film, valeur_update_dictionnaire)

            flash("Donnée mise à jour !!", "success")
            print("Donnée mise à jour !!")

            return redirect(url_for('compte_afficher', id_compte_sel=0))

        elif request.method == "GET" and id_compte_update:  # Only proceed if id_compte_update is available
            str_sql_id_film = "SELECT * FROM t_compte WHERE id_compte = %(value_id_compte)s"
            valeur_select_dictionnaire = {"value_id_compte": id_compte_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_film, valeur_select_dictionnaire)
                data_compte = mybd_conn.fetchone()
                print("data_compte ", data_compte, " type ", type(data_compte))
                if data_compte:
                    form_update_compte.nom_compte_update_wtf.data = data_compte["nom_compte"]
                    form_update_compte.id_utilisateur_update_wtf.data = data_compte["id_utilisateur"]
                else:
                    flash("Compte introuvable.", "error")
                    return redirect(url_for('compte_afficher', id_compte_sel=0))

    except Exception as Exception_compte_update_wtf:
        print(f"Erreur: {Exception_compte_update_wtf}")
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{compte_update_wtf.__name__} ; "
                                     f"{Exception_compte_update_wtf}")

    return render_template("compte/compte_update_wtf.html", form_update_compte=form_update_compte)

"""
    nom: genres_comptes_afficher_data

    Récupère la liste de tous les genres du compte sélectionné par le bouton "MODIFIER" de "compte_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


@app.route("/compte_delete", methods=['GET', 'POST'])
def compte_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_compte_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_depense"
    id_depense_delete = request.values['id_compte_btn_delete_html']

    # Objet formulaire pour effacer le compte sélectionné.
    form_delete_compte = FormWTFDeleteCompte()
    try:
        # Si on clique sur "ANNULER", afficher tous les comptes.
        if form_delete_compte.submit_btn_annuler.data:
            return redirect(url_for("comptes_genres_afficher", id_compte_sel=0))

        if form_delete_compte.submit_btn_conf_del.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "comptes/compte_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_compte_delete = session['data_compte_delete']
            print("data_compte_delete ", data_compte_delete)

            flash(f"Effacer le compte de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_compte.submit_btn_del.data:
            valeur_delete_dictionnaire = {"value_id_depense": id_depense_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_revenu = """DELETE FROM t_revenu WHERE id_compte = %(value_id_depense)s"""

            str_sql_delete_depense = """DELETE FROM t_depense WHERE id_compte = %(value_id_depense)s"""
            str_sql_delete_utilisateur_comptes = """DELETE FROM t_utilisateur_comptes WHERE id_compte = %(value_id_depense)s"""
            str_sql_delete_compte = """DELETE FROM t_compte WHERE id_compte = %(value_id_depense)s"""

            # Supprimer les dépendances avant de supprimer le compte
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_revenu, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_depense, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_utilisateur_comptes, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_compte, valeur_delete_dictionnaire)

            flash(f"compte définitivement effacé !!", "success")
            print(f"compte définitivement effacé !!")

            # afficher les données
            return redirect(url_for('compte_afficher', id_compte_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_depense": id_depense_delete}
            print(id_depense_delete, type(id_depense_delete))

            # Requête qui affiche le compte qui doit être effacé.
            str_sql_genres_comptes_delete = """SELECT * FROM t_compte WHERE id_compte = %(value_id_depense)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_comptes_delete, valeur_select_dictionnaire)
                data_compte_delete = mydb_conn.fetchall()
                print("data_compte_delete...", data_compte_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "comptes/compte_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_compte_delete'] = data_compte_delete

            # Le bouton pour l'action "DELETE" dans le form. "compte_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_compte_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{compte_delete_wtf.__name__} ; "
                                     f"{Exception_compte_delete_wtf}")

    return render_template("compte/compte_delete_wtf.html",
                           form_delete_compte=form_delete_compte,
                           btn_submit_del=btn_submit_del,
                           data_compte_del=data_compte_delete
                           )
