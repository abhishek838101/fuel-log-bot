import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# === Replace these values ===
ACCESS_TOKEN = "EAARZC01fOq1EBO09ZCgz879brMhKN7pkmJF59PAmTJHZCHEoZBc28v9Ri0ybFlQXM1vcyTcs0dti9F42voPqwSMMPxIx0Ps5qwXQKmM7fokQk4OjiOZCmVZAbJS3EznUAtDbUXcEshT41I6HYDT0DwLJPBOmZCDZCB2vtFkhsQ97T46ONnq2ktXGdunC8brQCycyZAt0cJh128O94XM4B1oVXelQYbw1T9cMZD"
PHONE_NUMBER_ID = "632074519997733"
RECIPIENT_PHONE = "+15556507312"  # Your test WhatsApp number
VERIFY_TOKEN = "fuelbot123"  # Must match the token you use in Meta dashboard

# === WhatsApp Send Message Function ===
def send_whatsapp_message(message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "text",
        "text": {"body": message}
    }
    res = requests.post(url, headers=headers, json=data)
    print("WhatsApp API Response:", res.status_code, res.text)

# === Webhook Verification Endpoint (GET) ===
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return "Verification failed", 403

# === Fuel Log Entry (POST) ===
@app.route("/fuel-log", methods=["POST"])
def fuel_log():
    data = request.json
    odometer = data.get("odometer")
    rate = data.get("rate")
    amount = data.get("amount")

    if not all([odometer, rate, amount]):
        return jsonify({"error": "Missing data"}), 400

    msg = (
        f"🚗 Fuel Log Entry\n"
        f"Odometer: {odometer} km\n"
        f"Rate: ₹{rate}/L\n"
        f"Amount: ₹{amount}"
    )

    send_whatsapp_message(msg)
    return jsonify({"status": "message sent"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
