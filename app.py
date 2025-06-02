from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('fuel_log.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        date TEXT,
        odometer INTEGER,
        rate REAL,
        amount REAL,
        liters REAL
    )""")
    conn.commit()
    conn.close()

@app.route("/fuel-bot", methods=['POST'])
def fuel_bot():
    msg = request.form.get('Body').strip()
    user = request.form.get('From')
    resp = MessagingResponse()

    if msg.lower().startswith('add'):
        try:
            parts = msg.split()
            odometer = int(parts[1].replace('km', ''))
            rate = float(parts[2].replace('Rs', ''))
            amount = float(parts[3].replace('Rs', ''))
            liters = round(amount / rate, 2)

            conn = sqlite3.connect('fuel_log.db')
            c = conn.cursor()
            c.execute("INSERT INTO logs (user, date, odometer, rate, amount, liters) VALUES (?, ?, ?, ?, ?, ?)",
                      (user, datetime.now().strftime('%Y-%m-%d %H:%M'), odometer, rate, amount, liters))
            conn.commit()
            conn.close()

            resp.message(f"✅ Entry Logged:\nOdometer: {odometer} km\nRate: ₹{rate}/L\nAmount: ₹{amount}\nFuel: {liters} L")
        except:
            resp.message("❌ Use format: Add 45600km 98Rs 2000Rs")

    elif msg.lower() == 'view log':
        conn = sqlite3.connect('fuel_log.db')
        c = conn.cursor()
        c.execute("SELECT date, odometer, rate, amount, liters FROM logs WHERE user=? ORDER BY id DESC LIMIT 5", (user,))
        rows = c.fetchall()
        conn.close()
        if rows:
            text = "📘 Last 5 Fuel Entries:\n"
            for row in rows:
                text += f"{row[0]} | {row[1]}km | ₹{row[2]}/L | ₹{row[3]} | {row[4]}L\n"
            resp.message(text)
        else:
            resp.message("No logs found.")

    elif msg.lower() == 'summary':
        conn = sqlite3.connect('fuel_log.db')
        c = conn.cursor()
        c.execute("SELECT SUM(amount), SUM(liters) FROM logs WHERE user=?", (user,))
        total = c.fetchone()
        conn.close()
        resp.message(f"📊 Total:\nFuel: {round(total[1] or 0, 2)} L\nCost: ₹{round(total[0] or 0, 2)}")

    elif msg.lower() == 'help':
        resp.message("🛠️ Commands:\n- Add 45600km 98Rs 2000Rs\n- View log\n- Summary\n- Help")

    else:
        resp.message("🤖 Unknown command. Send 'Help' for options.")

    return str(resp)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
