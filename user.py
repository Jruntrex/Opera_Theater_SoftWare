import json

class Signin:
    """Логує користувачів."""

    def __init__(self, name: str, password: str, email: str = "") -> None:
        """
        Ініціалізує об'єкт Signin.

        Args:
            name (str): Ім'я користувача.
            password (str): Пароль користувача.
            email (str, optional): Email користувача. Defaults to "".
        """
        self.name = name
        self.password = password
        self.email = email

    def check_login(self) -> bool:
        """
        Перевіряє логін та пароль з файлу.

        Returns:
            bool: True, якщо вхід успішний, False в іншому випадку.
        """
        try:
            with open("ui/data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            if self.name in data:
                if data[self.name][0] == self.password:
                    self.email = data[self.name][1]
                    print(f"Вхід успішний. Вітаю, {self.name}!")
                    return True
                else:
                    print("Невірний пароль.")
                    return False
            else:
                print(f"Користувача '{self.name}' не знайдено.")
                return False

        except FileNotFoundError:
            print("Файл 'ui/data.json' не знайдено.")
            return False
        except json.JSONDecodeError:
            print("Помилка декодування JSON у файлі 'data.json'.")
            return False

    def download_data(self) -> bool:
        """
        Завантажує дані користувача з файлу.

        Returns:
            bool: True, якщо дані знайдено, False в іншому випадку.
        """
        try:
            with open("ui/data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if self.name in data:
                    self.email = data[self.name][1]
                    return True
                return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False


class Signup:
    """Реєструє нових користувачів."""

    def __init__(self, name: str, password: str, email: str) -> None:
        """
        Ініціалізує об'єкт Signup.

        Args:
            name (str): Ім'я користувача.
            password (str): Пароль користувача.
            email (str): Email користувача.
        """
        self.name = name
        self.password = password
        self.email = email

    def check_userdata(self) -> bool:
        """
        Перевіряє коректність даних користувача.

        Returns:
            bool: True, якщо дані коректні, False в іншому випадку.
        """
        if not (6 <= len(self.password) <= 10):
            print("Пароль має бути довжиною від 6 до 10 символів.")
            return False

        if not (3 <= len(self.name) <= 20):
            print("Ім'я користувача має бути довжиною від 3 до 20 символів.")
            return False

        if "@" not in self.email or self.email.count("@") != 1:
            print("Невірний формат email.")
            return False

        local_part, domain_part = self.email.split("@")
        if "." not in domain_part:
            print("Невірний формат email.")
            return False

        return True

    def save_data(self) -> str:
        """
        Зберігає дані користувача у файл.

        Returns:
            str: Повідомлення про результат операції.
        """
        if not self.check_userdata():
            return "Перевірка даних користувача не пройдена. Дані не збережено."

        try:
            try:
                with open("ui/data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            if self.name in data:
                return f"Користувач з логіном '{self.name}' вже існує."

            if any(data[user][1] == self.email for user in data):
                return f"Email '{self.email}' вже використовується."

            data[self.name] = (self.password, self.email)

            with open("ui/data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return f"Користувача '{self.name}' успішно зареєстровано."
        except IOError:
            return "Помилка запису у файл 'data.json'."


# Тестування
if __name__ == "__main__":
    print("=== Реєстрація ===")
    new_user = Signup("john_doe", "mypa55w", "john@example.com")
    registration_result = new_user.save_data()
    print(registration_result)

    print("\n=== Вхід ===")
    login_attempt = Signin("john_doe", "mypa55w")
    login_result = login_attempt.check_login()
    print("Результат входу:", login_result)

    print("\n=== Вхід з неправильним паролем ===")
    wrong_login_attempt = Signin("john_doe", "wrongpass")
    wrong_login_result = wrong_login_attempt.check_login()
    print("Результат входу:", wrong_login_result)

    print("\n=== Вхід неіснуючого користувача ===")
    no_user_attempt = Signin("fake_user", "somepass")
    no_user_result = no_user_attempt.check_login()
    print("Результат входу:", no_user_result)