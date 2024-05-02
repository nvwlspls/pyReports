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

    group_summary_df = march2024.groupby('parent category')['amount'].agg(['sum', 'mean', 'count']).reset_index()
    category_summary_df = march2024.groupby('category')['amount'].agg(['sum', 'mean','count']).reset_index()
    parent_catergory_links = {}

    for group in group_summary_df['parent category']:
            parent_catergory_links[group] = march2024.loc[march2024['parent category'] == group, ['category']]['category'].unique()

    context = {
        "title": "This is the title",
        "content": "This is the content",
        "group_summary": group_summary_df.to_dict('records'),
        "category_summary": category_summary_df.to_dict('records'),
        "parent_category_links": parent_catergory_links
    }
    return render_template('report.html', **context)
