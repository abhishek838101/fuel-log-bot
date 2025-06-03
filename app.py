import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# === REPLACE THESE VALUES ===
ACCESS_TOKEN = "EAARZC01fOq1EBOZCZB4sgqSrtbXNYNezpnrEzgL4HTOWPLrdrNM4wNHWDbqoDMilyZCiYW7nP5kdLN0ZAnoSyay7y3yhrRm8RsZCn7xeZBhbXwZCaHrJ2x2fWCmnDxAs3Ur5AFy5YyAEWL0d24af5csD0U0XjP0ZCjG9L96WINv9FIStW1XMuYs5IBttvjsisRFMst8mGDpSwKquOZAgvm7WbBzdNjkXftxUNs"
PHONE_NUMBER_ID = "632074519997733"
RECIPIENT_PHONE = "+15556507312"  # Your test WhatsApp number

# === Send message to WhatsApp user ===
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

# === API endpoint to receive fuel log ===
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
