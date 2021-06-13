"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
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

"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@obj_mon_application.route("/avoir_genre_afficher/<int:id_scan_sel>", methods=['GET', 'POST'])
def avoir_genre_afficher(id_scan_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as Exception_init_films_genres_afficher:
                code, msg = Exception_init_films_genres_afficher.args
                flash(f"{error_codes.get(code, msg)} ", "danger")
                flash(f"Exception _init_films_genres_afficher problème de connexion BD : {sys.exc_info()[0]} "
                      f"{Exception_init_films_genres_afficher.args[0]} , "
                      f"{Exception_init_films_genres_afficher}", "danger")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_avoir_genre_afficher_data = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition,
                                                            GROUP_CONCAT(genre) as GenresScans FROM t_avoir_genre
                                                            RIGHT JOIN t_scan ON t_scan.id_scan = t_avoir_genre.fk_scan
                                                            LEFT JOIN t_genre ON t_genre.id_genre = t_avoir_genre.fk_genre
                                                            GROUP BY id_scan"""
                if id_scan_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_avoir_genre_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_scan_selected_dictionnaire = {"value_id_scan_selected": id_scan_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_avoir_genre_afficher_data += """ HAVING id_scan= %(value_id_scan_selected)s"""

                    mc_afficher.execute(strsql_avoir_genre_afficher_data, valeur_id_scan_selected_dictionnaire)

                # Récupère les données de la requête.
                data_avoir_genre_afficher = mc_afficher.fetchall()
                print("data_genres ", data_avoir_genre_afficher, " Type : ", type(data_avoir_genre_afficher))

                # Différencier les messages.
                if not data_avoir_genre_afficher and id_scan_sel == 0:
                    flash("""La table "t_film" est vide. !""", "warning")
                elif not data_avoir_genre_afficher and id_scan_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le film {id_scan_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données films et genres affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            code, msg = Exception_films_genres_afficher.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception films_genres_afficher : {sys.exc_info()[0]} "
                  f"{Exception_films_genres_afficher.args[0]} , "
                  f"{Exception_films_genres_afficher}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template("avoir_genre/avoir_genre_afficher.html", data=data_avoir_genre_afficher)


"""
    nom: edit_avoir_genre_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@obj_mon_application.route("/edit_avoir_genre_selected", methods=['GET', 'POST'])
def edit_avoir_genre_selected():
    if request.method == "GET":
        try:
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_genres_afficher = """SELECT id_genre, genre FROM t_genre ORDER BY id_genre ASC"""
                mc_afficher.execute(strsql_genres_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_avoir_genre_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_film" du formulaire html "films_genres_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "films_genres_afficher.html"
            # href="{{ url_for('edit_avoir_genre_selected', id_film_genres_edit_html=row.id_film) }}"
            id_avoir_genre_edit = request.values['id_avoir_genre_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_avoir_genre_edit'] = id_avoir_genre_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_scan_selected_dictionnaire = {"value_id_scan_selected": id_avoir_genre_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_scans_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_scans_afficher_data"
            data_avoir_genre_selected, data_avoir_genre_non_attribues, data_avoir_genre_attribues = \
                avoir_genre_afficher(valeur_id_scan_selected_dictionnaire)

            print(data_avoir_genre_non_attribues)
            lst_data_scan_selected = [item['id_scan'] for item in data_avoir_genre_selected]
            print("lst_data_scan_selected  ", lst_data_scan_selected,
                  type(lst_data_scan_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_avoir_genre_non_attribues = [item['id_genre'] for item in data_avoir_genre_non_attribues]
            session['session_lst_data_avoir_genre_non_attribues'] = lst_data_avoir_genre_non_attribues
            print("lst_data_avoir_genre_non_attribues  ", lst_data_avoir_genre_non_attribues,
                  type(lst_data_avoir_genre_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_avoir_genre_old_attribues = [item['id_genre'] for item in data_avoir_genre_attribues]
            session['session_lst_data_avoir_genre_old_attribues'] = lst_data_avoir_genre_old_attribues
            print("lst_data_avoir_genre_old_attribues  ", lst_data_avoir_genre_old_attribues,
                  type(lst_data_avoir_genre_old_attribues))

            print(" data data_avoir_genre_selected", data_avoir_genre_selected, "type ", type(data_avoir_genre_selected))
            print(" data data_avoir_genre_non_attribues ", data_avoir_genre_non_attribues, "type ",
                  type(data_avoir_genre_non_attribues))
            print(" data_avoir_genre_attribues ", data_avoir_genre_attribues, "type ",
                  type(data_avoir_genre_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_films_non_attribues = [item['intitule_genre'] for item in data_avoir_genre_non_attribues]
            print("lst_all_genres gf_edit_avoir_genre_selected ", lst_data_avoir_genre_non_attribues,
                  type(lst_data_avoir_genre_non_attribues))

        except Exception as Exception_edit_avoir_genre_selected:
            code, msg = Exception_edit_avoir_genre_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception edit_avoir_genre_selected : {sys.exc_info()[0]} "
                  f"{Exception_edit_avoir_genre_selected.args[0]} , "
                  f"{Exception_edit_avoir_genre_selected}", "danger")

    return render_template("avoir_genre/avoir_genre_modifier_tags_dropbox.html.html",
                           data_genres=data_genres_all,
                           data_scan_selected=data_avoir_genre_selected,
                           data_genres_attribues=data_avoir_genre_attribues,
                           data_genres_non_attribues=data_avoir_genre_non_attribues)


"""
    nom: update_avoir_genre_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@obj_mon_application.route("/update_avoir_genre_selected", methods=['GET', 'POST'])
def update_avoir_genre_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_scan_selected = session['session_id_avoir_genre_edit']
            print("session['session_id_avoir_genre_edit'] ", session['session_id_avoir_genre_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_avoir_genre_non_attribues = session['session_lst_data_avoir_genre_non_attribues']
            print("old_lst_data_avoir_genre_non_attribues ", old_lst_data_avoir_genre_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_avoir_genre_attribues = session['session_lst_data_avoir_genre_old_attribues']
            print("old_lst_data_avoir_genre_old_attribues ", old_lst_data_avoir_genre_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "avoir_genre_modifier_tags_dropbox.html"
            new_lst_str_avoir_genre = request.form.getlist('name_select_tags')
            print("new_lst_str_avoir_genre ", new_lst_str_avoir_genre)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_avoir_genre_old = list(map(int, new_lst_str_avoir_genre))
            print("new_lst_avoir_genre ", new_lst_int_avoir_genre_old, "type new_lst_avoir_genre ",
                  type(new_lst_int_avoir_genre_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_avoir_genre".
            lst_diff_genres_delete_b = list(
                set(old_lst_data_avoir_genre_attribues) - set(new_lst_int_avoir_genre_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_avoir_genre"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_avoir_genre_old) - set(old_lst_data_avoir_genre_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_genre" dans la "t_avoir_genre"
            strsql_insert_avoir_genre = """INSERT INTO t_avoir_genre (id_avoir_genre, fk_genre, fk_scan)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_scan)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_genre" dans la "t_avoir_genre"
            strsql_delete_avoir_genre = """DELETE FROM t_avoir_genre WHERE fk_genre = %(value_fk_genre)s AND fk_scan = %(value_fk_scan)s"""

            with MaBaseDeDonnee() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_avoir_genre".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_scan": id_scan_selected,
                                                               "value_fk_genre": id_genre_ins}

                    mconn_bd.mabd_execute(strsql_insert_avoir_genre, valeurs_film_sel_genre_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_scan": id_scan_selected,
                                                               "value_fk_genre": id_genre_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.mabd_execute(strsql_delete_avoir_genre, valeurs_film_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_film_selected:
            code, msg = Exception_update_genre_film_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception update_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_update_genre_film_selected.args[0]} , "
                  f"{Exception_update_genre_film_selected}", "danger")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('films_genres_afficher', id_scan_sel=id_scan_selected))


"""
    nom: genres_scans_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def avoir_genre_afficher(valeur_id_scan_selected_dictionnaire):
    print("valeur_id_scan_selected_dictionnaire...", valeur_id_scan_selected_dictionnaire)
    try:

        strsql_scans_selected = """SELECT id_scan, scan_titre, scan_auteur, scan_dessinateur, scan_description, scan_nombreDePages, scan_maisonDEdition, GROUP_CONCAT(id_genre) as GenresScans FROM t_avoir_genre
                                        INNER JOIN t_scan ON t_scan.id_scan = t_avoir_genre.fk_scan
                                        INNER JOIN t_genre ON t_genre.id_genre = t_avoir_genre.fk_genre
                                        WHERE id_film = %(valeur_id_scan_selected_dictionnaire)s"""

        strsql_avoir_genre_non_attribues = """SELECT id_genre, genre FROM t_genre WHERE id_genre not in(SELECT id_genre as idGenresScans FROM t_avoir_genre
                                                    INNER JOIN t_scan ON t_scan.id_scan = t_avoir_genre.fk_scan
                                                    INNER JOIN t_genre ON t_genre.id_genre = t_avoir_genre.fk_genre
                                                    WHERE id_film = %(valeur_id_scan_selected_dictionnaire)s)"""

        strsql_avoir_genre_attribues = """SELECT id_scan, id_genre, genre FROM t_avoir_genre
                                            INNER JOIN t_scan ON t_scan.id_scan = t_avoir_genre.fk_scan
                                            INNER JOIN t_genre ON t_genre.id_genre = t_avoir_genre.fk_genre
                                            WHERE id_film = %(valeur_id_scan_selected_dictionnaire)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_avoir_genre_non_attribues, valeur_id_scan_selected_dictionnaire)
            # Récupère les données de la requête.
            data_avoir_genre_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_scans_afficher_data ----> data_genres_films_non_attribues ",  data_avoir_genre_non_attribues,
                  " Type : ",
                  type( data_avoir_genre_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_scans_selected, valeur_id_scan_selected_dictionnaire)
            # Récupère les données de la requête.
            data_genre_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genre_selected  ", data_genre_selected, " Type : ", type(data_genre_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_avoir_genre_attribues, valeur_id_scan_selected_dictionnaire)
            # Récupère les données de la requête.
            data_avoir_genre_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_films_attribues ", data_avoir_genre_attribues, " Type : ",
                  type(data_avoir_genre_non_attribues))

            # Retourne les données des "SELECT"
            return data_genre_selected, data_avoir_genre_non_attribues, data_avoir_genre_attribues
    except pymysql.Error as pymysql_erreur:
        code, msg = pymysql_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.Error Erreur dans avoir_genre_afficher_data : {sys.exc_info()[0]} "
              f"{pymysql_erreur.args[0]} , "
              f"{pymysql_erreur}", "danger")
    except Exception as exception_erreur:
        code, msg = exception_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"Exception Erreur dans avoir_genre_afficher_data : {sys.exc_info()[0]} "
              f"{exception_erreur.args[0]} , "
              f"{exception_erreur}", "danger")
    except pymysql.err.IntegrityError as IntegrityError_genres_scans_afficher_data:
        code, msg = IntegrityError_genres_scans_afficher_data.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.err.IntegrityError Erreur dans avoir_genre_afficher_data : {sys.exc_info()[0]} "
              f"{IntegrityError_genres_scans_afficher_data.args[0]} , "
              f"{IntegrityError_genres_scans_afficher_data}", "danger")
