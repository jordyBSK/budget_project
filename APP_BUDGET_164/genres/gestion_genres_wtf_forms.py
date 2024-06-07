"""
    Fichier : gestion_compte_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import Length, InputRequired, Email, DataRequired
from wtforms.validators import Regexp

from flask_wtf import FlaskForm
from wtforms import EmailField



class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "categories_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"

    # Champ pour le nom de famille
    nom_utilisateur = StringField(
        "Nom de famille",
        validators=[
            DataRequired(message="Le nom est requis."),
            Length(min=2, max=50, message="Le nom doit contenir entre 2 et 50 caractères."),
            Regexp(nom_genre_regexp, message="Caractères invalides dans le nom.")
        ]
    )


    # Champ pour le prénom
    prenom_utilisateur = StringField(
        "Prénom",
        validators=[
            DataRequired(message="Le prénom est requis."),
            Length(min=2, max=50, message="Le prénom doit contenir entre 2 et 50 caractères."),
            Regexp(nom_genre_regexp, message="Caractères invalides dans le prénom.")
        ]
    )

    # Champ pour le mot de passe
    password_utilisateur = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(message="Le mot de passe est requis."),
            Length(min=1, max=100, message="Le mot de passe doit contenir au moins 8 caractères.")
        ]
    )

    email_utilisateur = EmailField(
        "Email de l'utilisateur",
        validators=[
            DataRequired(message="L'adresse e-mail est requise."),
            Email(message="L'adresse e-mail n'est pas valide."),
            Length(min=5, max=50, message="L'adresse e-mail doit contenir entre 5 et 50 caractères.")
        ]
    )
    submit = SubmitField("Enregistrer genre")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "categories_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_genre_update_wtf = StringField("Clavioter le genre ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    nom_user_update_wtf = StringField("nom utilisateur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    prenom_user_update_wtf = StringField("prenom utilisateur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                         Regexp(nom_genre_update_regexp,
                                                                                message="Pas de chiffres, de "
                                                                                        "caractères "
                                                                                        "spéciaux, "
                                                                                        "d'espace à double, de double "
                                                                                        "apostrophe, de double trait "
                                                                                        "union")
                                                                         ])
    email_user_update_wtf = StringField("email utilisateur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                            Regexp(nom_genre_update_regexp,
                                                                                   message="Pas de chiffres, de "
                                                                                           "caractères "
                                                                                           "spéciaux, "
                                                                                           "d'espace à double, de double "
                                                                                           "apostrophe, de double trait "
                                                                                           "union")
                                                                            ])
    password_user_update_wtf = StringField("password utilisateur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                           Regexp(nom_genre_update_regexp,
                                                                                  message="Pas de chiffres, de "
                                                                                          "caractères "
                                                                                          "spéciaux, "
                                                                                          "d'espace à double, de double "
                                                                                          "apostrophe, de double trait "
                                                                                          "union")
                                                                           ])
    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "categories_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Effacer cette utilisateur")
    submit_btn_del = SubmitField("Effacer utilisateur")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
