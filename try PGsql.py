import psycopg2
from BD_connection import host, user, password, db_name, port

# connection = psycopg2.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=db_name,
#     port=port
# )
#
# with connection.cursor() as curs:
#     curs.execute("""INSERT INTO exit_ (kust, m_e, exit_date, gp, ruo, snph) VALUES ('323', 'sfs', '24rewds3', 270,
#     'ruo', '3w')""")
#
# connection.close()
#

def put_string_into_BD(values: tuple):
    with connection.cursor() as curs:
        curs.execute("""INSERT INTO exit_ VALUES (%s, %s, %s, %s, %s, %s);""", values)



connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port
)

connection.autocommit = True

values = ("45у", "pro", "13-11-2023", 320, 1, 0)
put_string_into_BD(values)

connection.close()



