class to_do_list:
    def __init__(self):
        self.counter = 0
        self.file = ""

    def create_file(self, path):
        import os
        filepath = path
        if not os.path.exists(filepath):
            os.mkdir(filepath)

        self.file = filepath + "/to_do_list.txt"
        file = open(self.file, "a")

        file = open(self.file, "r")
        self.counter = len(file.readlines())

        file.close()


    def print_list(self):
        file = open(self.file, "r")

        print("TO-DO LIST\n")

        task = file.readline()
        task_len = len(task)
        if(task_len != 0):
            print("|", "-" * 90)
            while task:
                print("|", task[:len(task)-1])
                print("|", "-" * 90)
                task = file.readline()

        else:
            print("-" * 90, "\n*ПУСТО*\n" + "-" * 90)
        file.close()

    def add_task(self, task):
        file = open(self.file, "a")
        self.counter += 1
        file.write(str(self.counter) + "\t" + str(task) + "\n")

        file.close()

    def delete_task(self, delete_task):
        import ctypes
        file = open(self.file, "r")
        tasks = file.readlines()

        class uncorrect_number(BaseException):
            pass

        class not_exist_number(BaseException):
            pass

        try:
            if (not delete_task.isdigit()) or int(delete_task) <= 0:
                raise uncorrect_number("Некорректный номер удаляемого задания.\nВведённый номер: " + delete_task)
            if int(delete_task) > self.counter:
                raise not_exist_number("Удаляемый номер " + delete_task + " превышает максимальный номер в списке.")

        except uncorrect_number as err_uncorrect_number:
            ctypes.windll.user32.MessageBoxW(0, str(err_uncorrect_number), "ОШИБКА", 16)
            return
        except not_exist_number as err_not_exist_number:
            ctypes.windll.user32.MessageBoxW(0, str(err_not_exist_number), "ОШИБКА", 16)
            return

        file = open(self.file, "w")

        local_counter = 1
        for task in tasks:
            if task[:task.find("\t")] != delete_task:
                file.write(str(local_counter) + task[task.find("\t"):])
                local_counter += 1
            else:
                self.counter -= 1
        file.close()

    def clear_list(self):
        file = open(self.file, "w")
        self.counter = 0
        file.close()

def main():
    import os

    path = os.getcwd()
    to_do = to_do_list()
    to_do.create_file(path)

    selected_number = 0

    while int(selected_number) != 4:
        to_do.print_list()
        selected_number = input("\nВведите команду для работы с To-Do List:\n"
                                    "1 - добавить задание в список\n"
                                    "2 - удалить задание из списка\n"
                                    "3 - очистить список заданий\n"
                                    "4 - завершить работу со списком\nКоманда: ")
        try:
            if not selected_number.isdigit() or int(selected_number) > 4 or int(selected_number) < 1:
                raise Exception("Команды " + str(selected_number) + " нет в списке.")
            selected_number = int(selected_number)
            if selected_number == 1:
                task_to_add = input("Введите задание для добавления в список:")
                to_do.add_task(task_to_add)
            elif selected_number == 2:
                task_to_del = input("Введите номера задания для удаления из списка:")
                to_do.delete_task(task_to_del)
            elif selected_number == 3:
                to_do.clear_list()
        except Exception as input_err:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, str(input_err), "ОШИБКА", 16)
            selected_number = 0
            os.system('cls')
            continue
        os.system('cls')
main()
