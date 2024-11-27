from terminaltables import SingleTable
from colorama import Fore


def display_table(title, data, headers):
    table_data = [headers] + data
    table = SingleTable(table_data, title)
    print(Fore.YELLOW + table.table)