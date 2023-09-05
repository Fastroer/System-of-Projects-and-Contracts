import psycopg2
from datetime import datetime
from colorama import init, Fore


class Contract:

    @staticmethod
    def create_contract():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            name = input("Введите название договора: ")
            creation_date = datetime.now().date()
            sign_date = None
            status = "черновик"
            project_id = None

            query = "INSERT INTO contracts (name, creation_date, sign_date, status, project_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, creation_date, sign_date, status, project_id))

            conn.commit()
            conn.close()

            print(Fore.GREEN + "Договор успешно создан.")
        except Exception as e:
            print(Fore.RED + "Ошибка при создании договора:", str(e))

    @staticmethod
    def confirm_contract():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            contract_ID = int(input("Введите ID договора, который вы хотите подтвердить: "))

            check_query = "SELECT contract_id, status FROM contracts WHERE contract_id = %s AND status = %s"
            cursor.execute(check_query, (contract_ID, "черновик"))
            existing_contract = cursor.fetchone()

            if existing_contract:
                update_query = "UPDATE contracts SET status = %s, sign_date = %s WHERE contract_id = %s"
                new_status = "активен"
                sign_date = datetime.now().date()
                cursor.execute(update_query, (new_status, sign_date, contract_ID))
                conn.commit()
                print(Fore.GREEN + f"Договор с ID {contract_ID} успешно подтвержден.")
            else:
                print(Fore.YELLOW + f"Договор с ID {contract_ID} не найден или уже подтвержден.")

            conn.close()
        except Exception as e:
            print(Fore.RED + "Ошибка при подтверждении договора:", str(e))

    @staticmethod
    def complete_contract():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            contract_id = int(input("Введите ID договора, который вы хотите завершить: "))

            check_query = "SELECT contract_id, status FROM contracts WHERE contract_id = %s AND status = %s"
            cursor.execute(check_query, (contract_id, "активен"))
            existing_contract = cursor.fetchone()

            if existing_contract:
                update_query = "UPDATE contracts SET status = %s WHERE contract_id = %s"
                new_status = "завершен"
                cursor.execute(update_query, (new_status, contract_id))
                conn.commit()
                print(Fore.GREEN + f"Договор с ID {contract_id} успешно завершен.")
            else:
                print(Fore.YELLOW + f"Договор с ID {contract_id} не найден, не активен или уже завершен.")

            conn.close()
        except Exception as e:
            print(Fore.RED + "Ошибка при завершении договора:", str(e))


class Project:

    @staticmethod
    def create_project():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            name = input("Введите название проекта: ")
            creation_date = datetime.now().date()

            query = "INSERT INTO projects (name, creation_date) VALUES (%s, %s)"
            cursor.execute(query, (name, creation_date))

            conn.commit()
            conn.close()

            print(Fore.GREEN + "Проект успешно создан.")
        except Exception as e:
            print(Fore.RED + "Ошибка при создании проекта:", str(e))

    @staticmethod
    def add_contract_to_project():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            project_id = int(input("Введите ID проекта, к которому хотите подключить договор: "))
            contract_id = int(input("Введите ID договора, который хотите подключить к проекту: "))

            check_project_query = "SELECT project_id FROM projects WHERE project_id = %s"
            cursor.execute(check_project_query, (project_id,))
            existing_project = cursor.fetchone()

            if existing_project:
                check_contract_status_query = "SELECT status FROM contracts WHERE contract_id = %s"
                cursor.execute(check_contract_status_query, (contract_id,))
                contract_status = cursor.fetchone()

                if contract_status and contract_status[0] not in ["черновик", "завершен"]:
                    check_active_contract_query = "SELECT contract_id FROM contracts WHERE project_id = %s AND status = %s"
                    cursor.execute(check_active_contract_query, (project_id, "активен"))
                    existing_active_contract = cursor.fetchone()

                    if existing_active_contract:
                        print(Fore.YELLOW + f"У проекта с ID {project_id} уже есть активный договор.")
                    else:
                        update_contract_query = "UPDATE contracts SET project_id = %s WHERE contract_id = %s"
                        cursor.execute(update_contract_query, (project_id, contract_id))
                        conn.commit()
                        print(Fore.GREEN + f"Договор с ID {contract_id} успешно подключен к проекту с ID {project_id}.")
                else:
                    print(
                        Fore.YELLOW + f"Договор с ID {contract_id} имеет статус 'черновик' или 'завершен', и его нельзя подключить.")
            else:
                print(Fore.YELLOW + f"Проект с ID {project_id} не найден.")

            conn.close()
        except Exception as e:
            print(Fore.RED + "Ошибка при подключении договора к проекту:", str(e))

    @staticmethod
    def complete_contract_in_project():
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            project_id = int(input("Введите ID проекта, в котором хотите завершить договор: "))

            check_project_query = "SELECT project_id FROM projects WHERE project_id = %s"
            cursor.execute(check_project_query, (project_id,))
            existing_project = cursor.fetchone()

            if existing_project:
                update_contract_query = "UPDATE contracts SET status = %s WHERE project_id = %s AND status = %s"
                new_status = "завершен"
                cursor.execute(update_contract_query, (new_status, project_id, "активен"))
                conn.commit()
                print(Fore.GREEN + f"Договор в проекте с ID {project_id} успешно завершен.")
            else:
                print(Fore.YELLOW + f"Проект с ID {project_id} не найден или проект не активен.")

            conn.close()
        except Exception as e:
            print(Fore.RED + "Ошибка при завершении договора в проекте:", str(e))


def connect_to_database():
    db_params = {
        'dbname': 'contracts_and_projects',
        'user': 'user',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    return psycopg2.connect(**db_params)


class Menu(Contract, Project):

    def main_menu(self):
        while True:
            print("\nГлавное меню:")
            print("1. Договор")
            print("2. Проект")
            print("3. Просмотреть списки договоров и проектов")
            print("4. Завершить работу с программой")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.contract_menu()
            elif choice == "2":
                self.project_menu()
            elif choice == "3":
                self.view_lists()
            elif choice == "4":
                print("Программа завершена.")
                break
            else:
                print("Неправильный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

    def view_lists(self):
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            print("\nСписок договоров:")
            list_contracts_query = "SELECT contract_id, name, status FROM contracts"
            cursor.execute(list_contracts_query)
            contracts = cursor.fetchall()
            for contract in contracts:
                print(Fore.BLUE + f"ID: {contract[0]}, Название: {contract[1]}, Статус: {contract[2]}")

            print("\nСписок проектов:")
            list_projects_query = "SELECT project_id, name FROM projects"
            cursor.execute(list_projects_query)
            projects = cursor.fetchall()
            for project in projects:
                print(Fore.BLUE + f"ID: {project[0]}, Название: {project[1]}")

            conn.close()
        except Exception as e:
            print(Fore.RED + "Ошибка при просмотре списков:", str(e))

    def contract_menu(self):
        while True:
            print("\nМеню договора:")
            print("1. Создать договор")
            print("2. Подтвердить договор")
            print("3. Завершить договор")
            print("4. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_contract()
            elif choice == "2":
                self.confirm_contract()
            elif choice == "3":
                self.complete_contract()
            elif choice == "4":
                break
            else:
                print("Неправильный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

    def project_menu(self):
        while True:
            print("\nМеню проекта:")
            print("1. Создать проект")
            print("2. Добавить договор к проекту")
            print("3. Завершить договор в проекте")
            print("4. Назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.add_contract_to_project()
            elif choice == "3":
                self.complete_contract_in_project()
            elif choice == "4":
                break
            else:
                print("Неправильный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")


if __name__ == "__main__":
    init(autoreset=True)
    menu = Menu()
    menu.main_menu()
