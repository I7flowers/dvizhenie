import sqlite3
import datetime


def handmade_raschet():
    with (sqlite3.connect("DB1.db") as db):
        cursor = db.cursor()
        # выбираем кусты котрые выходят в следубщие 45 суток
        cursor.execute("SELECT kust, exit_date FROM Exit_")
        kust_end = cursor.fetchall()
        today = datetime.date.today()
        kust_end_handmade = []
        for elem in kust_end:
            end = datetime.datetime.strptime(elem[1], '%Y-%m-%d').date()
            if today + datetime.timedelta(45) >= end:
                kust_end_handmade.append(str(elem[0])   )
            else:
                break
        cursor.execute("SELECT * FROM Raschet")
        for KPexKPent in cursor.fetchall():
            kust_ex = KPexKPent[0]
            if kust_ex in kust_end_handmade:
                cursor.execute(
                    "INSERT INTO For_handmade_raschet(kust_ex, kust_ent, GEN_rating, "
                    "GP_rating, Ist_stage_rating, IInd_stage_rating, RUO_rating, m_e_rating, Comment) "
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    KPexKPent)

    dvizh_opr = str(input('Введите кусты, движение на которые определено вручную:', ))
    spis_dvizh_opr = dvizh_opr.split()

    # Удаляем результаты ручного определения из raschet
    with sqlite3.connect("DB1.db") as db:
        cursor = db.cursor()
        for elem in spis_dvizh_opr:
            cursor.execute("DELETE FROM Raschet WHERE kust_ent=?", (elem,))

        cursor.execute("SELECT DISTINCT kust_ex FROM for_handmade_raschet")
        for elem in cursor.fetchall():
            cursor.execute("DELETE FROM Raschet WHERE kust_ex=?", elem)


def auto_raschet():
    with sqlite3.connect("DB1.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT kust_ex FROM raschet")
        for kust_ex in cursor.fetchall():
            cursor.execute("SELECT max(gen_rating) FROM Raschet WHERE kust_ex=?", kust_ex)
            max_gen_rating = cursor.fetchone()[0]
            if max_gen_rating is None:
                cursor.execute("INSERT INTO auto_raschet(kust_ex, kust_ent, GEN_rating) VALUES(?, ?, ?)",
                               (kust_ex[0], 'нет кандидата', ' '))
            else:
                values = (kust_ex[0], max_gen_rating)
                cursor.execute("SELECT kust_ex, kust_ent, GEN_rating FROM Raschet WHERE kust_ex=? AND GEN_rating=?",
                               values)
                finish_solution = cursor.fetchone()
                cursor.execute("DELETE FROM Raschet WHERE kust_ent=?", (finish_solution[1],))
                cursor.execute("INSERT INTO auto_raschet(kust_ex, kust_ent, GEN_rating) VALUES(?, ?, ?)",
                               finish_solution)

