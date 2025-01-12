import pyaudio
import wave
import keyboard
import speech_recognition as sr
import gtts
from playsound import playsound
import os
from g4f.client import Client
available_lang = ["af-ZA", "sq-AL", "ar-AE", "ar-AR", "hy-AM", "bn-BD", "bs-BA", "ca-ES", "hr-HR", "cs-CZ",
                "da-DK", "nl-NL", "en-AU", "en-CA", "en-GH", "en-GB", "en-IN", "en-IE", "en-JM", "en-MY",
                "en-NZ", "en-PH", "en-SG", "en-US", "en-ZA", "eo", "et-EE", "tl-PH", "fi-FI", "fr-CA",
                "fr-FR", "de-DE", "de-AT", "de-CH", "el-GR", "gu-IN", "he-IL", "hi-IN", "hu-HU", "is-IS",
                "id-ID", "it-IT", "ja-JP", "jw-ID", "kn-IN", "kk-KZ", "km-KH", "ko-KR", "la", "lv-LV",
                "lt-LT", "mk-MK", "ml-IN", "mn-MN", "mr-IN", "my-MM", "ne-NP", "no-NO", "pl-PL", "pt-BR",
                "pt-PT", "pa-IN", "ro-RO", "ru-RU", "sr-RS", "si-LK", "sk-SK", "sl-SI", "es-AR", "es-BO",
                "es-CL", "es-CO", "es-CR", "es-ES", "es-GT", "es-HN", "es-MX", "es-NI", "es-PA", "es-PE", 
                "es-PR", "es-DO", "es-UY", "es-VE", "su-ID", "sw-TZ", "sw-KE", "ta-IN", "ta-LK", "te-IN", 
                "th-TH", "tr-TR", "uk-UA", "ur-PK", "vi-VN", "cy-GB", "xh-ZA", "yi", "zu-ZA"]
if input("Вам нужен список языков для ознакомления?, если да напишите 'Да'") == "Да":
    print(''' 
    "ar-SA",  # Арабский
    "hy-AM",  # Армянский
    "hr-HR",  # Хорватский
    "cs-CZ",  # Чешский
    "da-DK",  # Датский
    "nl-NL",  # Нидерландский
    "en-US",  # Американский английский
    "en-GB",  # Британский английский
    "eo",     # Эсперанто
    "tl-PH",  # Филиппинский 
    "fi-FI",  # Финский
    "fr-FR",  # Французский
    "de-DE",  # Немецкий
    "el-GR",  # Греческий
    "he-IL",  # Иврит
    "hi-IN",  # Хинди
    "is-IS",  # Исландский
    "id-ID",  # Индонезийский
    "it-IT",  # Итальянский
    "ja-JP",  # Японский
    "kk-KZ",  # Казахский
    "la",     # Латинский
    "lt-LT",  # Литовский
    "pl-PL",  # Польский
    "pt-PT",  # Португальский
    "ro-RO",  # Румынский
    "ru-RU",  # Русский
    "sr-RS",  # Сербский
    "es-ES",  # Испанский
    "sv-SE",  # Шведский
    "tr-TR",  # Турецкий
    "uk-UA",  # Украинский
    "vi-VN",  # Вьетнамский
    Полный список в файле 'языки.txt'
    ''')
def get_language_input(prompt):
    while True:
        lang = input(prompt)
        if lang in available_lang:
            return lang
        else:
            print("Неверный ввод. Пожалуйста, введите язык в формате, например, 'ru-RU' или 'en-US'.")
api_language_1 = get_language_input('Язык первого человека(в формате ru-RU,en-US и другие): ')
api_language_2 = get_language_input('Язык второго человека(в формате ru-RU,en-US и другие): ')

filename = "recorded.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
t = 0
while True:
    t += 1
    p = pyaudio.PyAudio()
    recognizer = sr.Recognizer()
    
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    if t % 2 != 0:
        print("Говорит человек 1. Нажмите пробел когда закончите.")
    else:
        print("Говорит человек 2. Нажмите пробел когда закончите.")
    while True:
        data = stream.read(chunk)
        frames.append(data)
        if keyboard.is_pressed('space'):
            break
    print("Запись закончена")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    audio_ex = sr.AudioFile('recorded.wav')
    type(audio_ex)

    with audio_ex as source:
        audiodata = recognizer.record(audio_ex)
    type(audiodata)
    try:
        text = recognizer.recognize_google(audio_data=audiodata, language=api_language_1)
    except:
        print('Вы ничего не сказали')
    os.remove('recorded.wav')

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": ''.join(["Hello, please translate this text from ", api_language_1, " to ", api_language_2, ":", ' "', text, '". ', "Don't say anything except the answer to my question. You are a professional translator specializing in any languages. Your task is to accurately and naturally convey the meaning, style, and tone of the original text."])}],
    )
    q = response.choices[0].message.content
    print(q)

    tts = gtts.gTTS(str(q), lang=api_language_2[:2])
    tts.save("hello.mp3")
    playsound("hello.mp3")
    os.remove('hello.mp3')
    api_language_1, api_language_2 = api_language_2, api_language_1
    
