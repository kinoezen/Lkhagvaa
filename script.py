# 1. Майкрософтын нууц API санг суулгах хэсэг
!pip install edge-tts

import asyncio
import os
import re
from edge_tts import Communicate

# =====================================================================
# 2. ОДДЫН ДАЙН БОЛОН БУСАД КИНОНЫ ТЕКСТЭЭ ЦАГИЙН КОДТОЙ НЬ ЭНД ХУУЛЖ ТАВИНА
# =====================================================================
RAW_TEXT = """
1
00:01:20,000 --> 00:01:23,000
Урт хугацааны өмнө, алсын алс дахь галактикт...

2
00:01:24,500 --> 00:01:28,000
Оддын дайн: 5 дугаар анги - Эзэнт гүрэн хариу цохилт өгсөн нь.
"""

# 3. Цагийн код устгаж, текстийг киноны амьд уншлагад зориулж хөрвүүлэх функц
def clean_and_build_ssml(text):
    # Цагийн кодуудыг автоматаар арилгах хэсэг
    text = re.sub(r'\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}', '', text)
    text = re.sub(r'[\[\(]\d{2}:\d{2}[\]\)]', '', text)
    text = re.sub(r'\b\d{2}:\d{2}\b', '', text)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # КИНОГ АМИЛУУЛАХ ХАК: Цэг таслал дээр гоё зогсолт хийлгэх хэсэг
    ssml_text = ""
    for line in lines:
        # Таслал дээр 800ms (0.8 сек) амьсгаа авна
        line = line.replace(", ", '<break time="800ms"/>')
        line = line.replace(",", '<break time="800ms"/>')
        
        # Цэг дээр 1500ms (1.5 сек) жүжиглэж зогсоно
        line = line.replace(". ", '. <break time="1500ms"/>')
        
        if not line.endswith("."):
            ssml_text += line + ' <break time="1500ms"/>\n'
        else:
            ssml_text += line + "\n"
            
    return ssml_text

CLEANED_TEXT = clean_and_build_ssml(RAW_TEXT)

# 4. ДУУ ХОЛОЙНЫ ТӨГС ТОХИРГОО (Дунд зэрэг)
VOICE = "mn-MN-BataaNeural"
RATE = "+0%"   # Хурд: Дунд зэрэг
PITCH = "+0Hz" # Өнгө: Дунд зэрэг (Бүдүүн ч биш, нарийхан ч биш)
OUTPUT_FILE = "starwars_perfect_audio.mp3"

async def generate_audio():
    if not CLEANED_TEXT.strip():
        print("❌ Алдаа: Текст хоосон байна.")
        return
    try:
        # SSML форматыг бэлдэж байна
        ssml_string = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='mn-MN'>
            <voice name='{VOICE}'><prosody rate='{RATE}' pitch='{PITCH}'>
                {CLEANED_TEXT}
            </prosody></voice>
        </speak>"""
        
        communicate = Communicate()
        await communicate.save_ssml(ssml_string, OUTPUT_FILE)
        print("\n🚀 100% ТӨГС БОЛЛОО! Скрипт амжилттай ажиллаж дууслаа.")
    except Exception as e:
        print(f"❌ Системд алдаа гарлаа: {e}")

# Ажиллуулах
await generate_audio()

# 5. Файлыг шууд Windows 7 компьютер руу татаж авах хэсэг
if os.path.exists(OUTPUT_FILE):
    from google.colab import files
    files.download(OUTPUT_FILE)
