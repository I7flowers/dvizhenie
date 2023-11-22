import Raschet
from Raschet_filling import clear, sort, raschet
from put_inf_into_DB import export_exits, export_enterances


def main(start_string: int, finish_string: int):
    clear()
    export_exits(start_string, finish_string)
    export_enterances(start_string, finish_string)
    sort()
    raschet()
    Raschet.handmade_raschet()
    Raschet.auto_raschet()


if __name__ == "__main__":
    main(44, 75)
    print("Все штатно")
