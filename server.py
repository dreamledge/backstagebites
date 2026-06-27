import base64
import io
import json
import re
import wave
from flask import Flask, request, jsonify
from flask_cors import CORS
import piper

app = Flask(__name__)
CORS(app)

voice = piper.PiperVoice.load(
    'voices/en_US-joe-medium.onnx',
    config_path='voices/en_US-joe-medium.onnx.json'
)

faq = [
    {
        'keywords': ['hours', 'open', 'time', 'when', 'close', '24'],
        'answer': 'Backstage Bites is open right now. We operate daily for delivery through our partner apps — Deliveroo, Talabat, and Careem Food. Check your app for exact hours in your area.'
    },
    {
        'keywords': ['menu', 'food', 'serve', 'sell', 'item', 'pizza', 'wing', 'side', 'what'],
        'answer': 'Our set list features real pizza, big wings, and loaded sides. It\'s inspired by New York and Philadelphia street food, all halal. Check out the full menu under the Menu section on our site.'
    },
    {
        'keywords': ['halal', 'halaal'],
        'answer': 'Yes — everything at Backstage Bites is 100% halal. From our pizza to our wings and loaded sides, we use only halal-certified ingredients.'
    },
    {
        'keywords': ['order', 'delivery', 'deliveroo', 'talabat', 'careem', 'buy', 'get'],
        'answer': 'You can order right now on Deliveroo, Talabat, and Careem Food. We have two kitchens — one in Arjan and one in JBR / Marina. Hit the Order section on our site for direct links.'
    },
    {
        'keywords': ['location', 'where', 'kitchen', 'area', 'dubai', 'arjan', 'jbr', 'marina'],
        'answer': 'We\'re a delivery-only brand based in Dubai. Our kitchens are in Arjan and JBR / Marina, covering areas like Barsha, Downtown, Dubai Marina, JLT, Palm Jumeirah, and Sheikh Zayed Road.'
    },
    {
        'keywords': ['backstage list', 'waitlist', 'join', 'sign up', 'signup', 'exclusive', 'offer', 'discount', 'deal', 'promo'],
        'answer': 'Join the Backstage List to get exclusive offers, secret menu access, and first-order discounts before anyone else. You can sign up right on our homepage with your name, WhatsApp, email, and area.'
    },
    {
        'keywords': ['story', 'backstory', 'concept', 'about', 'who', 'start', 'begin'],
        'answer': 'Backstage Bites was born from the streets of Philadelphia and New York, mixed with music and culture. We\'re a delivery-only brand built for late studio sessions, movie nights, game days, and after-hours hunger. Every plate tells a story.'
    },
    {
        'keywords': ['instagram', 'social', 'media', 'follow', 'gallery', 'photo', 'picture'],
        'answer': 'Follow us on Instagram at @backstagebites.ae for the latest photos, updates, and behind-the-scenes content. You can also check out our Gallery page for our Instagram feed.'
    },
    {
        'keywords': ['contact', 'email', 'reach', 'call', 'phone', 'support'],
        'answer': 'You can reach us at info@backstagebites.ae. Follow us on Instagram @backstagebites.ae for the quickest updates.'
    },
    {
        'keywords': ['cost', 'price', 'pricing', 'expensive', 'afford', 'cost', 'fee', 'charge', 'dirham', 'aed'],
        'answer': 'Our pricing is competitive for premium halal pizza, wings, and loaded sides in Dubai. For exact prices, check the current menu on Deliveroo, Talabat, or Careem Food in your area.'
    },
    {
        'keywords': ['name', 'why backstage', 'backstage bites meaning', 'brand name'],
        'answer': 'The name Backstage Bites reflects our roots in music and culture. We\'re the food that happens behind the scenes — backstage, where the real flavor comes together before the main event.'
    },
    {
        'keywords': ['hello', 'hi', 'hey', 'help', 'assist', 'support'],
        'answer': 'Hey there! Welcome to Backstage Bites. I\'m the Backstage Bot. You can ask me about our menu, locations, ordering, hours, or anything else about the brand. What can I help you with?'
    },
]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    user_text = data.get('text', '').strip().lower()

    if not user_text:
        return jsonify({'reply': "I didn't catch that. Could you try again?", 'audio': ''})

    best = None
    best_score = 0
    for entry in faq:
        score = sum(1 for kw in entry['keywords'] if kw in user_text)
        if score > best_score:
            best_score = score
            best = entry['answer']

    reply = best or "I'm not sure about that, but you can check our website or ask me about the menu, ordering, hours, locations, or our story. What would you like to know?"

    audio_buf = io.BytesIO()
    with wave.open(audio_buf, 'wb') as wav:
        voice.synthesize_wav(reply, wav)
    audio_b64 = base64.b64encode(audio_buf.getvalue()).decode()

    return jsonify({'reply': reply, 'audio': audio_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
