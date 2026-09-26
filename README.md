# Personal-Finance-Tracker
 
A small self-hosted Flask app that categorizes my expenses month by month.
 
## What it does

- Parses a transaction history file and automatically categorizes expenses using keyword matching.
- Calculates monthly spending, income, savings, and vehicle-related expenses.
- Applies custom rules for recurring and shared expenses (e.g., Spotify family plan, Ryanair and Aeroitalia flight splitting).
- Generates monthly spending reports by category, with an optional transaction-level breakdown.
- Analyzes spending using budgeting metrics, including the 50/30/20 rule.
- Flags uncategorized transactions and allows new keywords to be easily added to the category database.

## Notes

1. **The following script is just a demo**  
   This demo is only intended to showcase the functionality; the script I currently use on my server includes a few differences on the strcuture, but the main tracker.py logic is the same.

2. **Why use a plain `.txt` file instead of a database?**  
   The project started as a small Python exercise. A text file was simple to work with and integrates well with my Bank Notification → MacroDroid → Python workflow.

3. **Why not migrate to a database?**  
   I may do so in the future, but the current approach is lightweight, easy to maintain, and fully meets my personal needs.

4. **Demo data**  
   All transactions included in the demo are fictional and were created solely for demonstration purposes.


 
### Demo Installation

### Windows (PowerShell)

Install Git and Python (skip if already installed):

```powershell
winget install --id Git.Git
winget install --id Python.Python.3.13
```

Close and reopen PowerShell

Clone and set up the project:

```powershell
cd ~
git clone https://github.com/MattiaSanna/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
python -m pip install flask
```

Run the app:

```powershell
python app.py
```

---

### Linux (Debian/Ubuntu)

Install Git and Python/pip (skip if already installed):

```bash
sudo apt update
sudo apt install -y git python3 python3-pip
```

Clone and set up the project:

```bash
cd ~
git clone https://github.com/MattiaSanna/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
pip3 install flask
```

> If your system blocks global pip installs, use:
> `pip3 install flask --break-system-packages`
> or set up a virtual environment:
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install flask
> ```

Run the app:

```bash
python3 app.py
```
 
Then open `http://127.0.0.1:8001` in a browser. Hit **Run** to process the latest data, or use **Choose** to pick a breakdown style:
 
- **Normal** — total spent per category
- **Show more** — per-category totals plus a full line-item breakdown
- **Stats** — spending split into Essentials / Wants / Savings percentages
### Configuration
 
The app expects two files to exist on the server:
 
| File | Purpose |
|---|---|
| `categories.json` | Maps category names to the keywords/merchant tags used to match transactions |
| `transactions.txt` | The raw transaction log synced from Nextcloud (one line per notification) |
 
 
### Project structure
 
```
money_app/
├── app.py             # Flask routes
├── tracker.py         # Parsing, categorization, and calculations
└── templates/
    └── index.html     # UI
```

