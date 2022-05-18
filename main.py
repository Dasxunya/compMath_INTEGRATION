import colors as color
import functions as f


def main():
    try:
        print(
            color.BLUE + "\nВыберите режим ввода для интегрирования методом Симпсона:\n1 ~ с клавиатуры\n2 ~ хочу выйти")
        choice = input("> ")
        while (choice != '1') and (choice != '2'):
            print("Воспользуйтесь командами, предложенными в меню!")
            choice = input("> ")
        if choice == "2":
            print(color.GREEN + "\nВы успешно вышли")
            exit(0)
        else:
            # из консоли
            answer, abs_error, n = f.console_decide()
            print(
                f"\nРезультат по методу Симпсона: {answer:.8f}\nАбсолютная погрешность: {abs_error}\nКоличество разбиений: {n}")

    except KeyboardInterrupt:
        print(color.RED + "\n\nПрограмма прервана:(")
        exit(1)


main()
