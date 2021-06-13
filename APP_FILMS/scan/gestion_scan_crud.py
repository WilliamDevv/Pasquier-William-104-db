"""
    Fichier : gestion_scans_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les scan.
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
from APP_FILMS.scan.gestion_scan_wtf_forms import FormWTFAjouterScan
from APP_FILMS.scan.gestion_scan_wtf_forms import FormWTFUpdateScan
from APP_FILMS.scan.gestion_scan_wtf_forms import FormWTFDeleteScan

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /scans_afficher
    
    Test : ex : http://127.0.0.1:5005/scan_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_scan_sel = 0 >> tous les scan.
                id_scan_sel = "n" affiche le scan dont l'id est "n"
"""


@obj_mon_application.route("/scan_afficher/<string:order_by>/<int:id_scan_sel>", methods=['GET', 'POST'])
def scan_afficher(order_by, id_scan_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion scan ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur Gestionscans {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_scan_sel == 0:
                    strsql_scan_afficher = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_scan ORDER BY id_scan ASC"""
                    mc_afficher.execute(strsql_scan_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_scan"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du scan sélectionné avec un nom de variable
                    valeur_id_scan_selected_dictionnaire = {"value_id_scan_selected": id_scan_sel}
                    strsql_scan_afficher = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_scan WHERE id_scan = %(value_id_scan_selected)s"""

                    mc_afficher.execute(strsql_scan_afficher, valeur_id_scan_selected_dictionnaire)
                else:
                    strsql_scan_afficher = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_scan ORDER BY id_scan ASC"""

                    mc_afficher.execute(strsql_scan_afficher)

                data_scan = mc_afficher.fetchall()

                print("data_scans ", data_scan, " Type : ", type(data_scan))

                # Différencier les messages si la table est vide.
                if not data_scan and id_scan_sel == 0:
                    flash("""La table "t_scan" est vide. !!""", "warning")
                elif not data_scan and id_scan_sel > 0:
                    # Si l'utilisateur change l'id_scan dans l'URL et que le scan n'existe pas,
                    flash(f"Le scan demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_scan" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données scan affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. scans_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} scans_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("scan/scan_afficher.html", data=data_scan)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /scan_ajouter
    
    Test : ex : http://127.0.0.1:5005/scans_ajouter
    
    Paramètres : sans
    
    But : Ajouter un scan pour un film
    
    Remarque :  Dans le champ "name_scan_html" du formulaire "scan/scans_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/scan_ajouter", methods=['GET', 'POST'])
def scan_ajouter_wtf():
    form = FormWTFAjouterScan()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion scan ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionScan {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                scan_titre_wtf = form.scan_titre_wtf.data
                scan_auteur_wtf = form.scan_auteur_wtf.data
                scan_dessinateur_wtf = form.scan_dessinateur_wtf.data
                scan_description_wtf = form.scan_description_wtf.data
                scan_nombreDePages_wtf = form.scan_nombreDePages_wtf.data
                scan_maisonDEdition_wtf = form.scan_maisonDEdition_wtf.data

                scan_titre = scan_titre_wtf.capitalize()
                scan_auteur = scan_auteur_wtf.capitalize()
                scan_dessinateur = scan_dessinateur_wtf.capitalize()
                scan_description = scan_description_wtf
                scan_nombreDePages = scan_nombreDePages_wtf
                scan_maisonDEdition = scan_maisonDEdition_wtf.capitalize()

                valeurs_insertion_dictionnaire = {"value_titre": scan_titre,
                                                  "value_auteur": scan_auteur,
                                                  "value_dessinateur": scan_dessinateur,
                                                  "value_description": scan_description,
                                                  "value_nombreDePages": scan_nombreDePages,
                                                  "value_maisonDEdition": scan_maisonDEdition}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_scan = """INSERT INTO t_scan (id_scan,scan_titre,scan_auteur,scan_dessinateur,scan_description,scan_nombreDePages,scan_maisonDEdition) VALUES (NULL,%(value_titre)s,%(value_auteur)s,%(value_dessinateur)s,%(value_description)s,%(value_nombreDePages)s,%(value_maisonDEdition)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_scan, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('scan_afficher', order_by='DESC', id_scan_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_scan_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_scan_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_scan_crud:
            code, msg = erreur_gest_scan_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion scan CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_scan_crud.args[0]} , "
                  f"{erreur_gest_scan_crud}", "danger")

    return render_template("scan/scan_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /scan_update
    
    Test : ex cliquer sur le menu "scan" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "scan/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/scan_update", methods=['GET', 'POST'])
def scan_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_scan_update = request.values['id_scan_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateScan()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            scan_titre_update_wtf = form_update.scan_titre_update_wtf.data
            scan_auteur_update_wtf = form_update.scan_auteur_update_wtf.data
            scan_dessinateur_update_wtf = form_update.scan_dessinateur_update_wtf.data
            scan_description_update_wtf = form_update.scan_description_update_wtf.data
            scan_nombreDePages_update_wtf = form_update.scan_nombreDePages_update_wtf.data
            scan_maisonDEdition_update_wtf = form_update.scan_maisonDEdition_update_wtf.data

            scan_titre = scan_titre_update_wtf
            scan_auteur = scan_auteur_update_wtf
            scan_dessinateur = scan_dessinateur_update_wtf
            scan_description = scan_description_update_wtf
            scan_nombreDePages = scan_nombreDePages_update_wtf
            scan_maisonDEdition = scan_maisonDEdition_update_wtf.capitalize()

            valeur_update_dictionnaire = {"value_id_scan": id_scan_update,
                                              "value_titre": scan_titre,
                                              "value_auteur": scan_auteur,
                                              "value_dessinateur": scan_dessinateur,
                                              "value_description": scan_description,
                                              "value_nombreDePages": scan_nombreDePages,
                                              "value_maisonDEdition": scan_maisonDEdition}
            print("valeurs_insertion_dictionnaire ", valeur_update_dictionnaire)


            str_sql_update_scan = """UPDATE t_scan SET scan_titre = %(value_titre)s, scan_auteur = %(value_auteur)s, scan_dessinateur = %(value_dessinateur)s, scan_description = %(value_description)s, scan_nombreDePages = %(value_nombreDePages)s, scan_maisonDEdition = %(value_maisonDEdition)s WHERE id_scan = %(value_id_scan)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_scan, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('scan_afficher', order_by="ASC", id_scan_sel=id_scan_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_scan = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_scan WHERE id_scan = %(value_id_scan)s"""
            valeur_select_dictionnaire = {"value_id_scan": id_scan_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_scan, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_scan = mybd_curseur.fetchone()
            print("data_scan ", data_scan, " type ", type(data_scan), " scan ",
                  data_scan["scan_titre"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.scan_titre_update_wtf.data = data_scan["scan_titre"]
            form_update.scan_auteur_update_wtf.data = data_scan["scan_auteur"]
            form_update.scan_dessinateur_update_wtf.data = data_scan["scan_dessinateur"]
            form_update.scan_description_update_wtf.data = data_scan["scan_description"]
            form_update.scan_nombreDePages_update_wtf.data = data_scan["scan_nombreDePages"]
            form_update.scan_maisonDEdition_update_wtf.data  = data_scan["scan_maisonDEdition"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans scan_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans scan_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_scan_crud:
        code, msg = erreur_gest_scan_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_scan_crud} ", "danger")
        flash(f"Erreur dans scan_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_scan_crud.args[0]} , "
              f"{erreur_gest_scan_crud}", "danger")
        flash(f"__KeyError dans scan_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("scan/scan_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "scan" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_pseudo_delete_wtf" du formulaire "scan/pseudo_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/scan_delete", methods=['GET', 'POST'])
def scan_delete_wtf():
    data_scan_avoir_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_scan_delete = request.values['id_scan_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteScan()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("scan_afficher", order_by="ASC", id_scan_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "scan/scan_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_scan_avoir_personne_delete = session['data_scan_avoir_genre_delete']
                print("data_scan_avoir_genre_delete ", data_scan_avoir_genre_delete)

                flash(f"Effacer le scan de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_scan": id_scan_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_avoir_genre = """DELETE FROM t_avoir_genre WHERE fk_scan = %(value_id_scan)s"""
                str_sql_delete_id_scan = """DELETE FROM t_scan WHERE id_scan = %(value_id_scan)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_avoir_genre, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_id_scan, valeur_delete_dictionnaire)

                flash(f"scan définitivement effacé !!", "success")
                print(f"scan définitivement effacé !!")

                # afficher les données
                return redirect(url_for('scan_afficher', order_by="ASC", id_scan_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_scan": id_scan_delete}
            print(id_scan_delete, type(id_scan_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            str_sql_avoir_genre_delete = """SELECT id_avoir_genre, genre, id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_avoir_genre
                                            INNER JOIN t_genre ON t_avoir_genre.fk_genre = t_genre.id_genre
                                            INNER JOIN t_scan ON t_avoir_genre.fk_scan = t_scan.id_scan
                                            WHERE fk_scan = %(value_id_scan)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_avoir_genre_delete, valeur_select_dictionnaire)
            data_scan_avoir_genre_delete = mybd_curseur.fetchall()
            print("data_scan_avoir_genre_delete...", data_scan_avoir_genre_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "scan/pseudo_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_scan_avoir_genre_delete'] = data_scan_avoir_genre_delete

            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_scan = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition FROM t_scan WHERE id_scan = %(value_id_scan)s"""

            mybd_curseur.execute(str_sql_id_scan, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            data_scan = mybd_curseur.fetchone()
            print("data_scan ", data_scan, " type ", type(data_scan), " scan ",
                  data_scan["scan_titre"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "pseudo_delete_wtf.html"
            form_delete.scan_titre_delete_wtf = data_scan["scan_titre"]
            form_delete.scan_auteur_delete_wtf = data_scan["scan_auteur"]
            form_delete.scan_dessinateur_delete_wtf = data_scan["scan_dessinateur"]
            form_delete.scan_description_delete_wtf = data_scan["scan_description"]
            form_delete.scan_nombreDePages_delete_wtf = data_scan["scan_nombreDePages"]
            form_delete.scan_maisonDEdition_delete_wtf = data_scan["scan_maisonDEdition"]

            # Le bouton pour l'action "DELETE" dans le form. "scan_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans scan_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans scan_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans scan_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans scan_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("scan/scan_delete_wtf.html",
                               form_delete=form_delete,
                               btn_submit_del=btn_submit_del,
                               data_genre_associes=data_scan_avoir_genre_delete)
