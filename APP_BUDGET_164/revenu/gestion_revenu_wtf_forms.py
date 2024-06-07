"""
    Fichier : gestion_revenu_wtf_forms.py
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

class FormWTFAjouterRevenu(FlaskForm):
    """
    Dans le formulaire "categories_ajouter_wtf.html" on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_revenuewe_regexp = r"^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"

    id_utilisateur = StringField(
        "id du destinataire",
        validators=[
            DataRequired(message="L'ID du compte est requis."),
            Length(min=1, max=50, message="L'ID du compte doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID du compte doit contenir uniquement des chiffres.")
        ]
    )

    id_compte = StringField(
        "Compte du destinataire",
        validators=[
            DataRequired(message="L'ID du compte est requis."),
            Length(min=1, max=50, message="L'ID du compte doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="L'ID du compte doit contenir uniquement des chiffres.")
        ]
    )

    montant_revenu = StringField(
        "Montant du revenu",
        validators=[
            DataRequired(message="Le montant est requis."),
            Length(min=1, max=50, message="Le montant doit contenir entre 1 et 50 caractères."),
            Regexp(r'^\d+$', message="Le montant doit contenir uniquement des chiffres.")
        ]
    )

    date_revenu = DateField(
        "Date de revenu",
        format='%Y-%m-%d',
        validators=[
            DataRequired(message="La date est requise."),
        ]
    )

    submit = SubmitField("Enregistrer catégorie")

class FormWTFUpdateRevenu(FlaskForm):
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
    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteRevenu(FlaskForm):
    """
        Dans le formulaire "categories_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_categorie_delete_wtf = StringField("Effacer cette categorie")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")