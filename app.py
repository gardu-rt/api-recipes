from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

DATA_DIR = "data"

def load_all_recipes():
    all_data = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            filepath = os.path.join(DATA_DIR, file)
            try:
                df = pd.read_csv(filepath)
                df = df.rename(columns={
                    "Title": "title",
                    "Ingredients": "ingredients",
                    "Steps": "steps",
                    "Loves": "likes",
                    "URL": "url"
                })
                df["category"] = file.replace("dataset-", "").replace(".csv", "")
                all_data.append(df)
            except Exception as e:
                print(f"Failed to read {file}: {e}")
    return pd.concat(all_data, ignore_index=True).fillna("")

RECIPES_DF = load_all_recipes()


@app.route("/")
def home():
    return {"message": "Welcome to the Indonesian Recipe API"}

@app.route("/recipes")
def get_all_recipes():
    return jsonify(RECIPES_DF.to_dict(orient="records"))

@app.route("/recipes/<title>")
def search_by_title(title):
    result = RECIPES_DF[RECIPES_DF["title"].str.contains(title, case=False, na=False)]
    return jsonify(result.to_dict(orient="records"))

@app.route("/category/<name>")
def search_by_category(name):
    result = RECIPES_DF[RECIPES_DF["category"] == name]
    return jsonify(result.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
