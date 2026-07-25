from flask import Flask, render_template, request
import io
from contextlib import redirect_stdout

from tracker import run_tracker

app = Flask(__name__)

@app.route('/')
def index():
    # show empty output initially
    return render_template('index.html', output="")

@app.route('/run', methods=['POST'])
def run():
    # Get the value from the hidden input
    selected_choice = request.form.get('user_option', 'Default')
    
    # Capture printed output from run_tracker
    buf = io.StringIO()
    with redirect_stdout(buf):
        # call the function that uses print()
        run_tracker(selected_choice)
    printed_output = buf.getvalue()
    
    # Render the same HTML but inject the captured printed output
    return render_template('index.html', output=printed_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
