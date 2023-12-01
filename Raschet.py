import datetime

import psycopg2

from BD_connection import host, user, password, db_name, port


def handmade_raschet():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        # выбираем кусты котрые выходят в следующие 45 суток
        today_and_45 = datetime.date.today()+datetime.timedelta(45)

        cursor.execute("SELECT * FROM raschet WHERE exit_date<=%s ORDER BY exit_date, kust_ex", (today_and_45, ))
        for_handmade = cursor.fetchall()
        for elem in for_handmade:
            cursor.execute("INSERT INTO for_handmade_raschet VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", elem)
        cursor.execute("DELETE FROM raschet WHERE exit_date<=%s", (today_and_45, ))

    dvizh_opr = str(input('Введите кусты, движение на которые определено вручную (через пробел):', ))
    spis_dvizh_opr = dvizh_opr.split()

    # Удаляем результаты ручного определения из raschet
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        for elem in spis_dvizh_opr:
            cursor.execute("DELETE FROM raschet WHERE kust_ent=%s", (elem,))
    connection.close()


def auto_raschet():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT kust_ex FROM raschet")
        for kust_ex in cursor.fetchall():
            cursor.execute("SELECT max(gen_rating) FROM raschet WHERE kust_ex=%s", kust_ex)
            max_gen_rating = str(cursor.fetchone()[0])
            if max_gen_rating == 'None':
                cursor.execute("INSERT INTO auto_raschet(kust_ex, kust_ent) VALUES(%s, %s)",
                               (kust_ex[0], 'нет кандидата'))
            else:
                values = (kust_ex[0], max_gen_rating)
                cursor.execute("SELECT kust_ex, kust_ent, GEN_rating FROM raschet WHERE kust_ex=%s AND GEN_rating=%s "
                               "ORDER BY exit_date, kust_ex",
                               values)
                finish_solution = cursor.fetchone()
                cursor.execute("DELETE FROM raschet WHERE kust_ent=%s", (finish_solution[1],))
                cursor.execute("INSERT INTO auto_raschet(kust_ex, kust_ent, GEN_rating) VALUES(%s, %s, %s)",
                               finish_solution)
    connection.close()
