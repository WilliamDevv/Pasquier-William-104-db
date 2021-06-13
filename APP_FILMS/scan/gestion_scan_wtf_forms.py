"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterScan(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    scan_titre_wtf = StringField("Clavioter le titre ", validators=[Length(min=2, max=60, message="min 2 max 60")])
    scan_auteur_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_auteur_wtf = StringField("Clavioter l'auteur ", validators=[Length(min=2, max=60, message="min 2 max 60"),
                                                                     Regexp(scan_auteur_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                     ])
    scan_dessinateur_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_dessinateur_wtf = StringField("Clavioter le dessinateur ", validators=[Length(min=2, max=60, message="min 2 max 60"),
                                                                     Regexp(scan_dessinateur_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                     ])
    scan_description_wtf = StringField("Clavioter la description ")
    scan_nombreDePages_regexp = "^([1-9][0-9]{0,2})$"
    scan_nombreDePages_wtf = StringField("Clavioter le nombre de pages ", validators=[Length(min=2, max=4, message="min 2 max 4"),
                                                                            Regexp(scan_nombreDePages_regexp,
                                                                                   message="Pas de lettre")
                                                                            ])
    scan_maisonDEdition_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_maisonDEdition_wtf = StringField("Clavioter la maison d'édition ", validators=[Length(min=2, max=30, message="min 2 max 30"),
                                                                     Regexp(scan_maisonDEdition_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                     ])
    submit = SubmitField("Enregistrer Scan")


class FormWTFUpdateScan(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    scan_titre_update_wtf = StringField("Clavioter le titre ", validators=[Length(min=2, max=60, message="min 2 max 60")])
    scan_auteur_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_auteur_update_wtf = StringField("Clavioter l'auteur ", validators=[Length(min=2, max=60, message="min 2 max 60"),
                                                                     Regexp(scan_auteur_update_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                     ])
    scan_dessinateur_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_dessinateur_update_wtf = StringField("Clavioter le dessinateur ",
                                       validators=[Length(min=2, max=60, message="min 2 max 60"),
                                                   Regexp(scan_dessinateur_update_regexp,
                                                          message="Pas de chiffres, de caractères "
                                                                  "spéciaux, "
                                                                  "d'espace à double, de double "
                                                                  "apostrophe, de double trait union")
                                                   ])
    scan_description_update_wtf = StringField("Clavioter la description ")
    scan_nombreDePages_update_regexp = "^([1-9][0-9]{0,2})$"
    scan_nombreDePages_update_wtf = StringField("Clavioter le nombre de pages ",
                                         validators=[Length(min=2, max=4, message="min 2 max 4"),
                                                     Regexp(scan_nombreDePages_update_regexp,
                                                            message="Pas de lettre")
                                                     ])
    scan_maisonDEdition_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    scan_maisonDEdition_update_wtf = StringField("Clavioter la maison d'édition ",
                                          validators=[Length(min=2, max=30, message="min 2 max 30"),
                                                      Regexp(scan_maisonDEdition_update_regexp,
                                                             message="Pas de chiffres, de caractères "
                                                                     "spéciaux, "
                                                                     "d'espace à double, de double "
                                                                     "apostrophe, de double trait union")
                                                      ])
    submit = SubmitField("Update scan")


class FormWTFDeleteScan(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    scan_titre_delete_wtf = StringField("Effacer le titre ")
    scan_auteur_delete_wtf = StringField("Effacer l'auteur ")
    scan_dessinateur_delete_wtf = StringField("Effacer le dessinateur ")
    scan_description_delete_wtf = StringField("Effacer la description ")
    scan_nombreDePages_delete_wtf = StringField("Effacer le nombre de pages ")
    scan_maisonDEdition_delete_wtf = StringField("Effacer la maison d'édition ")
    submit_btn_del = SubmitField("Effacer scan")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
