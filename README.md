# Banking Management System (Flask + PostgreSQL)

A web-based banking management system built using Flask and PostgreSQL.  
The application supports user and employee authentication, balance enquiry, and secure fund transfers.

---

## 🚀 Features

- User login and dashboard
- Balance enquiry
- Fund transfer between accounts
- Employee login with administrative privileges
- Session-based authentication
- PostgreSQL database integration

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **Database:** PostgreSQL  
- **Frontend:** HTML (Jinja templates)  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/banking-management-system.git
cd banking-management-system
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure database
Ensure PostgreSQL is running and the required tables exist.

The application reads database credentials using environment variables inside the code.
Update them according to your local PostgreSQL setup.

5️⃣ Run the application
bash
Copy code
python app.py
6️⃣ Open in browser
cpp
Copy code
http://127.0.0.1:5000
