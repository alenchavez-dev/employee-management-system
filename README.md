# 🧾 Employee Management System

Simple Python console app modeling **Employees** and **Managers** (inheritance + composition).  
Supports adding managers with subordinates, zero-padded IDs, and **left-aligned** output for clarity.

## 🚀 Features
- `Employee` with name + zero-padded ID
- `Manager(Employee)` with a list of subordinates (composition)
- CLI prompts to add employees/managers and their teams
- Clean, left-aligned printout of the organization

## 📂 Structure
    employee-management-system/
    ├── employee_management.py
    └── README.md

## ▶️ Run
    python3 employee_management.py

## 📝 Sample Output
    Printing Employee List
    0123: Alen
    Alen's Employees
    1111: Jason
    2222: Mike

## 💡 Notes
- Empty subordinate name → `Unknown`
- Empty subordinate id → `9999` (still shown zero-padded by display)

## 🧑‍💻 Author
Alen Chavez

## 📝 License
MIT License
