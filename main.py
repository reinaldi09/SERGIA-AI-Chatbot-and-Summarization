import os
import sqlite3
from datetime import datetime
from transformers import pipeline, GPT2TokenizerFast, GPT2LMHeadModel
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file, send_from_directory, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from fpdf import FPDF
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import data
import shutil

# Initialize Flask app and login manager
app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# Database functions
def get_db():
    db = sqlite3.connect('sergia.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT,
            password TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS antrean (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            faskes TEXT,
            date TEXT,
            poli TEXT,
            doctor TEXT,
            antrean_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        # Insert default users if not exist
        for username, info in data.users.items():
            db.execute('INSERT OR IGNORE INTO users (email, name, password) VALUES (?, ?, ?)', (username + '@example.com', info['name'], info['password']))
        db.commit()

init_db()

# Simulated user class for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load Hugging Face model and tokenizer
# pretrained_name = "w11wo/indo-gpt2-small"
# tokenizer = GPT2TokenizerFast.from_pretrained(pretrained_name)
# model = GPT2LMHeadModel.from_pretrained(pretrained_name)

# # Set up the pipeline for text generation (chatbot)
# generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

pipe = pipeline("summarization", model="MbahLaba/Sergia_Summarization")
gen_kwargs = {'length_penalty': 0.8, 'num_beams': 8, "max_length": 150}

# Login manager: load user
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    try:
        with get_db() as db:
            db.execute('INSERT INTO users (email, name, password) VALUES (?, ?, ?)', (email, name, password))
            db.commit()
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        return "Email already exists", 400

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = get_db().execute('SELECT * FROM users WHERE email = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            # Login
            user_obj = User(user['id'])
            login_user(user_obj)
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['email']
            session['patient_name'] = user['name']
            # For simplicity, set doctor_id to a default, or from data
            session['doctor_id'] = 'D001'  # default
            session['selected_doctor_id'] = 'D001'
            return render_template('home1.html', doctor_id=session['doctor_id'], patient_name=session['patient_name'])

        else:
            return jsonify({"error": "Invalid credentials"}), 401
    # return render_template('login.html')
    return render_template('login1.html')

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))

# Home route (chatbot and summarization)
@app.route('/')
def home1():
    return redirect(url_for('login'))
    # return render_template('index4.html')



# Chatbot route
@app.route('/chat', methods=['POST'])
@login_required
def chat():
    input_data = request.json
    input_text = input_data.get('text', '')

    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    # Append user input to conversation history
    data.conversation_history.append(f"User: {input_text}")

    # Check if we have more questions to ask
    if data.question_index < len(data.medical_questions):
        bot_response = data.medical_questions[data.question_index]
        data.question_index += 1
        data.all_questions_answered = False
    else:
        # If all questions are answered, end the conversation
        bot_response = "Terima kasih, jawaban Anda sudah kami terima."
        data.all_questions_answered = True

    data.conversation_history.append(f"Bot: {bot_response}")

    # Return the bot response (the medical question)
    return jsonify({"chatbot_response": bot_response,
                    "all_questions_answered": data.all_questions_answered})

# Inisialisasi chat
@app.route('/start_chat', methods=['POST'])
@login_required
def start_chat():
    data.question_index = 0  # Reset indeks pertanyaan untuk memulai percakapan baru

    # Sapaan awal dari bot
    # greeting_message = "Halo, selamat datang di layanan chatbot kesehatan kami! Saya akan menanyakan beberapa pertanyaan terkait kesehatan Anda."
    greeting_message = " "

    # Ambil pertanyaan pertama dari daftar
    first_question = data.medical_questions[data.question_index]
    data.question_index += 1

    # Gabungkan sapaan dan pertanyaan pertama
    initial_message = f"{greeting_message} {first_question}"

    # Simpan dalam riwayat percakapan
    data.conversation_history.append(f"Bot: {initial_message}")

    # Kembalikan sapaan dan pertanyaan pertama ke frontend
    return jsonify({"chatbot_response": initial_message})

# Summarization route
@app.route('/summarize', methods=['POST'])
@login_required
def summarize():
    # Summarize the conversation (simplified approach)
    input_data = request.json
    if input_data is None:
        return jsonify({"error": "No input data received"}), 400
    print("Received input data:", input_data)

    patientUsername = session.get('username')
    patient_name = session.get('patient_name')
    doctor_id = session.get('selected_doctor_id')
    doctor_name = next((info['name'] for info in data.users.values() if info.get('id') == doctor_id), doctor_id)

    # Get antrean data
    faskes = poli = appointment_date = "N/A"
    with get_db() as db:
        row = db.execute('SELECT * FROM antrean WHERE user_id = ? ORDER BY id DESC LIMIT 1', (session.get('user_id'),)).fetchone()
        if row:
            faskes = row['faskes']
            poli = row['poli']
            appointment_date = row['date']
            doctor_full = row['doctor']
            # Use the full doctor name from antrean
            doctor_name = doctor_full

    # print(f"Summarizing for patient: {patientUsername}, doctor: {doctorName}")  # Tambahkan log

    if not data.conversation_history:
        return jsonify({"summary": "No conversation to summarize!"})

    summary_input = " ".join(data.conversation_history)
    # summary = generator(summary_input, max_new_tokens=50, num_return_sequences=1)[0]["generated_text"]

    print(f"SI : {summary_input}")
    print(f"CH : {data.conversation_history}")

    # Use the LLM model for summarization
    summary = pipe(summary_input, **gen_kwargs)
    print(summary[0]['summary_text'])

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Laporan Anamnesis Pasien', ln=True, align='C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Pasien: {patient_name}', ln=True)
    pdf.cell(0, 10, f'Dokter: {doctor_name}', ln=True)
    pdf.cell(0, 10, f'Faskes: {faskes}', ln=True)
    pdf.cell(0, 10, f'Poli: {poli}', ln=True)
    pdf.cell(0, 10, f'Tanggal Kunjungan: {appointment_date}', ln=True)
    pdf.cell(0, 10, f'Waktu Pembuatan Laporan: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Riwayat Percakapan:', ln=True)
    pdf.set_font('Arial', '', 10)
    for line in data.conversation_history:
        pdf.multi_cell(0, 8, line)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Ringkasan Anamnesis:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, summary[0]['summary_text'])

    pdf_file_path = os.path.join("clinic_summaries", f"{patientUsername}_summary.pdf")
    os.makedirs("clinic_summaries", exist_ok=True)
    pdf.output(pdf_file_path)

    # Simpan summary ke dalam data
    data.summary_data[patientUsername] = {
        'doctor': doctor_id,
        'summary': summary[0]['summary_text'],
        'pdf_file': pdf_file_path
    }

    print(f"PDF summary for patient {patientUsername} saved to clinic system at {pdf_file_path}")
    print("PDF Content:")
    print(f"Patient: {patient_name}")
    print(f"Doctor: {doctor_name}")
    print(f"Faskes: {faskes}")
    print(f"Poli: {poli}")
    print(f"Tanggal Kunjungan: {appointment_date}")
    print(f"Waktu Pembuatan Laporan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Conversation History:")
    for line in data.conversation_history:
        print(line)
    print("Summary:")
    print(summary[0]['summary_text'])

    return jsonify({"summary": summary[0]['summary_text'], "pdf_file": f"/clinic_summaries/{patientUsername}_summary.pdf", "message": "Summary generated and sent to clinic system."}), 200

# Save antrean data
@app.route('/save_antrean', methods=['POST'])
@login_required
def save_antrean():
    faskes = request.form['faskes']
    date = request.form['date']
    poli = request.form['poli']
    doctor = request.form['doctor']
    user_id = session.get('user_id')

    # Generate antrean_number: doctor_code + count (simplified)
    doctor_code = doctor.split(' - ')[0][:3].upper()
    with get_db() as db:
        cursor = db.execute('SELECT COUNT(*) as count FROM antrean WHERE doctor = ?', (doctor,))
        count = cursor.fetchone()['count'] + 1
        antrean_number = f"{doctor_code}{count:03d}"
        db.execute('INSERT INTO antrean (user_id, faskes, date, poli, doctor, antrean_number) VALUES (?, ?, ?, ?, ?, ?)', (user_id, faskes, date, poli, doctor, antrean_number))
        db.commit()

    return jsonify({'antrean_number': antrean_number})

@app.route('/get_patient_data', methods=['GET', 'POST'])
def get_patient_data():
    doctorName = session.get('selected_doctor_id')
    doctorsession_now = session.get('doctor_id')

    if doctorName == doctorsession_now:
        with get_db() as db:
            rows = db.execute('SELECT * FROM antrean WHERE doctor = ?', (doctorName,)).fetchall()
            patients_for_doctor = {row['id']: dict(row) for row in rows}
        print(f"Patients found: {patients_for_doctor}")
        return jsonify(patients_for_doctor), 200

    else:
        return jsonify({"message": "No patients found for this doctor."}), 404

@app.route('/clinic_summaries/<filename>')
@login_required
def serve_clinic_file(filename):
    return send_from_directory('clinic_summaries', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)

