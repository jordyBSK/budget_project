"""
    Fichier : gestion_compte_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.validators import Length, InputRequired, Email, DataRequired
from wtforms.validators import Regexp

from flask_wtf import FlaskForm
from wtforms import EmailField

class FormWTFAjouterCompte(FlaskForm):
    """
    Dans le formulaire "categories_ajouter_wtf.html" on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    id_utilisateur = StringField(
        "id de l'utilisateur",
        validators=[
            DataRequired(message="L'ID du compte est requis."),
            Length(min=1, max=50, message="L'ID du compte doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID du compte doit contenir uniquement des chiffres.")
        ]
    )

    nom_compte = StringField(
        "nom du compte",
        validators=[
            DataRequired(message="L'ID du compte est requis."),
            Length(min=1, max=50, message="L'ID du compte doit contenir entre 1 et 50 caractères."),
            Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$", message="L'ID du compte doit contenir uniquement des chiffres.")
        ]
    )



    submit = SubmitField("Enregistrer compte")

class FormWTFUpdateCompte(FlaskForm):
    """
        Dans le formulaire "categories_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    id_utilisateur_update_wtf = IntegerField("id utilisateur ", validators=[Length(min=1, max=1000000, message="min 1 max 20")])

    nom_compte_update_wtf = StringField("nom du compte", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update compte")


class FormWTFDeleteCompte(FlaskForm):
    """
        Dans le formulaire "categories_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_categorie_delete_wtf = StringField("Effacer ce compte")
    submit_btn_del = SubmitField("Effacer compte")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
