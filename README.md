# 🧾 Employee Management System (SQL Edition)

A console-based Python application that models **Employees** and **Managers** using **SQLite** for persistent storage.  
This upgraded version replaces in-memory lists with a relational database, adds CRUD operations, and includes **sample data** on first run for instant testing.

---

## 🚀 Features
- 🧍 **Employees** with unique zero-padded IDs and names  
- 👔 **Managers** with assignable subordinates (one-to-many relationships)  
- 🧠 **SQLite database (`company.db`)** for persistent employee and manager data  
- ✍️ **Create, Read, Update, and Delete** employees directly from the console  
- 🔗 Assign subordinates to managers with clean JOIN queries  
- 🧪 **Sample managers & employees** auto-inserted on first run for easy testing:
  - Alice Johnson → Manager of Carla & David  
  - Bob Smith → Manager of Elena  
- 📊 Manager–subordinate teams view with SQL JOIN

---

## 🧰 Tech Stack
- **Language:** Python 3  
- **Database:** SQLite (`company.db`, created automatically)  
- **No external libraries** — runs using only the Python standard library

---

## 📂 Project Structure
employee-management-system/
├── main.py
├── README.md
├── LICENSE
└── .gitignore

yaml
Copy code

---

## ▶️ How to Run
```bash
git clone https://github.com/alenchavez-dev/employee-management-system.git
cd employee-management-system
python3 main.py
