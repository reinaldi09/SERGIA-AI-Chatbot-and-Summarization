from flask import Flask, render_template

app = Flask(__name__)

# Route for login page
@app.route('/loginaa', methods=['GET', 'POST'])
def loginaa():
    return render_template('login1.html')

if __name__ == '__main__':
    app.run(debug=True)

# import speech_recognition as sr
#
# # Inisialisasi recognizer
# recognizer = sr.Recognizer()
#
# # Fungsi untuk menangkap suara dari mikrofon dan mengubahnya ke teks dalam bahasa Indonesia
# def realtime_speech_to_text():
#     try:
#         with sr.Microphone() as source:
#             print("Menyesuaikan kebisingan sekitar... Harap tunggu!")
#             recognizer.adjust_for_ambient_noise(source)  # Sesuaikan dengan kebisingan sekitar
#             print("Mikrofon siap. Silakan mulai berbicara...")
#
#             while True:
#                 print("Mendengarkan...")
#                 audio = recognizer.listen(source)
#
#                 try:
#                     # Ubah suara menjadi teks menggunakan Google Web Speech API dengan bahasa Indonesia
#                     text = recognizer.recognize_google(audio, language="id-ID")
#                     print(f"Teks Terkenali: {text}")
#                 except sr.UnknownValueError:
#                     print("Maaf, saya tidak bisa mengenali suara.")
#                 except sr.RequestError as e:
#                     print(f"Tidak dapat memproses hasil; {e}")
#     except KeyboardInterrupt:
#         print("Program dihentikan.")
#
# if __name__ == "__main__":
#     realtime_speech_to_text()

# import sounddevice as sd
# import queue
# import vosk
# import json
#
# # Inisialisasi model bahasa Indonesia
# model = vosk.Model("path_ke_folder_model_bahasa_indonesia")
#
# q = queue.Queue()
#
# def callback(indata, frames, time, status):
#     if status:
#         print(status, flush=True)
#     q.put(bytes(indata))
#
# # Mulai pengenalan suara
# def realtime_speech_to_text():
#     with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
#                            channels=1, callback=callback):
#         recognizer = vosk.KaldiRecognizer(model, 16000)
#         print("Silakan berbicara...")
#
#         while True:
#             data = q.get()
#             if recognizer.AcceptWaveform(data):
#                 result = recognizer.Result()
#                 text = json.loads(result).get("text", "")
#                 print(f"Teks Terkenali: {text}")
#             else:
#                 partial_result = recognizer.PartialResult()
#                 print(partial_result)
#
# if __name__ == "__main__":
#     realtime_speech_to_text()
