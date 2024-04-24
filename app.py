from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def render_report():
    # Open file

    # get the data into a dataframe

    # organzie the dataframe


    context = {
        "title": "This is the title",
        "content": "This is the content"
    }
    return render_template('report.html', **context)
