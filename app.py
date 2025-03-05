from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database Setup
def create_database():
    conn = sqlite3.connect("transfusion_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transfusion_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mrn TEXT,
            date TEXT,
            starting_hct REAL,
            ending_hct REAL,
            desired_increase_hct REAL,
            transfusion_coefficient REAL,
            weight REAL,
            volume_to_transfuse REAL
        )
    """)
    conn.commit()
    conn.close()

create_database()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        mrn = request.form["mrn"]
        starting_hct = float(request.form["starting_hct"])
        ending_hct = float(request.form["ending_hct"])
        weight = float(request.form["weight"])

        desired_increase_hct = ending_hct - starting_hct
        transfusion_coefficient = 0.02 if desired_increase_hct < 11 else \
                                  0.03 if desired_increase_hct < 16 else \
                                  0.04 if desired_increase_hct < 21 else \
                                  0.05 if desired_increase_hct < 26 else \
                                  0.06 if desired_increase_hct < 31 else \
                                  0.07 if desired_increase_hct < 36 else \
                                  0.08

        volume_to_transfuse = transfusion_coefficient * weight

        # Save Data
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("transfusion_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transfusion_records (mrn, date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (mrn, date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse))
        conn.commit()
        conn.close()

        result = {
            "desired_increase_hct": desired_increase_hct,
            "transfusion_coefficient": transfusion_coefficient,
            "volume_to_transfuse": volume_to_transfuse
        }

    return render_template("index.html", result=result)

@app.route("/records")
def view_records():
    conn = sqlite3.connect("transfusion_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, mrn, date, starting_hct, ending_hct, desired_increase_hct, transfusion_coefficient, weight, volume_to_transfuse FROM transfusion_records ORDER BY date DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("records.html", records=records)

@app.route("/delete/<int:record_id>")
def delete_record(record_id):
    conn = sqlite3.connect("transfusion_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transfusion_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_records"))

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
