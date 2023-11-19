from Raschet import handmade_raschet, auto_raschet
from Raschet_filling import clear, sort, raschet
from put_inf_into_DB import exits_into_DB, enterances_into_DB


def main(start_string: int, finish_string: int):
    clear()
    exits_into_DB(start_string, finish_string)
    enterances_into_DB(start_string, finish_string)
    sort()
    raschet()
    handmade_raschet()
    auto_raschet()



if __name__ == "__main__":
    main(44, 110)
    print("Все штатно")
