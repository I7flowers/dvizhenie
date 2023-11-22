import sqlite3
import openpyxl
from get_dop_inf import m_e_spisok, GP_spisok
from typing import NamedTuple


class Exits(NamedTuple):
    kust: str
    m_e: str
    exit_date: str
    GP: int
    RUO: bool
    SNPH: bool


class Enterances(NamedTuple):
    kust: str
    m_e: str
    Ist_stage: str
    IInd_stage: str
    GP: int
    RUO: bool
    SNPH: bool


def import_exits(start_string: int, finish_string: int) -> list:
    # """Импортируем данные из Экселя и вставляем в список"""
    wb = openpyxl.load_workbook('Движение_БУ.xlsx', data_only=True)
    ws = wb['Движение_БУ']
    Exits_: [list] = []
    for number_of_string in range(start_string, finish_string):
        kust = ws.cell(number_of_string, 4).value
        m_e = ws.cell(number_of_string, 5).value
        if m_e is not None and m_e not in m_e_spisok:
            print("В строке №", number_of_string, "ошибка в названии месторождения. Нужно исправить")
        exit_date = str(ws.cell(number_of_string, 6).value)[0:10]
        GP = ws.cell(number_of_string, 8).value
        if GP is not None and GP not in GP_spisok:
            print("В строке №", number_of_string, "ошибка в грузоподъемности. Нужно исправить")
        RUO = ws.cell(number_of_string, 9).value
        if RUO is not None and RUO != 0 and RUO != 1:
            print("В строке №", number_of_string, "ошибка в типе БР. Нужно исправить")
        SNPH = ws.cell(number_of_string, 10).value
        if SNPH is not None and SNPH != 0 and SNPH != 1:
            print("В строке №", number_of_string, "ошибка в SNPH. Нужно исправить")
        Exit_ = Exits(kust, m_e, exit_date, GP, RUO, SNPH)
        if Exit_.kust == Exit_.m_e == Exit_.GP is None:
            continue
        else:
            Exits_.append(Exit_)
    return Exits_


def export_exits(start_string: int, finish_string: int):
    # """Полученный список вставляем в БД"""
    Exits_ = import_exits(start_string, finish_string)
    with sqlite3.connect("DB1.db") as db:
        cursor = db.cursor()
        for Exit_ in Exits_:
            cursor.execute("INSERT INTO Exit_ VALUES (?, ?, ?, ?, ?, ?);",
                           (Exit_.kust, Exit_.m_e, Exit_.exit_date, Exit_.GP, Exit_.RUO, Exit_.SNPH))


def import_enterances(start_string: int, finish_string: int) -> list:
    # """Импортируем данные из Экселя и вставляем в список"""
    wb = openpyxl.load_workbook('Движение_БУ.xlsx', data_only=True)
    ws = wb['Движение_БУ']
    Enterances_: [list] = []
    for number_of_string in range(start_string, finish_string):
        kust = ws.cell(number_of_string, 12).value
        m_e = ws.cell(number_of_string, 13).value
        if m_e is not None and m_e not in m_e_spisok:
            print("В строке №", number_of_string, "ошибка в названии месторождения. Нужно исправить")
        Ist_stage = str(ws.cell(number_of_string, 14).value)[0:10]
        IInd_stage = str(ws.cell(number_of_string, 15).value)[0:10]
        GP = ws.cell(number_of_string, 17).value
        if GP is not None and GP not in GP_spisok:
            print("В строке №", number_of_string, "ошибка в грузоподъемности. Нужно исправить")
        RUO = ws.cell(number_of_string, 19).value
        if RUO is not None and RUO != 0 and RUO != 1:
            print("В строке №", number_of_string, "ошибка в типе БР. Нужно исправить")
        SNPH = ws.cell(number_of_string, 20).value
        if SNPH is not None and SNPH != 0 and SNPH != 1:
            print("В строке №", number_of_string, "ошибка в SNPH. Нужно исправить")
        Enterance = Enterances(kust, m_e, Ist_stage, IInd_stage, GP, RUO, SNPH)
        if Enterance.kust == Enterance.m_e == Enterance.GP is None:
            continue
        else:
            Enterances_.append(Enterance)
    return Enterances_


def export_enterances(start_string: int, finish_string: int):
    # """Полученный список вставляем в БД"""
    Enterances_ = import_enterances(start_string, finish_string)
    with sqlite3.connect("DB1.db") as db:
        cursor = db.cursor()
        for Enterance in Enterances_:
            cursor.execute("INSERT INTO Enterance VALUES (?, ?, ?, ?, ?, ?, ?);",
                           (Enterance.kust, Enterance.m_e, Enterance.Ist_stage,
                            Enterance.IInd_stage, Enterance.GP, Enterance.RUO, Enterance.SNPH))
