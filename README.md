# Q&A Platform Django Project

A fully-featured Q&A web platform inspired by Stack Overflow. Demonstrates advanced Django engineering: custom user models, group-based admin permissions, robust signals, extensible and modular architecture.

---

**Badges:**  
[![Django](https://img.shields.io/badge/Django-5.2.4-green)]() [![Python](https://img.shields.io/badge/Python-3.12-blue)]() [![license](https://img.shields.io/badge/license-MIT-informational)]()

---

## 📚 Table of Contents

- [Features](#-features)
- [Quickstart](#-quickstart)
- [Live Demo](#-live-demo)
- [Admin Permissions & Groups](#-admin-permissions--groups)
- [Testing](#-testing)
- [API Endpoints](#-api-endpoints)
- [Customization](#-customization)

---

## 🚀 Features

- **User System:** Register, login/logout, profile edit, avatar upload.
- **Q&A Module:** Ask, update, answer, comment (generic relations).
- **Tagging:** Add tags to questions.
- **Dynamic Permissions:**
    - **Super Admin:** Full permissions.
    - **Staff Moderator:** Add tags and badges. Limited edit permissions on all other models except users and groups. Users and groups are view only.
- **AJAX Username Check:** Real-time username availability check at registration and profile edit.
- **REST API Search Bar:** Search functionality based on question title/body and question tags.
- **Comprehensive Testing:** Models, forms, signals, permissions, admin workflows.

---

## ⚡ Quickstart

1. Clone the repository
   git clone <repo_url>
   cd <project_folder>

2. Create and activate a virtualenv
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install requirements
   pip install -r requirements.txt

4. Migrate
   python manage.py migrate

5. Create a superuser
   python manage.py createsuperuser

6. Run the server
   python manage.py runserver
    
   
Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


---

## 🌍 Live Demo

[Visit yourqa.azurewebsites.net](https://yourqa.azurewebsites.net)

---

## 🔑 Admin Permissions & Groups

| Role            | Create  |  Edit   | Delete  | Restrictions                                                                                                                     |
|-----------------|:-------:|:-------:|:-------:|----------------------------------------------------------------------------------------------------------------------------------|
| **Super Admin** |    ✅    |    ✅    |    ✅    | Full access                                                                                                                      |
| **Staff Mod**   | Limited | Limited | Limited | Can add tags and badges.<br>Limited edit permissions on all other models except users and groups.<br>Users and groups are view only. |

- Admin logic is in `admin.py` for each app.
- Signals auto-create groups/permissions during setup.
- Admin default credentials: username - `admin`, password - `admin`.

---

## 🧪 Testing

To run all tests:

python manage.py test

Covers: model integrity, form validation, admin permissions, AJAX, and signals.

---

## 🌐 API Endpoints

### Username Check

- **GET** `/check-username/?username=chosenname` when registering
- **GET** `/check-username/?username=chosenname&current_username=request.user.username` when updating profile
- Response:
  {"available": true/false, "is_current": true/false, "message": "message for additional context"}

### General CRUD

Standard Django CRUD for questions, answers, comments, users, and profiles.

---

## 🎨 Customization

- Modular/extensible: add features or override logic.
- Group and permission logic is signal-driven and easily extended.
