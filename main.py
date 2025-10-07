# 🏢 Employee Management System (SQLite Edition)
# Author: Alen Chavez
# Description:
# Console-based employee & manager management system using SQLite for
# persistent storage. Includes sample data, CRUD operations, and
# manager–subordinate relationships.

import sqlite3
import os

DB_FILE = "company.db"


# -------------------- Database Setup --------------------

def init_db():
    """Initialize database tables and insert sample data if empty."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eid TEXT NOT NULL,
        name TEXT NOT NULL,
        is_manager INTEGER NOT NULL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subordinates (
        manager_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,
        FOREIGN KEY(manager_id) REFERENCES employees(id),
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )
    """)

    # Add sample employees/managers if empty
    cur.execute("SELECT COUNT(*) FROM employees")
    count = cur.fetchone()[0]
    if count == 0:
        print("🧪 Adding sample employees & managers...")

        sample_data = [
            ("0001", "Alice Johnson", 1),  # Manager
            ("0002", "Bob Smith", 1),      # Manager
            ("0003", "Carla Martinez", 0),
            ("0004", "David Kim", 0),
            ("0005", "Elena Lopez", 0),
        ]

        ids = {}
        for eid, name, is_mgr in sample_data:
            cur.execute("INSERT INTO employees (eid, name, is_manager) VALUES (?, ?, ?)", (eid, name, is_mgr))
            ids[name] = cur.lastrowid

        # Assign subordinates: Carla & David to Alice; Elena to Bob
        cur.execute("INSERT INTO subordinates (manager_id, employee_id) VALUES (?, ?)", (ids["Alice Johnson"], ids["Carla Martinez"]))
        cur.execute("INSERT INTO subordinates (manager_id, employee_id) VALUES (?, ?)", (ids["Alice Johnson"], ids["David Kim"]))
        cur.execute("INSERT INTO subordinates (manager_id, employee_id) VALUES (?, ?)", (ids["Bob Smith"], ids["Elena Lopez"]))

        print("✅ Sample data inserted.")

    conn.commit()
    conn.close()


# -------------------- Helper Functions --------------------

def add_employee():
    eid = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    role = input("Is this a Manager? (y/n): ").strip().lower()
    is_mgr = 1 if role == 'y' else 0

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (eid, name, is_manager) VALUES (?, ?, ?)", (eid, name, is_mgr))
    conn.commit()
    conn.close()
    print(f"✅ {name} added successfully.")


def list_employees():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, eid, name, is_manager FROM employees")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No employees found.")
        return

    print("\n📋 Employee List:")
    for r in rows:
        role = "Manager" if r[3] == 1 else "Employee"
        print(f"[{r[1]}] {r[2]} - {role}")


def delete_employee():
    list_employees()
    eid = input("\nEnter Employee ID to delete: ").strip()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM employees WHERE eid = ?", (eid,))
    row = cur.fetchone()
    if not row:
        print("❌ Employee not found.")
        conn.close()
        return

    emp_id, name = row

    # Remove from subordinates first
    cur.execute("DELETE FROM subordinates WHERE employee_id = ? OR manager_id = ?", (emp_id, emp_id))
    cur.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()
    print(f"🗑 {name} deleted successfully.")


def update_employee():
    list_employees()
    eid = input("\nEnter Employee ID to update: ").strip()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, is_manager FROM employees WHERE eid = ?", (eid,))
    row = cur.fetchone()
    if not row:
        print("❌ Employee not found.")
        conn.close()
        return

    emp_id, old_name, old_mgr = row
    new_name = input(f"Enter new name (leave blank to keep '{old_name}'): ").strip()
    new_role = input("Change role? (m = Manager, e = Employee, leave blank to keep current): ").strip().lower()

    if new_name:
        cur.execute("UPDATE employees SET name = ? WHERE id = ?", (new_name, emp_id))

    if new_role == 'm':
        cur.execute("UPDATE employees SET is_manager = 1 WHERE id = ?", (emp_id,))
    elif new_role == 'e':
        cur.execute("UPDATE employees SET is_manager = 0 WHERE id = ?", (emp_id,))

    conn.commit()
    conn.close()
    print(f"✏️ Employee {eid} updated successfully.")


def assign_subordinate():
    print("\nAssign Subordinate to Manager")
    list_employees()
    mgr_eid = input("\nEnter Manager ID: ").strip()
    emp_eid = input("Enter Employee ID to assign: ").strip()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT id, is_manager FROM employees WHERE eid = ?", (mgr_eid,))
    mgr = cur.fetchone()
    cur.execute("SELECT id FROM employees WHERE eid = ?", (emp_eid,))
    emp = cur.fetchone()

    if not mgr or not emp:
        print("❌ Invalid manager or employee ID.")
        conn.close()
        return

    if mgr[1] != 1:
        print("❌ Selected manager ID does not belong to a manager.")
        conn.close()
        return

    cur.execute("INSERT INTO subordinates (manager_id, employee_id) VALUES (?, ?)", (mgr[0], emp[0]))
    conn.commit()
    conn.close()
    print("✅ Subordinate assigned successfully.")


def view_manager_teams():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    SELECT m.name, e.name
    FROM subordinates s
    JOIN employees m ON s.manager_id = m.id
    JOIN employees e ON s.employee_id = e.id
    ORDER BY m.name
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No manager-subordinate relationships found.")
        return

    print("\n👥 Manager Teams:")
    teams = {}
    for manager, employee in rows:
        teams.setdefault(manager, []).append(employee)

    for mgr, subs in teams.items():
        print(f"- {mgr}: {', '.join(subs)}")


# -------------------- Menu --------------------

def main_menu():
    print("\n===== Employee Management System (SQL Edition) =====")
    print("[1] Add Employee")
    print("[2] List Employees")
    print("[3] Update Employee")
    print("[4] Delete Employee")
    print("[5] Assign Subordinate to Manager")
    print("[6] View Manager Teams")
    print("[7] Exit")
    return input("Enter your choice: ").strip()


def main():
    init_db()
    while True:
        choice = main_menu()
        if choice == '1':
            add_employee()
        elif choice == '2':
            list_employees()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            assign_subordinate()
        elif choice == '6':
            view_manager_teams()
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

