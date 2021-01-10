# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List

# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения (список из трех чисел). Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены по алфавиту; вывод на экран информации о людях, чьи
# дни рождения приходятся на месяц, значение которого введено с клавиатуры; если таких
# нет, выдать на дисплей соответствующее сообщение.


@dataclass(frozen=True)
class Worker:
    las_name: str
    name: str
    tel: int
    date: list


@dataclass
class Staff:
    workers: List[Worker] = field(default_factory=lambda: [])

    def add(self, las_name, name, tel, date):
        self.workers.append(
        Worker(
            las_name=las_name,
            name=name,
            tel=tel,
            date=date
        )
        )
        self.workers.sort(key=lambda worker: worker.name)

    def __str__(self):
        # Заголовок таблицы.
        table = []
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            '-' * 4,
            '-' * 15,
            '-' * 15,
            '-' * 20,
            '-' * 20
        )
        table.append(line)
        table.append((
                "| {:^4} | {:^15} | {:^15} | {:^20} | {:^20} |".format(
                    "№",
                    "Фамилия",
                    "Имя",
                    "Телефон",
                    "Дата рождения"
                )
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(self.workers, 1):
            table.append(
                '| {:>4} | {:<15} | {:<15} | {:>20} | {:^20} |'.format(
                        idx,
                        worker.las_name,
                        worker.name,
                        worker.tel,
                        ".".join(map(str, worker.date))
                    )
            )
            table.append(line)
        return '\n'.join(table)

    def load(self, filename):
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)
        self.workers = []
        for worker_element in tree:
            las_name, name, tel, date = None, None, None, None
        for element in worker_element:
            if element.tag == 'las_name':
                las_name = element.text
            elif element.tag == 'name':
                name = element.text
            elif element.tag == 'tel':
                tel = int(element.text)
            elif element.tag == 'date':
                date = list(map(int, element.text.split(" ")))
        if las_name is not None and name is not None \
                and tel is not None and date is not None:
            self.workers.append(
                Worker(
                    las_name=las_name,
                    name=name,
                    tel=tel,
                    date=date
                )
            )

    def save(self, filename):
        root = ET.Element('workers')
        for worker in self.workers:
            worker_element = ET.Element('worker')

            las_name_element = ET.SubElement(worker_element, 'las_name')
            las_name_element.text = worker.las_name

            name_element = ET.SubElement(worker_element, 'name')
            name_element.text = worker.name

            tel_element = ET.SubElement(worker_element, 'tel')
            tel_element.text = worker.tel

            date_element = ET.SubElement(worker_element, 'date')
            date_element.text = ' '.join(map(str, worker.date))

            root.append(worker_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':
    staff = Staff()
    while True:
        command = input("Enter command> ").lower()

        if command == "exit":
            break

        elif command == "add":
            las_name = str(input("Enter last name>  "))
            name = str(input("Enter first name> "))
            tel = str(input("Enter phone> +"))
            date = list(map(int, input("Enter birthdate separated by space> ").split(" ")))
            staff.add(las_name, name, tel, date)

        elif command == "list":
            print(staff)

        elif command.startswith('load '):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(' ', maxsplit=1)
            staff.load(parts[1])

        elif command.startswith('save '):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(' ', maxsplit=1)
            staff.save(parts[1])

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить работника;")
            print("list - вывести список работников;")
            print("task - вывести сотрудников определенной даты рождения")
            print("load <имя файла> - загрузить данные из файла;")
            print("save <имя файла> - сохранить данные в файл;")
            print("exit - выход из программы;")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)