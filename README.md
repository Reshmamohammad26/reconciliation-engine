# Cross-System Reconciliation

A full-stack reconciliation system for identifying discrepancies between System A and System B while keeping organization data isolated.

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite

### Frontend
- React
- Vite
- JavaScript
- CSS

## Project Structure

```text
reconciliation-engine/
│
├── backend/
│   ├── core/
│   ├── reconciler/
│   ├── manage.py
│   └── db.sqlite3
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── data/
│   ├── system_a.csv
│   ├── system_b.csv
│   └── locations.csv
│
├── README.md
└── DECISIONS.md