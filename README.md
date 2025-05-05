# Z-POS: Local Development Guide

Z-POS is a web-based Point of Sale (POS) system tailored for small businesses. This document explains how to set up and run the project locally on a Windows machine.

## 🛠️ Technology Stack

- **Frontend**: Vue.js (via Vue CLI)
- **Backend**: Django + Django REST Framework
- **Database**: MySQL

---

## ⚙️ Prerequisites
Ensure the following are installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js (v16+)](https://nodejs.org/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [npm or yarn](https://www.npmjs.com/)

---


## Backend Setup (USING COMMAND PROMPT) (Django)

1. **Navigate to backend folder:**
   ```bash
   cd Z-Pos-main/Z-Pos/pos_backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start development server:**
   ```bash
   python manage.py runserver
   ```

---

## Frontend Setup (OPEN ANOTHER COMMAND PROMPT) (Vue.js)

1. **Navigate to frontend folder:**
   ```bash
   cd Z-Pos-main/Z-Pos/pos_backend/z-pos-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run Vue dev server:**
   ```bash
   npm run serve
   ```
3. **Click on this link as shown in CMD:**
   ```bash
   Network: http://192.168.0.91:8080/
   ```

4. **Login as:**
```text
Admin:
  username: admin
  password: Zohaib2004

Cashier:
  username: cashier_bob
  password: 123
```
