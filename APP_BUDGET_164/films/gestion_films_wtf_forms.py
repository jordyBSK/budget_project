"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddFilm(FlaskForm):
    """
    Dans le formulaire "depenses_add_wtf.html", on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    id_utilisateur = StringField(
        "ID de l'utilisateur",
        validators=[
            DataRequired(message="L'ID de l'utilisateur est requis."),
            Length(min=1, max=50, message="L'ID de l'utilisateur doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID de l'utilisateur doit contenir uniquement des chiffres.")
        ]
    )

    id_compte = StringField(
        "ID du compte",
        validators=[
            DataRequired(message="L'ID du compte est requis."),
            Length(min=1, max=50, message="L'ID du compte doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID du compte doit contenir uniquement des chiffres.")
        ]
    )

    id_categorie = StringField(
        "ID de la catégorie",
        validators=[
            DataRequired(message="L'ID de la catégorie est requis."),
            Length(min=1, max=50, message="L'ID de la catégorie doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID de la catégorie doit contenir uniquement des chiffres.")
        ]
    )

    montant_depense = StringField(
        "Montant de la dépense",
        validators=[
            DataRequired(message="Le montant de la dépense est requis.")
        ]
    )

    date_depense = DateField(
        "Date de la dépense",
        format='%Y-%m-%d',
        validators=[
            DataRequired(message="La date de la dépense est requise.")
        ]
    )

    description_depense = StringField(
        "Description de la dépense",
        validators=[
            DataRequired(message="La description est requise."),
            Length(min=1, max=255, message="La description doit contenir entre 1 et 255 caractères.")
        ]
    )

    lieu_depense = StringField(
        "Lieu de la dépense",
        validators=[
            DataRequired(message="Le lieu est requis."),
            Length(min=1, max=255, message="Le lieu doit contenir entre 1 et 255 caractères.")
        ]
    )

    submit = SubmitField("Enregistrer la dépense")


class FormWTFUpdateFilm(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    categorie_depense_update_wtf = IntegerField("id categorie", )
    id_compte_update_wtf = IntegerField("id compte", )
    montant_depense_update_wtf = StringField("Montant ")
    cover_link_film_update_wtf = StringField("lieu dépense", )
    description_depense_update_wtf = StringField("description dépense", )
    date_depense_update_wtf = DateField("date de dépense", validators=[InputRequired("Date obligatoire"),
                                                                       DataRequired("Date non valide")])

    submit = SubmitField("Update depense")


class FormWTFDeleteFilm(FlaskForm):
    """
        Dans le formulaire "film_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    nom_film_delete_wtf = StringField("Effacer ce dépense")
    submit_btn_del_film = SubmitField("Effacer dépense")
    submit_btn_conf_del_film = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
