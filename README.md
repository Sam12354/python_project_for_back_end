# 🪨 Gem Store - Flask Version

This is a web app built using **Flask**, **MySQL**, and **Jinja2**, where users can register, log in, create, edit and delete gems or minerals.

Originally built with Node.js, Express, and MongoDB, this project is being reimplemented using Flask and MySQL.

---

## 📌 Important Notes

- This project **runs in PyCharm** using the command: "python -m src.main"


- It **does not currently run in VS Code** — I'm still working on that part. If you know why, feel free to help or open an issue!

- Some things may not be perfect — I’m still learning Python and SQLAlchemy. The project works for me in PyCharm, but hasn't been tested much beyond that.

---

## ✅ Features

- User registration & login (JWT-based)
- Password hashing (with bcrypt)
- Create / Edit / Delete gems and minerals
- Only item owners can edit/delete
- Jinja2 templates (dynamic views based on login)
- MySQL database

---

## 🧰 Tech Used

- Python 3.11+
- Flask
- MySQL
- SQLAlchemy ORM
- bcrypt for passwords
- JWT for authentication
- Jinja2 for frontend templating

---

## 🔧 How to Run

> Make sure you have Python and MySQL installed.

--- 

Create a .env file in the root folder with:
JWT_SECRET=your_jwt_secret

--- 

Create a MySQL database:
CREATE DATABASE online_store_python;

---

Run the project (from the root folder):
python -m src.main

---

Then open your browser and go to:
http://localhost:3000

---

📦 To-Do / Known Issues
- VS Code doesn't run the project properly yet
- Add more validations and error handling
- Add styling


