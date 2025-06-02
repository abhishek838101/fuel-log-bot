# 🚗 WhatsApp Fuel Log Bot

A simple fuel log chatbot for WhatsApp using Flask, SQLite, and Twilio.

## 📦 Features
- Log fuel entry with odometer, rate, and amount
- View last 5 entries
- Get total fuel and cost summary

## 📲 Message Format (via WhatsApp)
```
Add 45600km 98Rs 2000Rs
View log
Summary
Help
```

## 🚀 Deploy to Render

1. Fork or clone this repo
2. Push to your own GitHub
3. Go to https://render.com > New Web Service
4. Connect your repo
5. Set:
   - Environment: Python
   - Start command: `python app.py`

6. Set Twilio webhook to:
   ```
   https://your-render-url.onrender.com/fuel-bot
   ```

## 🧪 Test it
Send WhatsApp message to your Twilio sandbox number using the above formats.
