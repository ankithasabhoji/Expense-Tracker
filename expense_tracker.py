
import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.txt")


def read_expenses():
    expenses = []

    if not DATA_FILE.exists():
        return expenses

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) != 3:
                continue

            item, amount, category = [value.strip() for value in row]

            try:
                amount = int(amount)
            except ValueError:
                continue

            if item and category and amount > 0:
                expenses.append([item, amount, category])

    return expenses


def store_expenses(expenses):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)

    print("Expenses saved successfully.")


def calculate_total(expenses):
    return sum(detail[1] for detail in expenses)


def category_report(expenses):
    if not expenses:
        print("No expenses available.")
        return

    category_totals = {}

    for item, amount, category in expenses:
        category_totals[category] = category_totals.get(category, 0) + amount

    print("\n--- Category-wise Expense Report ---")

    for category, total in category_totals.items():
        print(f"{category}: Rs. {total}")


def display_report(expenses):
    if not expenses:
        print("No expenses available.")
        return

    amounts = [detail[1] for detail in expenses]
    total = calculate_total(expenses)

    print("\n--- Expense Report ---")
    print(f"Total expenses: Rs. {total}")
    print(f"Average expense: Rs. {total / len(expenses):.2f}")
    print(f"Highest expense: Rs. {max(amounts)}")
    print(f"Lowest expense: Rs. {min(amounts)}")


def add_expense(expenses):
    while True:
        item = input("Enter expense item (or 'done' to finish): ").strip()

        if item.lower() == "done":
            break

        if not item:
            print("Expense item cannot be empty.")
            continue

        category = input("Enter category: ").strip()

        if not category:
            print("Category cannot be empty.")
            continue

        try:
            amount = int(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

        except ValueError:
            print("Please enter a valid whole number.")
            continue

        detail = [item, amount, category]
        expenses.append(detail)

        print("Expense added:", detail)

    store_expenses(expenses)


def search_expense(expenses):
    item = input("Enter an expense item to search: ").strip()

    matches = [
        detail for detail in expenses
        if item.lower() == detail[0].lower()
    ]

    if not matches:
        print("No matching expense found.")
        return

    for detail in matches:
        print(f"{detail[0]} | Rs. {detail[1]} | {detail[2]}")


def select_expense(expenses, action):
    item = input(f"Enter the expense item to {action}: ").strip()

    matches = [
        detail for detail in expenses
        if item.lower() == detail[0].lower()
    ]

    if not matches:
        print("No matching expense found.")
        return None

    print("\nMatching expenses:")

    for index, detail in enumerate(matches, start=1):
        print(f"{index}. {detail[0]} | Rs. {detail[1]} | {detail[2]}")

    try:
        choice = int(input(f"Which one to {action}? "))

        if 1 <= choice <= len(matches):
            return matches[choice - 1]

    except ValueError:
        pass

    print("Invalid selection.")
    return None


def delete_expense(expenses):
    selected = select_expense(expenses, "delete")

    if selected is not None:
        expenses.remove(selected)
        store_expenses(expenses)
        print("Expense deleted successfully.")


def edit_expense(expenses):
    selected = select_expense(expenses, "edit")

    if selected is None:
        return

    choice = input(
        "What would you like to edit (category/amount)? "
    ).strip().lower()

    if choice == "category":
        category = input("Enter new category: ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        selected[2] = category

    elif choice == "amount":
        try:
            amount = int(input("Enter new amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

        except ValueError:
            print("Please enter a valid whole number.")
            return

        selected[1] = amount

    else:
        print("Invalid choice.")
        return

    store_expenses(expenses)
    print("Expense updated successfully.")


def main():
    expenses = read_expenses()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expense report")
        print("3. Category-wise report")
        print("4. Search expense")
        print("5. Delete expense")
        print("6. Edit expense")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            display_report(expenses)

        elif choice == "3":
            category_report(expenses)

        elif choice == "4":
            search_expense(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            edit_expense(expenses)

        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    main()
