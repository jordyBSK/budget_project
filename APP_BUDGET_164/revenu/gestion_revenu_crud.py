"""
    Fichier : gestion_compte_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les revenus et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_BUDGET_164.database.database_tools import DBconnection
from APP_BUDGET_164.erreurs.exceptions import *
from APP_BUDGET_164.revenu.gestion_revenu_wtf_forms import FormWTFAjouterRevenu, FormWTFDeleteRevenu

"""
    Nom : revenu_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /revenu_afficher
    
    But : Afficher les revenus avec les genres associés pour chaque revenu.
    
    Paramètres : id_genre_sel = 0 >> tous les revenus.
                 id_genre_sel = "n" affiche le revenu dont l'id est "n"
                 
"""


@app.route("/revenu_afficher/<int:id_revenu_sel>", methods=['GET', 'POST'])
def revenu_afficher(id_revenu_sel):
    print(" revenu_afficher id_revenu_sel ", id_revenu_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_revenus_afficher_data = """
SELECT 
    d.id_revenu,
    u.nom_utilisateur,
    u.prenom_utilisateur,
    a.nom_compte,
    d.montant_revenu,
    d.date_revenu
FROM 
    t_revenu d
    INNER JOIN t_utilisateur u
    ON d.id_utilisateur = u.id_utilisateur
    INNER JOIN t_compte a
    ON d.id_compte = a.id_compte
"""

                if id_revenu_sel == 0:
                    # le paramètre 0 permet d'afficher tous les revenus
                    # Sinon le paramètre représente la valeur de l'id du revenu
                    mc_afficher.execute(strsql_genres_revenus_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du revenu sélectionné avec un nom de variable
                    valeur_id_revenu_selected_dictionnaire = {"value_id_revenu_selected": id_revenu_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_revenus_afficher_data += """ HAVING id_depense= %(value_id_revenu_selected)s"""

                    mc_afficher.execute(strsql_genres_revenus_afficher_data, valeur_id_revenu_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_revenus_afficher = mc_afficher.fetchall()
                print("data_genres ", data_genres_revenus_afficher, " Type : ", type(data_genres_revenus_afficher))

                # Différencier les messages.
                if not data_genres_revenus_afficher and id_revenu_sel == 0:
                    flash("""La table "t_depense" est vide. !""", "warning")
                elif not data_genres_revenus_afficher and id_revenu_sel > 0:
                    # Si l'utilisateur change l'id_revenu dans l'URL et qu'il ne correspond à aucun revenu
                    flash(f"La depense {id_revenu_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données revenue affichés !!", "success")

        except Exception as Exception_revenu_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {revenu_afficher.__name__} ;"
                                               f"{Exception_revenu_afficher}")

    print("revenu_afficher  ", data_genres_revenus_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("revenu/revenu_afficher.html", data=data_genres_revenus_afficher)



@app.route("/revenu_ajouter", methods=['GET', 'POST'])
def revenu_ajouter_wtf():
    form = (FormWTFAjouterRevenu())
    if request.method == "POST":
        try:
            if form.validate_on_submit():

                # Récupérer les données du formulaire
                montant_revenu = form.montant_revenu.data.lower()
                date_revenu = form.montant_revenu.data.lower()
                id_utilisateur = form.id_utilisateur.data.lower()
                id_compte = form.id_compte.data.lower()


            # Préparer le dictionnaire des valeurs à insérer
                valeurs_insertion_dictionnaire = {
                    "montant_revenu": montant_revenu,
                    "date_revenu": date_revenu,
                    "id_utilisateur": id_utilisateur,
                    "id_compte": id_compte
                }

                strsql_insert_genre = """INSERT INTO t_revenu (id_utilisateur, id_compte, montant_revenu, date_revenu)
VALUES (%(id_utilisateur)s,%(id_compte)s, %(montant_revenu)s,  %(montant_revenu)s,'2024-04-25');"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")

                return redirect(url_for('categorie_afficher', order_by='DESC', id_categorie_sel=0))

        except Exception as Exception_revenu_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(
                f"fichier : {Path(__file__).name} ; {revenu_ajouter_wtf.__name__} ; {Exception_revenu_ajouter_wtf}"
            )

    return render_template("revenu/revenu_ajouter_wtf.html", form=form)



"""
    nom: edit_genre_revenu_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du revenu sélectionné par le bouton "MODIFIER" de "compte_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au revenu selectionné.
    3) Les genres non-attribués au revenu sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_genre_revenu_selected", methods=['GET', 'POST'])
def edit_revenu_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_afficher = """SELECT id_genre, intitule_genre FROM t_genre ORDER BY id_genre ASC"""
                mc_afficher.execute(strsql_genres_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_genre_revenu_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_revenu" du formulaire html "compte_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_revenu"
            # grâce à la variable "id_revenu_genres_edit_html" dans le fichier "compte_afficher.html"
            # href="{{ url_for('edit_genre_revenu_selected', id_revenu_genres_edit_html=row.id_revenu) }}"
            id_revenu_genres_edit = request.values['id_revenu_genres_edit_html']

            # Mémorise l'id du revenu dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_revenu_genres_edit'] = id_revenu_genres_edit

            # Constitution d'un dictionnaire pour associer l'id du revenu sélectionné avec un nom de variable
            valeur_id_revenu_selected_dictionnaire = {"value_id_revenu_selected": id_revenu_genres_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_revenus_afficher_data
            # 1) Sélection du revenu choisi
            # 2) Sélection des genres "déjà" attribués pour le revenu.
            # 3) Sélection des genres "pas encore" attribués pour le revenu choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_revenus_afficher_data"
            data_genre_revenu_selected, data_genres_revenus_non_attribues, data_genres_revenus_attribues = \
                revenu_afficher(valeur_id_revenu_selected_dictionnaire)

            print(data_genre_revenu_selected)
            lst_data_revenu_selected = [item['id_revenu'] for item in data_genre_revenu_selected]
            print("lst_data_revenu_selected  ", lst_data_revenu_selected,
                  type(lst_data_revenu_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_genres_revenus_non_attribues = [item['id_genre'] for item in data_genres_revenus_non_attribues]
            session['session_lst_data_genres_revenus_non_attribues'] = lst_data_genres_revenus_non_attribues
            print("lst_data_genres_revenus_non_attribues  ", lst_data_genres_revenus_non_attribues,
                  type(lst_data_genres_revenus_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_genres_revenus_old_attribues = [item['id_genre'] for item in data_genres_revenus_attribues]
            session['session_lst_data_genres_revenus_old_attribues'] = lst_data_genres_revenus_old_attribues
            print("lst_data_genres_revenus_old_attribues  ", lst_data_genres_revenus_old_attribues,
                  type(lst_data_genres_revenus_old_attribues))

            print(" data data_genre_revenu_selected", data_genre_revenu_selected, "type ", type(data_genre_revenu_selected))
            print(" data data_genres_revenus_non_attribues ", data_genres_revenus_non_attribues, "type ",
                  type(data_genres_revenus_non_attribues))
            print(" data_genres_revenus_attribues ", data_genres_revenus_attribues, "type ",
                  type(data_genres_revenus_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_revenus_non_attribues = [item['intitule_genre'] for item in data_genres_revenus_non_attribues]
            print("lst_all_genres gf_edit_genre_revenu_selected ", lst_data_genres_revenus_non_attribues,
                  type(lst_data_genres_revenus_non_attribues))

        except Exception as Exception_edit_genre_revenu_selected:
            raise ExceptionEditGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_revenu_selected.__name__} ; "
                                                 f"{Exception_edit_genre_revenu_selected}")

    return render_template("revenu/revenu_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_revenu_selected=data_genre_revenu_selected,
                           data_genres_attribues=data_genres_revenus_attribues,
                           data_genres_non_attribues=data_genres_revenus_non_attribues)


"""
    nom: update_genre_revenu_selected

    Récupère la liste de tous les genres du revenu sélectionné par le bouton "MODIFIER" de "compte_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au revenu selectionné.
    3) Les genres non-attribués au revenu sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_genre_revenu_selected", methods=['GET', 'POST'])
def update_revenu_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du revenu sélectionné
            id_revenu_selected = session['session_id_revenu_genres_edit']
            print("session['session_id_revenu_genres_edit'] ", session['session_id_revenu_genres_edit'])

            # Récupère la liste des genres qui ne sont pas associés au revenu sélectionné.
            old_lst_data_genres_revenus_non_attribues = session['session_lst_data_genres_revenus_non_attribues']
            print("old_lst_data_genres_revenus_non_attribues ", old_lst_data_genres_revenus_non_attribues)

            # Récupère la liste des genres qui sont associés au revenu sélectionné.
            old_lst_data_genres_revenus_attribues = session['session_lst_data_genres_revenus_old_attribues']
            print("old_lst_data_genres_revenus_old_attribues ", old_lst_data_genres_revenus_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_revenus_modifier_tags_dropbox.html"
            new_lst_str_genres_revenus = request.form.getlist('name_select_tags')
            print("new_lst_str_genres_revenus ", new_lst_str_genres_revenus)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_genre_revenu_old = list(map(int, new_lst_str_genres_revenus))
            print("new_lst_genre_revenu ", new_lst_int_genre_revenu_old, "type new_lst_genre_revenu ",
                  type(new_lst_int_genre_revenu_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_revenu".
            lst_diff_genres_delete_b = list(set(old_lst_data_genres_revenus_attribues) -
                                            set(new_lst_int_genre_revenu_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_revenu"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_genre_revenu_old) - set(old_lst_data_genres_revenus_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_revenu"/"id_revenu" et "fk_genre"/"id_genre" dans la "t_genre_revenu"
            strsql_insert_genre_revenu = """INSERT INTO t_genre_revenu (id_genre_revenu, fk_genre, fk_revenu)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_revenu)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_revenu" et "id_genre" dans la "t_genre_revenu"
            strsql_delete_genre_revenu = """DELETE FROM t_genre_revenu WHERE fk_genre = %(value_fk_genre)s AND fk_revenu = %(value_fk_revenu)s"""

            with DBconnection() as mconn_bd:
                # Pour le revenu sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_revenu".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du revenu sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_revenu_sel_genre_sel_dictionnaire = {"value_fk_revenu": id_revenu_selected,
                                                               "value_fk_genre": id_genre_ins}

                    mconn_bd.execute(strsql_insert_genre_revenu, valeurs_revenu_sel_genre_sel_dictionnaire)

                # Pour le revenu sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_revenu".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du revenu sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_revenu_sel_genre_sel_dictionnaire = {"value_fk_revenu": id_revenu_selected,
                                                               "value_fk_genre": id_genre_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_genre_revenu, valeurs_revenu_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_revenu_selected:
            raise ExceptionUpdateGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_revenu_selected.__name__} ; "
                                                   f"{Exception_update_genre_revenu_selected}")

    # Après cette mise à jour de la table intermédiaire "t_genre_revenu",
    # on affiche les revenus et le(urs) genre(s) associé(s).
    return redirect(url_for('revenu_afficher', id_revenu_sel=id_film_btn_edit_html))


"""
    nom: genres_revenus_afficher_data

    Récupère la liste de tous les genres du revenu sélectionné par le bouton "MODIFIER" de "compte_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""

@app.route("/revenu_delete", methods=['GET', 'POST'])
def revenu_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_revenu_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_depense"
    id_depense_delete = request.values['id_revenu_btn_delete_html']

    # Objet formulaire pour effacer le revenu sélectionné.
    form_delete_revenu = FormWTFDeleteRevenu()
    try:
        # Si on clique sur "ANNULER", afficher tous les revenus.
        if form_delete_revenu.submit_btn_annuler.data:
            return redirect(url_for("revenus_genres_afficher", id_depense_sel=0))

        if form_delete_revenu.submit_btn_conf_del.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "revenus/compte_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_revenu_delete = session['data_revenu_delete']
            print("data_revenu_delete ", data_revenu_delete)

            flash(f"Effacer le revenu de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_revenu.submit_btn_del.data:
            valeur_delete_dictionnaire = {"value_id_depense": id_depense_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_utilisateur_depenses = """DELETE FROM t_utilisateur_revenus WHERE id_revenu = %(value_id_depense)s"""
            str_sql_delete_revenu = """DELETE FROM t_revenu WHERE id_revenu = %(value_id_depense)s"""

            # Supprimer les dépendances avant de supprimer la dépense
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_utilisateur_depenses, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_revenu, valeur_delete_dictionnaire)

            flash(f"Revenu définitivement effacée !!", "success")
            print(f"Revenu définitivement effacée !!")

            # afficher les données
            return redirect(url_for('revenu_afficher', id_revenu_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_depense": id_depense_delete}
            print(id_depense_delete, type(id_depense_delete))

            # Requête qui affiche le revenu qui doit être effacé.
            str_sql_genres_revenus_delete = """SELECT * FROM t_revenu WHERE id_revenu = %(value_id_depense)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_revenus_delete, valeur_select_dictionnaire)
                data_revenu_delete = mydb_conn.fetchall()
                print("data_revenu_delete...", data_revenu_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "revenus/compte_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_revenu_delete'] = data_revenu_delete

            # Le bouton pour l'action "DELETE" dans le form. "compte_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_revenu_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{revenu_delete_wtf.__name__} ; "
                                     f"{Exception_revenu_delete_wtf}")

    return render_template("revenu/revenu_delete_wtf.html",
                           form_delete_revenu=form_delete_revenu,
                           btn_submit_del=btn_submit_del,
                           data_revenu_del=data_revenu_delete
                           )
