import datetime
from datetime import timedelta
import sqlite3
from typing import NamedTuple

from get_dop_inf import host, user, password, db_name, port, Rating

import psycopg2


def GP():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust, GP FROM exit_")
        for kustGPex in cursor.fetchall():
            kust_ex = kustGPex[0]
            GP_ex = kustGPex[1]
            cursor.execute("SELECT kust, GP FROM enterance")
            for kustGPent in cursor.fetchall():
                kust_ent = kustGPent[0]
                GP_ent = kustGPent[1]
                rating = 0
                comment = ' '
                if GP_ex == GP_ent:  # грузоподъемность подходит идеально (10 баллов)
                    rating += 10

                elif (GP_ex == 400 and GP_ent == 320 or  # Запас по буримости низкий (8 баллов)
                      GP_ex == 320 and GP_ent == 270 or
                      GP_ex == 270 and GP_ent == 250 or
                      GP_ex == 250 and GP_ent == 225 or
                      GP_ex == 225 and GP_ent == 200):
                    rating += 8
                    comment = 'Потеря по буримости минимальная'
                elif (GP_ex == 400 and GP_ent == 270 or  # Запас по буримости приличный (3 балла)
                      GP_ex == 320 and GP_ent == 250 or
                      GP_ex == 270 and GP_ent == 225 or
                      GP_ex == 250 and GP_ent == 225):
                    rating += 3
                    comment = 'Потеря по буримости средняя'
                elif (GP_ex == 400 and GP_ent == 250 or  # Запас по буримости огромный (1 балл)
                      GP_ex == 320 and GP_ent == 225 or
                      GP_ex == 270 and GP_ent == 200 or
                      GP_ex == 250 and GP_ent == 200):
                    rating += 1
                    comment = 'Потеря по буримости критичная'
                # Запас по буримости отрицательный. Требуется оптимизация профилей (1.0001 балл)
                elif (
                        GP_ex == 320 and GP_ent == 400 or
                        GP_ex == 270 and GP_ent == 320 or
                        GP_ex == 250 and GP_ent == 270 or
                        GP_ex == 225 and GP_ent == 250 or
                        GP_ex == 200 and GP_ent == 225):
                    rating += 0.5
                    comment = 'Требуется оптимизация буримости'
                else:  # Бурение нецелесообразно. (вариант исключается)
                    continue
                values = (kust_ex, kust_ent, rating, comment)
                cursor.execute("INSERT INTO raschet(kust_ex, kust_ent, GP_rating, Comment) VALUES(%s, %s, %s, %s)",
                               values)
    connection.close()


def Ist():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust_ex, kust_ent FROM raschet")
        PARES = cursor.fetchall()
        for PARE in PARES:
            kust_ex = PARE[0]
            kust_ent = PARE[1]
            cursor.execute("SELECT exit_date FROM exit_ WHERE kust = %s", (kust_ex,))
            exit_date = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d")
            cursor.execute("SELECT first_stage FROM enterance WHERE kust = %s", (kust_ent,))
            Ist_stage = str(cursor.fetchone()[0])
            rating = 0
            comment = ' '
            if Ist_stage == 'готов':  # Идеальный вариант. Первый этап готов (10 баллов)
                rating += 10
            else:
                Ist_stage = datetime.datetime.strptime(Ist_stage, "%Y-%m-%d")
                if exit_date >= Ist_stage:  # Первый этап будет готов к выходу БУ (10 баллов)
                    rating += 10
                    comment = ' '
                elif exit_date + timedelta(
                        7) >= Ist_stage:  # Первый этап будет готов через 7 дней после выхода БУ (9 баллов)
                    rating += 9
                    comment = ' '
                elif exit_date + timedelta(
                        12) >= Ist_stage:  # Первый этап будет готов через 12 дней после выхода БУ (8 баллов)
                    rating += 8
                    comment = ' '
                elif exit_date + timedelta(
                        18) >= Ist_stage:  # Первый этап будет готов через 18 дней после выхода БУ (3 баллов)
                    rating += 3
                    comment = ' '
                elif exit_date + timedelta(
                        20) >= Ist_stage:
                    # Первый этап будет готов через 20 дней после выхода БУ (1 балл, требуется ускорение)
                    rating += 1
                    comment = ', требуется ускорение I этапа'
            if rating > 0:
                values1 = (rating, kust_ex, kust_ent)
                values2 = (comment, kust_ex, kust_ent)
                cursor.execute("UPDATE raschet SET first_stage_rating=%s WHERE kust_ex=%s AND kust_ent=%s", values1)
                cursor.execute("UPDATE raschet SET Comment=(Comment || ',' || %s) WHERE kust_ex=%s AND kust_ent=%s",
                               values2)
            else:
                values = (kust_ex, kust_ent)
                cursor.execute("DELETE FROM raschet WHERE kust_ex=%s AND kust_ent=%s", values)
    connection.close()


def IInd():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust_ex, kust_ent FROM raschet")
        PARES = cursor.fetchall()
        for PARE in PARES:
            kust_ex = PARE[0]
            kust_ent = PARE[1]
            cursor.execute("SELECT exit_date FROM exit_ WHERE kust = %s", (kust_ex,))
            exit_date = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d")
            cursor.execute("SELECT second_stage FROM enterance WHERE kust = %s", (kust_ent,))
            IInd_stage = str(cursor.fetchone()[0])
            rating = 0
            if IInd_stage == 'готов':  # Идеальный вариант. Второй этап готов (10 баллов)
                rating += 10
                comment = ' '
            else:
                IInd_stage = datetime.datetime.strptime(IInd_stage, '%Y-%m-%d')
                if exit_date >= IInd_stage:  # Второй этап будет готов к выходу БУ (10 баллов)
                    rating += 10
                    comment = ' '
                elif exit_date + timedelta(
                        10) >= IInd_stage:  # Второй этап будет готов через 10 дней после выхода БУ (9 баллов)
                    rating += 9
                    comment = ' '
                elif exit_date + timedelta(
                        14) >= IInd_stage:  # Второй этап будет готов через 14 дней после выхода БУ (8 баллов)
                    rating += 8
                    comment = ' '
                elif exit_date + timedelta(
                        21) >= IInd_stage:  # Второй этап будет готов через 21 дней после выхода БУ (6 баллов)
                    rating += 6
                    comment = ' '
                elif exit_date + timedelta(
                        28) >= IInd_stage:  # Второй этап будет готов через 28 дней после выхода БУ (4 баллов)
                    rating += 4
                    comment = ' '
                elif exit_date + timedelta(
                        35) >= IInd_stage:  # Второй этап будет готов через 35 дней после выхода БУ (2 балла)
                    rating += 2
                    comment = ' '
                elif exit_date + timedelta(
                        42) >= IInd_stage:
                    # Второй этап будет готов через 42 дня после выхода БУ (1 балл, требуется ускорение)
                    rating += 1
                    comment = 'требуется ускорение II этапа'
            if rating > 0:
                values1 = (rating, kust_ex, kust_ent)
                values2 = (comment, kust_ex, kust_ent)
                cursor.execute("UPDATE raschet SET second_stage_rating=%s WHERE kust_ex=%s AND kust_ent=%s", values1)
                cursor.execute("UPDATE raschet SET Comment=(Comment || ',' || %s) WHERE kust_ex=%s AND kust_ent=%s",
                               values2)
            else:
                values = (kust_ex, kust_ent)
                cursor.execute("DELETE FROM raschet WHERE kust_ex=%s AND kust_ent=%s", values)
    connection.close()


def RUO():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust_ex, kust_ent FROM raschet")
        PARES = cursor.fetchall()
        for PARE in PARES:
            kust_ex = PARE[0]
            kust_ent = PARE[1]
            cursor.execute("SELECT RUO FROM exit_ WHERE kust = %s", (kust_ex,))
            exit_RUO = cursor.fetchone()[0]
            cursor.execute("SELECT RUO FROM enterance WHERE kust = %s", (kust_ent,))
            enter_RUO = cursor.fetchone()[0]
            rating = 0
            comment = ' '
            if exit_RUO == enter_RUO:  # Куст соответствует возможности БУ бурить РУО (10 баллов)
                rating += 10
                comment = ' '
            if exit_RUO == 1 and enter_RUO == 0:  # БУ РУО едет на куст не РУО (6 баллов)
                rating += 6
                comment = ' '
            if exit_RUO == 0 and enter_RUO == 1:
                # БУ не РУО едет на куст РУО (3 балла, требуется подтверждение буримости)
                rating += 3
                comment = 'требуется подтверждение возможности  бурение на РВО'
            values1 = (rating, kust_ex, kust_ent)
            values2 = (comment, kust_ex, kust_ent)
            cursor.execute("UPDATE raschet SET RUO_rating = %s WHERE kust_ex=%s AND kust_ent=%s", values1)
            cursor.execute("UPDATE raschet SET Comment=(Comment || ',' || %s) WHERE kust_ex=%s AND kust_ent=%s",
                           values2)
    connection.close()


def ME():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust_ex, kust_ent FROM raschet")
        PARES = cursor.fetchall()
        for PARE in PARES:
            kust_ex = PARE[0]
            kust_ent = PARE[1]
            cursor.execute("SELECT m_e FROM exit_ WHERE kust = %s", (kust_ex,))
            exit_ME = cursor.fetchone()[0]
            cursor.execute("SELECT m_e FROM enterance WHERE kust = %s", (kust_ent,))
            enter_ME = cursor.fetchone()[0]
            comb = str(exit_ME) + str(enter_ME)
            values = (comb,)
            cursor.execute("SELECT distance FROM distance WHERE meme = %s", values)
            values1 = (cursor.fetchone()[0], kust_ex, kust_ent)
            cursor.execute("UPDATE raschet SET m_e_rating = %s WHERE kust_ex=%s AND kust_ent=%s", values1)
    connection.close()


def SNPH():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT kust_ex, kust_ent FROM raschet")
        PARES = cursor.fetchall()
        for PARE in PARES:
            kust_ex = PARE[0]
            kust_ent = PARE[1]
            cursor.execute("SELECT SNPH FROM exit_ WHERE kust=%s", (kust_ex,))
            exit_SNPH = cursor.fetchone()[0]
            cursor.execute("SELECT SNPH FROM enterance WHERE kust=%s", (kust_ent,))
            enter_SNPH = cursor.fetchone()[0]
            values1 = (kust_ex, kust_ent)
            if exit_SNPH == 1 and enter_SNPH == 0:  # СНПХ едет на куст не буримый для СНПХ. Удаляем
                cursor.execute("DELETE FROM raschet WHERE kust_ex=%s AND kust_ent=%s", values1)


def clear():
    # Очищаем рабочие таблицы
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM exit_")
        cursor.execute("DELETE FROM enterance")
        cursor.execute("DELETE FROM raschet")
        cursor.execute("DELETE FROM for_handmade_raschet")
        cursor.execute("DELETE FROM auto_raschet")
    connection.close()


def sort():
    # Сортируем таблицы по времени
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM exit_")
        sort_exit_ = cursor.fetchall()
        sort_exit_.sort(key=lambda a: datetime.datetime.strptime(str(a[2]), '%Y-%m-%d'))
        cursor.execute("DELETE FROM exit_")
        for elem in sort_exit_:
            cursor.execute("INSERT INTO exit_(kust, m_e, exit_date, GP, RUO, SNPH) VALUES(%s, %s, %s, %s, %s, %s)",
                           elem)

        cursor.execute("SELECT * FROM enterance")
        sort_enterance = cursor.fetchall()
        for_sorting = []
        cursor.execute("DELETE FROM enterance")
        for elem in sort_enterance:
            if elem[2] == 'готов':
                cursor.execute("INSERT INTO enterance(kust, m_e, first_stage, second_stage, GP, RUO, SNPH)"
                               "VALUES(%s, %s, %s, %s, %s, %s, %s)", elem)
            else:
                for_sorting.append(elem)
        for_sorting.sort(key=lambda a: datetime.datetime.strptime(str(a[2]), '%Y-%m-%d'))
        for elem in for_sorting:
            cursor.execute("INSERT INTO enterance(kust, m_e, first_stage, second_stage, GP, RUO, SNPH) "
                           "VALUES(%s, %s, %s, %s, %s, %s, %s)", elem)
    connection.close()


def get_rating(Rating: NamedTuple):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE raschet SET GEN_rating = "
            "GP_rating*%s+first_stage_rating*%s+second_stage_rating*%s+RUO_rating*%s+m_e_rating*%s", Rating)
    connection.close()


def raschet():
    GP()
    Ist()
    IInd()
    RUO()
    ME()
    SNPH()
    get_rating(Rating)
