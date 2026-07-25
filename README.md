# money-tracker
 
A small self-hosted Flask app that reads my bank notifications and tells me how poor I am.
 
### How it works
 
1. **MacroDroid** on my phone reads incoming bank notifications and appends the transaction details to a text file.
2. That file gets synced to my server through **Nextcloud**.
3. The **Flask app** on the server reads the file, categorizes each transaction, and calculates spending, savings, and category breakdowns.
4. Results are shown on a simple web page — no manual data entry required.
```
Bank notification → MacroDroid → money.txt → Nextcloud sync → Flask app → totals
```
 
### Demo Installation
 
```bash
$ git clone <your-repo-url>
$ cd money_app
$ pip3 install flask
```
 
(Use `pip3 install flask --break-system-packages` or a virtualenv if your system blocks global installs.)
 
### Usage
 
```bash
$ python3 app.py
```
 
Then open `http://<server-ip>:8001` in a browser. Hit **Run** to process the latest data, or use **Choose** to pick a breakdown style:
 
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
 
### A word of caution
 
This reads real transaction data — names, merchants, amounts. If you ever push this to a public repo, make sure `money.txt` and `data_2.json` are gitignored. Don't commit real financial data.
