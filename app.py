from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)

@app.route("/")
def render_report():
    df = pd.read_csv('/Users/wjessen/Documents/transactions.csv')

    # if the category is nan it is uncategorized
    df.loc[df['category'].isna(), "category" ] = "uncategorized"

    df["parent category"] = df["parent category"].combine_first(df["category"])

    # make the date column a date
    df['date'] = pd.to_datetime(df['date'])

    # keep only march 2024 transactions for now
    march2024 = df[(df['date'].dt.month == 4) & (df['date'].dt.year == 2024)]

    summary_df = df.groupby('category')['amount'].agg(['sum', 'mean', 'count']).reset_index()
    print(summary_df.head())
    context = {
        "title": "This is the title",
        "content": "This is the content",
        "month": march2024.to_dict('records')
    }
    return render_template('report.html', **context)
