from flask import Flask, request
import json
import os

app = Flask(__name__)

VERIFY_TOKEN = "+917409012617"  # must match the one you enter on Meta

LOG_FILE = "logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

user_logs = load_logs()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    data = request.get_json()
    if data and data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value")
                if "messages" in value:
                    message = value["messages"][0]
                    sender = message["from"]
                    msg_text = message.get("text", {}).get("body", "").strip()

                    reply = handle_user_message(sender, msg_text)
                    send_whatsapp_message(sender, reply)

    return "ok", 200

def handle_user_message(sender, msg):
    global user_logs
    logs = user_logs.setdefault(sender, [])

    if msg.lower().startswith("add"):
        try:
            _, odo, rate, amt = msg.split()
            odo = int(odo.replace("km", ""))
            rate = float(rate.replace("Rs", ""))
            amt = float(amt.replace("Rs", ""))
            logs.append({"odometer": odo, "rate": rate, "amount": amt})
            save_logs(user_logs)
            return "✅ Entry added!"
        except:
            return "❌ Use format: Add 45600km 98Rs 2000Rs"
    elif msg.lower() == "view log":
        if not logs:
            return "📝 No entries yet."
        return "\n".join(
            f"{i+1}. {e['odometer']}km, {e['rate']}Rs/L, {e['amount']}Rs"
            for i, e in enumerate(logs)
        )
    elif msg.lower() == "summary":
        total_amt = sum(e["amount"] for e in logs)
        total_litres = sum(e["amount"]/e["rate"] for e in logs)
        return f"📊 Total: ₹{total_amt}, ⛽ Fuel: {total_litres:.2f}L"
    else:
        return "🤖 Commands:\nAdd 45600km 98Rs 2000Rs\nView log\nSummary"

def send_whatsapp_message(to, message):
    import requests

    url = "https://graph.facebook.com/v19.0/632074519997733/messages"
    headers = {
        "Authorization": "Bearer EAARZC01fOq1EBO12srl4eSZBMvZAKb9HUFFQHmZAMZChiRgIV3qgNbAfZAUjp0akNO2W7pCN2DJ7y5A6GqjmCqNo2gTsD7bN4gZAKeHVGpQYzRMAp2n9amI8RZC6ZBoYvoZAK4B9MRlCbTqDg6J5qtNEGas9TZBreYAWkfgCDypf3IkieK6vZCfe1iQ1kj0zZA8BMaUOxes4AvL4jSXhZAmbebKsO60zKMZAB3ZCTvgZD",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)

if __name__ == "__main__":
    app.run(debug=True)
