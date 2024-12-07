import pymongo
from bson.objectid import ObjectId

# Підключення до сервера MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Створення бази даних та колекції
db = client["expense_manager"]
expenses = db["expenses"]

# Функції для CRUD операцій

# 1. Додавання витрати
def add_expense(name, amount, category, date):
    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    expenses.insert_one(expense)
    print(f"Витрата '{name}' додана успішно.")

# 2. Отримання всіх витрат
def get_expenses():
    print("\nСписок витрат:")
    for expense in expenses.find():
        print(expense)

# 3. Оновлення витрати
def update_expense(expense_id, updated_data):
    try:
        query = {"_id": ObjectId(expense_id)}
        new_data = {"$set": updated_data}
        result = expenses.update_one(query, new_data)
        if result.modified_count > 0:
            print("Витрата оновлена успішно.")
        else:
            print("Витрата не знайдена або не змінена.")
    except Exception as e:
        print(f"Помилка: {e}")

# 4. Видалення витрати
def delete_expense(expense_id):
    try:
        result = expenses.delete_one({"_id": ObjectId(expense_id)})
        if result.deleted_count > 0:
            print("Витрата видалена успішно.")
        else:
            print("Витрата не знайдена.")
    except Exception as e:
        print(f"Помилка: {e}")

# Основний цикл програми
def main():
    while True:
        print("\nУправління витратами:")
        print("1. Додати витрату")
        print("2. Показати всі витрати")
        print("3. Оновити витрату")
        print("4. Видалити витрату")
        print("5. Вийти")
        
        choice = input("Оберіть дію: ").strip()
        
        if choice == "1":
            name = input("Назва витрати: ").strip()
            if not name:
                print("Назва витрати не може бути порожньою.")
                continue
            try:
                amount = float(input("Сума: ").strip())
                if amount <= 0:
                    print("Сума повинна бути більшою за нуль.")
                    continue
            except ValueError:
                print("Сума повинна бути числом.")
                continue
            category = input("Категорія (наприклад, 'Їжа', 'Транспорт'): ").strip()
            if not category:
                print("Категорія не може бути порожньою.")
                continue
            date = input("Дата (у форматі YYYY-MM-DD): ").strip()
            if not date:
                print("Дата не може бути порожньою.")
                continue
            add_expense(name, amount, category, date)
        
        elif choice == "2":
            get_expenses()
        
        elif choice == "3":
            expense_id = input("ID витрати: ").strip()
            if not expense_id:
                print("ID витрати не може бути порожнім.")
                continue
            field = input("Яке поле оновити (name, amount, category, date): ").strip()
            if field not in ["name", "amount", "category", "date"]:
                print("Невірне поле для оновлення.")
                continue
            new_value = input(f"Нове значення для {field}: ").strip()
            if field == "amount":
                try:
                    new_value = float(new_value)
                except ValueError:
                    print("Сума повинна бути числом.")
                    continue
            update_expense(expense_id, {field: new_value})
        
        elif choice == "4":
            expense_id = input("ID витрати: ").strip()
            if not expense_id:
                print("ID витрати не може бути порожнім.")
                continue
            delete_expense(expense_id)
        
        elif choice == "5":
            print("Завершення програми.")
            break
        
        else:
            print("Невірний вибір. Спробуйте ще раз.")

# Запуск програми
if __name__ == "__main__":
    main()