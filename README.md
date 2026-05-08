# 📲 WageWise Endline Survey Bot

> **A WhatsApp-based endline survey bot built with Flask and Twilio that collects survey responses from WageWise programme participants and automatically rewards them with mobile airtime upon completion.**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?logo=twilio&logoColor=white)](https://www.twilio.com/whatsapp)
[![Azure](https://img.shields.io/badge/Azure-Web_App-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![SQL Server](https://img.shields.io/badge/Azure_SQL-MSSQL-CC2927?logo=microsoftsqlserver&logoColor=white)](https://azure.microsoft.com/en-us/products/azure-sql/)
[![Africa's Talking](https://img.shields.io/badge/Africa's_Talking-Airtime-FF6B00)](https://africastalking.com/)
[![Deploy](https://github.com/abdullahek/wagewise-endline/actions/workflows/main_wagewise-endline.yml/badge.svg)](https://github.com/abdullahek/wagewise-endline/actions/workflows/main_wagewise-endline.yml)

---

## 🌟 Overview

**WageWise Endline** is a conversational survey bot that runs over WhatsApp using Twilio's Messaging API. It was built for the **WageWise** financial-literacy programme by Genesis Analytics to collect 3-year endline survey data from participants in South Africa.

The bot:
1. Receives an inbound WhatsApp message from a participant.
2. Verifies the user is registered in the `users_endline` table.
3. Walks them through a sequenced survey (single-select, multi-select, and free-text questions).
4. Logs every question sent and every answer received in an Azure SQL database.
5. On survey completion (~21 questions), automatically dispatches **R125 of mobile airtime** to the participant via the **Africa's Talking** Airtime API.
6. Marks the user as "completed" so they cannot retake the survey.

---

## ✨ Core Features

### 💬 WhatsApp Survey Flow
- Inbound message handling via Twilio webhook (`POST /message`)
- Registration check against the `users_endline` table — unregistered numbers receive a help message
- Re-entry guard: users whose surveys are marked complete receive *"Your survey has already been taken"*
- `Hi` / `STOP` / `End` keywords for start, opt-out, and reset

### 🧠 Dynamic Question Engine
- Questions stored in `endline_questions_list` (driven by SQL — no code changes to add/edit questions)
- Three question types supported:
  - **Single-select** — letter/number response validated against `Options_List`
  - **Multi-select** — accepts comma-, space-, dot-, or character-delimited answers; each option validated
  - **"Other allowed"** — special last option lets the user type a free-text answer
- Per-user question pointer so each participant resumes exactly where they left off
- Pending-question detection (re-prompt after 48 / 168 hours of inactivity)

### 🎁 Automated Airtime Reward
- On survey completion (`count >= 21`), sends **R125 ZAR** airtime via Africa's Talking
- Test/whitelist numbers receive a reduced **R10** payload (for QA participants)
- Bulk retrospective sender (`send_many_retrospective`) reads recipients from an Excel sheet for back-pay runs

### 🗄️ Robust Data Logging
Every interaction is captured across three tables:
- `endline_answers` — log of every question sent to each user (with `Response_Status` and `completed` flags)
- `endline_question_response` — log of every answer received
- `endline_questions_list` — master list of survey questions, options, multi-select / other-allowed flags

### ☁️ Production Deployment
- Deployed to **Azure App Service** via GitHub Actions (`.github/workflows/main_wagewise-endline.yml`)
- OIDC-based Azure login (no static credentials in repo)
- Runs under **Gunicorn** with a 600-second timeout for long survey transactions
- Auto-installs `unixodbc-dev` + `msodbcsql18` on container boot via `startup.sh`

---

## 🏗️ Architecture

```
                ┌────────────────────────┐
                │      Participant       │
                │   (WhatsApp on phone)  │
                └──────────┬─────────────┘
                           │ WhatsApp message
                           ▼
                ┌────────────────────────┐
                │        Twilio          │
                │  WhatsApp Business API │
                └──────────┬─────────────┘
                           │ HTTP POST /message
                           ▼
       ┌──────────────────────────────────────────┐
       │       Flask App (Azure Web App)          │
       │                                          │
       │   ┌──────────────────────────────────┐   │
       │   │  glogic/bot_view.py              │   │
       │   │  ─ Routes inbound messages       │   │
       │   │  ─ Orchestrates survey flow      │   │
       │   └─────┬─────────────────────┬──────┘   │
       │         │                     │          │
       │   ┌─────▼─────────┐   ┌───────▼───────┐  │
       │   │ Long_Question │   │ send_airtime  │  │
       │   │ _Common.py    │   │ .py           │  │
       │   │  (SQL engine) │   │ (rewards)     │  │
       │   └─────┬─────────┘   └───────┬───────┘  │
       └─────────┼─────────────────────┼──────────┘
                 │                     │
                 ▼                     ▼
       ┌──────────────────┐   ┌──────────────────┐
       │  Azure SQL DB    │   │ Africa's Talking │
       │  (MSSQL)         │   │  Airtime API     │
       │ ─ users_endline  │   │  (R125 ZAR)      │
       │ ─ endline_*      │   └──────────────────┘
       └──────────────────┘
```

---

## 📦 Project Structure

```
wagewise-endline/
├── .github/
│   └── workflows/
│       └── main_wagewise-endline.yml   # CI/CD → Azure Web App
├── glogic/                             # Flask application package
│   ├── __init__.py                     # App + DB factory (prepare_app)
│   ├── config.py                       # MSSQL & Test config classes
│   ├── models.py                       # SQLAlchemy ORM models
│   ├── views.py                        # Health-check root route
│   ├── bot_view.py                     # /message webhook — survey orchestrator
│   ├── Long_Question_Common.py         # Raw-SQL survey engine (pyodbc)
│   ├── gresponses.py                   # Static response dictionary (legacy G:Bot copy)
│   ├── WebScrape.py                    # Legacy web-scrape helpers (G:Bot)
│   └── send_airtime.py                 # Africa's Talking integration
├── migrations/                         # Alembic / Flask-Migrate migrations
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── manage.py                           # Flask-Script entrypoint (runserver, db)
├── startup.sh                          # Azure container start script (gunicorn)
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 🗃️ Database Schema

The bot uses **two layers** of tables:

### SQLAlchemy ORM models (`glogic/models.py`)
| Table | Purpose |
|-------|---------|
| `Data_for_G:Bot` | Generic message log (legacy) |
| `Question_List` | Master question definitions |
| `User_Question_Logs` | Tracks which questions were sent to which user |
| `User_Response_Logs` | Tracks user-submitted responses |

### Raw-SQL survey tables (`glogic/Long_Question_Common.py`)
| Table | Purpose |
|-------|---------|
| `users_endline` | Registered participants (`number`, `registered`) |
| `endline_questions_list` | Survey question bank — `number`, `question`, `options`, `Options_List`, `Is_MultiSelect`, `Allow_Other`, `status` |
| `endline_answers` | Per-user "questions sent" log — `User_Number`, `Q_Number`, `Response_Status`, `Sent_On`, `completed` |
| `endline_question_response` | Per-user answers — `User_Number`, `Q_Number`, `Response`, `Received_On`, `completed` |

> **Note:** The raw-SQL endline tables (`endline_*`) are the ones actually used by the survey runtime. The ORM models are inherited from the original G:Bot template.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10 |
| Web framework | Flask 2.3.2 |
| WSGI server | Gunicorn (production) / Flask dev server (local) |
| ORM / Migrations | SQLAlchemy 2.0 + Flask-Migrate (Alembic) |
| Raw SQL driver | pyodbc (ODBC Driver 17 for SQL Server) |
| Database | Azure SQL (MSSQL) |
| Messaging | Twilio WhatsApp Business API |
| Airtime rewards | Africa's Talking (Python SDK 1.2.5) |
| Data utilities | pandas 1.4.1, numpy 1.22.3, openpyxl |
| Web scraping (legacy) | requests + BeautifulSoup4 |
| Hosting | Azure App Service (Linux) |
| CI/CD | GitHub Actions → Azure deploy |

---

## 🛠️ Local Development

### Prerequisites
- Python **3.10**
- ODBC Driver 17 for SQL Server ([Microsoft download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))
- Access to an Azure SQL instance (or use the bundled `TestConfig` SQLite mode)
- A Twilio account with a WhatsApp sandbox number
- An Africa's Talking sandbox account (for airtime testing)
- `ngrok` (or any HTTPS tunnel) to expose your local server to Twilio

### 1. Clone & install

```bash
git clone https://github.com/abdullahek/wagewise-endline.git
cd wagewise-endline

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root (do **not** commit it):

```bash
SECRET_KEY=change-me
DEBUG=True

# Azure SQL connection (used by glogic/config.py)
SERVER=your-server.database.windows.net
DATABASE=your-db
NAME=your-username
PASSWORD=your-password

# Twilio (set these in your Twilio console — webhook URL only)
# TWILIO_ACCOUNT_SID=...
# TWILIO_AUTH_TOKEN=...

# Africa's Talking (currently hardcoded in send_airtime.py — see Tech Debt below)
# AT_USERNAME=...
# AT_API_KEY=...
```

Source it before running:

```bash
set -a; source .env; set +a
```

### 3. Run database migrations

```bash
python manage.py db upgrade
```

### 4. Start the bot

**Flask dev server:**
```bash
python manage.py runserver       # → http://localhost:5000
```

**Gunicorn (production-like):**
```bash
gunicorn --bind=0.0.0.0 --timeout 600 manage:app
```

### 5. Expose it to Twilio

```bash
ngrok http 5000
```

Copy the public HTTPS URL and configure your Twilio WhatsApp sandbox webhook to point to:

```
https://<your-ngrok-id>.ngrok.io/message
```

Send `Hi` from a registered WhatsApp number to start the survey.

---

## 🔄 Survey Flow

```
User sends "Hi" (registered number)
         │
         ▼
┌─────────────────────────────────────────┐
│  registered(num) → check users_endline  │
└──────────────────┬──────────────────────┘
                   │ if 1
                   ▼
┌─────────────────────────────────────────┐
│  check_survey_status(num)               │
│  if already completed → reject          │
└──────────────────┬──────────────────────┘
                   │ if 0
                   ▼
┌─────────────────────────────────────────┐
│  Send_Survey_Question(num, 'New')       │
│  → fetches next question from           │
│    endline_questions_list               │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  add_Question_Sent_Log → endline_answers│
│  Twilio replies with Question + Options │
└──────────────────┬──────────────────────┘
                   │ user replies
                   ▼
┌─────────────────────────────────────────┐
│  Validate_Options(Options, response)    │
│   ┌─ valid → add_User_response →        │
│   │   endline_question_response,        │
│   │   then Send next question           │
│   └─ invalid → "please try again"       │
└──────────────────┬──────────────────────┘
                   │ count >= 21
                   ▼
┌─────────────────────────────────────────┐
│  Vipe_clean_user_question_logs(num)     │
│  send_airtime_after_survey(num, R125)   │
│  Reply: "Thank you! R125 airtime is on  │
│          its way..."                    │
└─────────────────────────────────────────┘
```

---

## 🌐 API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` / `POST` | `/` | Health check — returns *"I'm working"* |
| `GET` / `POST` | `/message` | Twilio WhatsApp webhook (TwiML response) |

---

## 🚢 Deployment (Azure)

The `main` branch auto-deploys to the **`wagewise-endline`** Azure Web App on every push:

1. **GitHub Actions** (`.github/workflows/main_wagewise-endline.yml`)
   - Builds with Python 3.10
   - Installs dependencies
   - Zips the artifact
   - Deploys via OIDC to Azure App Service (Production slot)
2. **Container start** (`startup.sh`)
   - Installs `unixodbc-dev` + `msodbcsql18` (required by pyodbc)
   - Boots gunicorn with a 600s timeout
3. **Twilio** webhook should be set to: `https://wagewise-endline.azurewebsites.net/message`

### Required Azure / GitHub secrets

| Secret | Used by |
|--------|---------|
| `AZUREAPPSERVICE_CLIENTID_*` | GitHub Actions OIDC login |
| `AZUREAPPSERVICE_TENANTID_*` | GitHub Actions OIDC login |
| `AZUREAPPSERVICE_SUBSCRIPTIONID_*` | GitHub Actions OIDC login |
| `SERVER`, `DATABASE`, `NAME`, `PASSWORD` | App settings (Azure SQL) |
| `SECRET_KEY`, `DEBUG` | Flask config |

---

## 🔒 Security & Tech-Debt Notes

The repository inherits some patterns from its G:Bot template that should be hardened before further production use:

- 🔴 **Hardcoded SQL credentials** in `glogic/config.py` and `glogic/Long_Question_Common.py` — should be moved entirely to environment variables.
- 🔴 **Hardcoded Africa's Talking API key** in `glogic/send_airtime.py` — should be moved to env vars / Azure Key Vault.
- 🟠 **Raw f-string SQL** throughout `Long_Question_Common.py` — should be migrated to parameterised queries (currently relies on phone-number format being trusted).
- 🟠 **Twilio request signature** is not validated — anyone who knows the URL can POST to `/message`.
- 🟠 **Whitelisted test numbers** are hardcoded in `bot_view.py` — should be moved to a config table.

A future hardening pass should:
1. Centralise all secrets in Azure Key Vault.
2. Replace f-string SQL with parameterised queries (`cursor.execute(query, (user,))`).
3. Add Twilio request-signature validation middleware.
4. Drop the unused legacy G:Bot files (`gresponses.py`, `WebScrape.py`).

---

## 🧪 Useful Commands

```bash
# Run migrations
python manage.py db upgrade

# Create a new migration after model changes
python manage.py db migrate -m "describe change"

# Send airtime to a list of numbers from an Excel sheet
python -m glogic.send_airtime
```

---

## 📄 License

This project is private and proprietary to its owner. All rights reserved.

---

## 👤 Author / Maintainer

**Abdullah EK** — [@abdullahek](https://github.com/abdullahek)

> Originally based on the **G:Bot** template by Genesis Analytics, adapted for the **WageWise** programme endline survey.

---

<p align="center">
  Built with ❤️ for financial-literacy research at scale
</p>
