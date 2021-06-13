"""
    Fichier : gestion_account.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les personne.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *
#from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFAjouterPersonne
#from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFDeletePersonne
#from APP_FILMS.personne.gestion_personne_wtf_forms import FormWTFUpdatePersonne


"""
    Auteur : WP 2021.05.22
    Définition d'une "route" /newindex

    Test : ex : http://127.0.0.1:5005/newindex
"""


@obj_mon_application.route("/newindex")
def newindex():
    return render_template("newhome.html")


"""
    Auteur : WP 2021.05.22
    Définition d'une "route" /register
    
    Test : ex : http://127.0.0.1:5005/register
"""


@obj_mon_application.route("/register")
def register():
    return render_template("account/register.html")



@obj_mon_application.route("/registered", methods=['GET', 'POST'])
def registered():
    if request.method == "POST":
        nameVal = request.form.get("name")
        firstnameVal = request.form.get("firstname")
        user_value_dictionnary = {
            "name_value": request.form.get("name"),
            "firstname_value": request.form.get("firstname"),
            "pseudo_value": request.form.get("pseudo"),
            "birthdate_value": request.form.get("birthdate"),
            "mail_value": request.form.get("confirm_mail"),
            "password_value": request.form.get("confirm_password")
        }
        inserted_value_dictionnary = {}
        print("user_value_dictionnary", user_value_dictionnary)



    MaBaseDeDonnee().connexion_bd.ping(False)


    sqlquery_insert_personne = """INSERT INTO `t_personne`(`id_personne`, `pers_nom`, `pers_prenom`, `pers_dateDeNaissance`, `pers_ageValide`, `fk_pseudo`, `fk_mail`, `fk_motDePasse`) VALUES (NULL, %(name_value)s, %(firstname_value)s, %(birthdate_value)s, NULL, NULL, NULL, NULL);"""
    sqlquery_insert_pseudo = """INSERT INTO `t_pseudo`(`id_pseudo`, `pseudo`) VALUES(NULL, %(pseudo_value)s);"""
    sqlquery_insert_mail = """INSERT INTO `t_mail`(`id_mail`, `mail`) VALUES(NULL, %(mail_value)s);"""
    sqlquery_insert_motdepasse  = """INSERT INTO `t_motdepasse`(`id_motdepasse`, `motdepasse`) VALUES(NULL, %(password_value)s);"""

    sql_get_pseudo = """SELECT `id_pseudo` FROM `t_pseudo` WHERE `pseudo` = %(pseudo_value)s;"""
    sql_get_mail = """SELECT `id_mail` FROM `t_mail` WHERE `mail` = %(mail_value)s;"""
    sql_get_motdepasse = """SELECT `id_motDePasse` FROM `t_motdepasse` WHERE `motDePasse` = %(password_value)s;"""

    sql_update_fk_value =""""""

    with MaBaseDeDonnee() as mconn_bd:
        mconn_bd.mabd_execute(sqlquery_insert_personne, user_value_dictionnary)
        mconn_bd.mabd_execute(sqlquery_insert_pseudo, user_value_dictionnary)
        mconn_bd.mabd_execute(sqlquery_insert_mail, user_value_dictionnary)
        mconn_bd.mabd_execute(sqlquery_insert_motdepasse, user_value_dictionnary)

        mybd_cursor = MaBaseDeDonnee().connexion_bd.cursor()

        mybd_cursor.execute(sql_get_pseudo, user_value_dictionnary)
        id_pseudo = mybd_cursor.fetchall()
        mybd_cursor.execute(sql_get_mail, user_value_dictionnary)
        id_mail = mybd_cursor.fetchall()
        mybd_cursor.execute(sql_get_motdepasse, user_value_dictionnary)
        id_motdepasse = mybd_cursor.fetchall()

        print(id_pseudo)
        print(id_mail)
        print(id_motdepasse)

        print(inserted_value_dictionnary)

        print("Données insérées !!")

    return render_template("account/confirmation.html", firstname_user_value= firstnameVal, name_user_value=nameVal)


    return render_template("account/register.html")



"""
    Auteur : WP 2021.05.22
    Définition d'une "route" /register

    Test : ex : http://127.0.0.1:5005/register
"""


@obj_mon_application.route("/login")
def login():
    return render_template("account/login.html")