# Personal-Finance-Tracker
 
A small self-hosted Flask app that categorizes my expenses month by month.
 
## How it works

- Parses a transaction history file and automatically categorizes expenses using keyword matching.
- Calculates monthly spending, income, savings, and vehicle-related expenses.
- Applies custom rules for recurring and shared expenses (e.g., Spotify family plan, Ryanair and Aeroitalia flight splitting).
- Generates monthly spending reports by category, with an optional transaction-level breakdown.
- Analyzes spending using budgeting metrics, including the 50/30/20 rule.
- Flags uncategorized transactions and allows new keywords to be easily added to the category database.

## Notes

1. **Why use a plain `.txt` file instead of a database?**  
   The project started as a small Python learning exercise. A text file was simple to work with and integrates well with my Bank Notification → MacroDroid → Python workflow.

2. **Why not migrate to a database?**  
   I may do so in the future, but the current approach is lightweight, easy to maintain, and fully meets my personal needs.

3. **Demo data**  
   All transactions included in the demo are fictional and were created solely for demonstration purposes.


### How the Pythone file works:
 
1. Why a simple .txt file instead of a proper database?
2. It started as Python practice and later became more seriues. Also, it makes the Bank notification → MacroDroid transition easier.
3. The transactions into the Demo are completelty made up.

 
### Demo Installation
 
```bash
$ git clone https://github.com/MattiaSanna/Personal-Finance-Tracker.git
$ cd Personal-Finance-Tracker
$ pip3 install flask
```
 
(Use `pip3 install flask --break-system-packages` or a virtualenv if your system blocks global installs.)
 
### Usage
 
```bash
$ python3 app.py
```
 
Then open `http://localhost:8001` in a browser. Hit **Run** to process the latest data, or use **Choose** to pick a breakdown style:
 
- **Normal** — total spent per category
- **Show more** — per-category totals plus a full line-item breakdown
- **50 30 20** — spending split into Essentials / Wants / Savings percentages
### Configuration
 
The app expects two files to exist on the server:
 
| File | Purpose |
|---|---|
| `categories.json` | Maps category names to the keywords/merchant tags used to match transactions |
| `transactions.txt` | The raw transaction log synced from Nextcloud (one line per notification) |
 
Paths to both are currently hardcoded in `money_logic.py` — update them if your setup differs.
 
### Project structure
 
```
money_app/
├── app.py             # Flask routes
├── tracker.py     # Parsing, categorization, and calculations
└── templates/
    └── index.html     # UI
```

