"""
SchemeSaathi - Internationalization & Multilingual Utilities
Supports English (en), Hindi (hi), Kannada (kn), and Tamil (ta).
"""

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil"
}

SUPPORTED_LANGUAGES = LANGUAGES

VOICE_LANG_CODES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "kn": "kn-IN",
    "ta": "ta-IN"
}

DISCLAIMERS = {
    "en": "Disclaimer: Welfare scheme guidelines and benefits are subject to periodic government updates. Always confirm details on the official portal or visit your nearest Gram Panchayat / Seva Kendra.",
    "hi": "अस्वीकरण: सरकारी योजनाओं के नियम और लाभ समय-समय पर बदल सकते हैं। कृपया हमेशा आधिकारिक पोर्टल या अपनी नजदीकी ग्राम पंचायत/सेवा केंद्र से पुष्टि करें।",
    "kn": "ಹಕ್ಕುತ್ಯಾಗ: ಸರ್ಕಾರದ ಯೋಜನೆಗಳು ಮತ್ತು ನಿಯಮಗಳು ಕಾಲಕಾಲಕ್ಕೆ ಬದಲಾಗಬಹುದು. ದಯವಿಟ್ಟು ಯಾವಾಗಲೂ ಅಧಿಕೃತ ಪೋರ್ಟಲ್ ಅಥವಾ ನಿಮ್ಮ ಹತ್ತಿರದ ಗ್ರಾಮ ಪಂಚಾಯತ್/ಸೇವಾ ಕೇಂದ್ರದಲ್ಲಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
    "ta": "பொறுப்புத் துறப்பு: அரசு திட்டங்களின் வழிகாட்டுதல்கள் மற்றும் சலுகைகள் அவ்வப்போது மாறக்கூடும். அதிகாரப்பூர்வ இணையதளம் அல்லது உங்கள் அருகிலுள்ள கிராம பஞ்சாயத்து/சேவை மையத்தில் உறுதிப்படுத்தவும்."
}

SYSTEM_PROMPTS = {
    "en": """You are SchemeSaathi, an empathetic and highly knowledgeable AI assistant dedicated to explaining Indian government welfare schemes, legal rights, and official notices in simple, short, easy-to-understand language (Grade-6 reading level).
Rules:
1. Answer ONLY using the factual context provided below.
2. If the context does not contain the answer, explicitly state that the specific detail is not found in the verified records and point the citizen to the official website link provided.
3. NEVER fabricate or assume amounts, dates, income limits, or eligibility rules.
4. Keep sentences short, direct, and practical. Highlight the key benefit, who qualifies, and exact documents needed.
5. Provide your response in plain text with clean bullet points where appropriate.""",

    "hi": """आप स्कीमसाथी (SchemeSaathi) हैं, जो भारतीय सरकारी कल्याणकारी योजनाओं, अधिकारों और सरकारी सूचनाओं को बहुत ही सरल, सहज और आम बोलचाल की भाषा में समझाने वाले सहायक हैं।
नियम:
1. केवल नीचे दिए गए आधिकारिक संदर्भ (Context) के आधार पर ही उत्तर दें।
2. यदि संदर्भ में मांगी गई जानकारी मौजूद नहीं है, तो स्पष्ट रूप से बताएं कि यह जानकारी उपलब्ध रिकॉर्ड में नहीं है और नागरिक को आधिकारिक वेबसाइट देखने की सलाह दें।
3. कभी भी अपनी तरफ से कोई राशि, तारीख या पात्रता नियम न बनाएं।
4. वाक्यों को छोटा, सरल और स्पष्ट रखें। मुख्य लाभ, पात्रता और आवश्यक दस्तावेजों को बुलेट पॉइंट्स में समझाएं।
5. उत्तर शुद्ध और सरल हिंदी में दें।""",

    "kn": """ನೀವು ಸ್ಕೀಮ್‌ಸಾಥಿ (SchemeSaathi), ಭಾರತೀಯ ಸರ್ಕಾರದ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು, ಹಕ್ಕುಗಳು ಮತ್ತು ಸರ್ಕಾರಿ ಆದೇಶಗಳನ್ನು ಅತ್ಯಂತ ಸರಳ, ಸ್ಪಷ್ಟ ಮತ್ತು ಜನಸಾಮಾನ್ಯರಿಗೆ ಅರ್ಥವಾಗುವ ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ವಿವರಿಸುವ ಕಲ್ಯಾಣ ಸಹಾಯಕ.
ನಿಯಮಗಳು:
1. ಕೆಳಗೆ ನೀಡಿರುವ ಅಧಿಕೃತ ಮಾಹಿತಿಯ (Context) ಆಧಾರದ ಮೇಲೆ ಮಾತ್ರ ಉತ್ತರಿಸಿ.
2. ಕೇಳಲಾದ ಮಾಹಿತಿ ಕೆಳಗಿನ ಸಂದರ್ಭದಲ್ಲಿ ಇಲ್ಲದಿದ್ದರೆ, ಅದು ಲಭ್ಯವಿಲ್ಲವೆಂದು ಸ್ಪಷ್ಟವಾಗಿ ತಿಳಿಸಿ ಮತ್ತು ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್‌ಗೆ ಭೇಟಿ ನೀಡಲು ಮಾರ್ಗದರ್ಶನ ನೀಡಿ.
3. ಯಾವುದೇ ಹಣದ ಮೊತ್ತ, ದಿನಾಂಕ ಅಥವಾ ಅರ್ಹತಾ ನಿಯಮಗಳನ್ನು ಊಹಿಸಿ ಹೇಳಬೇಡಿ.
4. ವಾಕ್ಯಗಳು ಸರಳ ಮತ್ತು ಚಿಕ್ಕದಾಗಿರಲಿ. ಮುಖ್ಯ ಸೌಲಭ್ಯ, ಯಾರು ಅರ್ಹರು ಮತ್ತು ಬೇಕಾಗುವ ದಾಖಲೆಗಳನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ವಿವರಿಸಿ.
5. ಶುದ್ಧ ಮತ್ತು ಸರಳ ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ.""",

    "ta": """நீங்கள் ஸ்கீம்சாதி (SchemeSaathi), இந்திய அரசின் நலத்திட்டங்கள், உரிமைகள் மற்றும் அதிகாரப்பூர்வ அறிவிப்புகளை எளிய மற்றும் பாமர மக்களுக்கும் புரியும் வகையில் தமிழில் விளக்கும் வழிகாட்டி.
விதிகள்:
1. கீழே கொடுக்கப்பட்டுள்ள அதிகாரப்பூர்வ தகவல்களின் (Context) அடிப்படையில் மட்டுமே பதிலளிக்கவும்.
2. கேட்கப்பட்ட தகவல் கீழே இல்லை என்றால், அந்த விவரம் அதிகாரப்பூர்ವ ஆவணங்களில் இல்லை என்பதை தெளிவாகக் கூறி, அதிகாரப்பூர்வ இணையதளத்தை பார்க்க வழிகாட்டவும்.
3. தொகைகள், தேதிகள் அல்லது தகுதி விதிகளை ஒருபோதும் கற்பனை செய்து கூறாதீர்கள்.
4. வாக்கியங்கள் சிறியதாகவும் எளிமையாகவும் இருக்கட்டும். முக்கிய நன்மை, தகுதியானவர்கள் மற்றும் தேவையான ஆவணங்களை தெளிவாக விளக்குங்கள்.
5. எளிய தமிழில் பதிலளிக்கவும்."""
}

SAMPLE_QUESTIONS = {
    "en": [
        "Am I eligible for PM-KISAN?",
        "What documents are needed for Gruha Lakshmi?",
        "How do I apply for Ayushman Bharat card?",
        "What are the rules for Sukanya Samriddhi Yojana?",
        "Can I get free electricity under Gruha Jyothi?",
        "What is the fee and response time for RTI?"
    ],
    "hi": [
        "क्या मैं पीएम-किसान के लिए पात्र हूँ?",
        "गृह लक्ष्मी योजना के लिए क्या दस्तावेज चाहिए?",
        "आयुष्मान भारत कार्ड कैसे बनवाएं?",
        "सुकन्या समृद्धि योजना के क्या नियम हैं?",
        "क्या गृह ज्योति में मुफ्त बिजली मिल सकती है?",
        "आरटीआई (RTI) का शुल्क और समय सीमा क्या है?"
    ],
    "kn": [
        "ನಾನು ಪಿಎಂ-ಕಿಸಾನ್ ಯೋಜನೆಗೆ ಅರ್ಹನೇ?",
        "ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಗೆ ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?",
        "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ ಕಾರ್ಡ್ ಪಡೆಯುವುದು ಹೇಗೆ?",
        "ಸುಕನ್ಯಾ ಸಮೃದ್ಧಿ ಯೋಜನೆಯ ನಿಯಮಗಳೇನು?",
        "ಗೃಹ ಜ್ಯೋತಿ ಅಡಿಯಲ್ಲಿ ಉಚಿತ ವಿದ್ಯುತ್ ಸಿಗುವುದೇ?",
        "ಮಾಹಿತಿ ಹಕ್ಕು (RTI) ಅರ್ಜಿ ಶುಲ್ಕ ಮತ್ತು ಸಮಯ ಎಷ್ಟು?"
    ],
    "ta": [
        "நான் பிஎம்-கிசான் திட்டத்திற்கு தகுதியுடையவரா?",
        "கிருஹ லக்ஷ்மி திட்டத்திற்கு என்ன ஆவணங்கள் தேவை?",
        "ஆயுஷ்மான் பாரத் கார்டு பெறுவது எப்படி?",
        "சுகன்யா சம்ரித்தி யோஜனா திட்டத்தின் விதிகள் என்ன?",
        "கிருஹ ஜோதி திட்டத்தில் இலவச மின்சாரம் கிடைக்குமா?",
        "தகவல் அறியும் உரிமை (RTI) கட்டணம் மற்றும் காலம் என்ன?"
    ]
}

def get_system_prompt(lang: str) -> str:
    return SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])

def get_disclaimer(lang: str) -> str:
    return DISCLAIMERS.get(lang, DISCLAIMERS["en"])
