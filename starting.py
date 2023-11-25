import psycopg2

import Raschet
from Raschet_filling import clear, sort, raschet
from put_inf_into_DB import export_exits, export_enterances
from get_dop_inf import host, user, password, db_name, port

def main(start_string: int, finish_string: int):
    clear()
    export_exits(start_string, finish_string)
    export_enterances(start_string, finish_string)
    sort()
    raschet()
    Raschet.handmade_raschet()
    Raschet.auto_raschet()



if __name__ == "__main__":
    main(51, 117)
    print("Все штатно")
