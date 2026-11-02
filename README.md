# 🛠 Installation

### 1. Clone the repository
```bash
cd your-repo-name
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```
### 1. Run the development server
```bash
python manage.py runserver
```
#### Then open your browser and go to:
```bash
http://127.0.0.1:8000/api/v1/swagger/
```
























<<<<<<< HEAD
=======

# برای نصب روی لینکوس سرور میخوایم


# آپدیت pip
python -m pip install --upgrade pip

# نصب پکیج‌ها
pip install -r requirements.txt

# یا نصب یک‌به‌یک
pip install Django==5.2.7
pip install djangorestframework==3.16.1
>>>>>>> develop
pip install djangorestframework-simplejwt==5.5.1
pip install drf-yasg==1.21.11
pip install django-environ==0.12.0
pip install requests==2.32.5
pip install django-ratelimit==4.1.0
pip install django-cors-headers==4.6.0
<<<<<<< HEAD
pip install psycopg2-binary==2.9.11# api_nowaitapp
=======
pip install psycopg2-binary==2.9.11
>>>>>>> develop
# nowaitapp.it_backend
