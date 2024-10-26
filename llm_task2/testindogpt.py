from transformers import pipeline, GPT2TokenizerFast, GPT2LMHeadModel
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from fpdf import FPDF

# Initialize Flask app and login manager
app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# Simulated user class for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load Hugging Face model and tokenizer
pretrained_name = "w11wo/indo-gpt2-small"
tokenizer = GPT2TokenizerFast.from_pretrained(pretrained_name)
model = GPT2LMHeadModel.from_pretrained(pretrained_name)

# Set up the pipeline for text generation (chatbot)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Simulate conversation storage (for summarization)
conversation_history = []
all_questions_answered=False

medical_questions = [
    "Bagaimana kondisi kesehatan Anda saat ini?",
    "Apakah Anda merasakan gejala seperti demam, batuk, atau sesak napas?",
    "Apakah Anda memiliki riwayat penyakit kronis?",
    "Berapa tekanan darah Anda terakhir kali diukur?",
    "Apakah Anda sedang mengonsumsi obat-obatan?",
    "Apakah ada keluhan lainnya terkait kesehatan Anda?"
]
question_index = 0

# Dictionary untuk menyimpan data summary pasien
summary_data = {}

# Simulated user database with detailed information
users = {
    # Pasien Data
    "pas1": {
        "id": "P001",                 # Unique ID for the patient
        "name": "John Doe",            # Full name of the patient
        "password": "a",         # Password for login
        "role": "pasien",              # Role: either 'pasien' or 'dokter'
        "doctor_id": "D001"            # Associated doctor's ID (dokter in charge)
    },
    "pas2": {
        "id": "P002",
        "name": "Jane Smith",
        "password": "a",
        "role": "pasien",
        "doctor_id": "D002"
    },

        "dok1": {
            "id": "D001",
            "name": "Dr. Siti Aisyah",
            "password": "a",
            "role": "dokter",
            "patients": ["P001"]
        },
        "dok2": {
            "id": "D002",
            "name": "Dr. Bambang Hartono",
            "password": "a",
            "role": "dokter",
            "patients": ["P002"]
        }
}

# Login manager: load user
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Route for login page
@app.route('/loginaa', methods=['GET', 'POST'])
def loginaa():
    return render_template('login1.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users and users[username]['password'] == password:
            if users[username]['role'] == role:
                # if role == "pasien":
                #     user = User(username)
                #     login_user(user)
                #     session['logged_in'] = True
                #     return render_template('choose_doctor.html')
                # elif role == "dokter":
                #     doctorName = session.get('selected_doctor_id')  # Mengambil doctor ID dari sesi
                #     return render_template('doctor_page.html', doctorName=doctorName)

                # Jika role adalah pasien
                if role == "pasien":
                    user = User(username)
                    login_user(user)
                    session['logged_in'] = True
                    session['username'] = username
                    session['doctor_id'] = users[username]['doctor_id']  # Simpan doctor_id pasien
                    return render_template('choose_doctor1.html', doctor_id=session['doctor_id'])

                # Jika role adalah dokter
                elif role == "dokter":
                    doctor_id = users[username]['id']  # Ambil doctor ID dari database
                    doctor_name = users[username]['name']  # Ambil nama dokter dari database
                    session['doctor_id'] = doctor_id
                    session['doctor_name'] = doctor_name

                    # Tampilkan halaman dokter dengan data pasien
                    return render_template('doctor_page1.html', doctorName=doctor_name)

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
    # return render_template('index3.html')

# Choose_doctor route
@app.route('/select_doctor')
@login_required
def select_doctor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('choose_doctor1.html')

# Home route (chatbot and summarization)
@app.route('/home')
@login_required
def home():
    if not session.get('logged_in') or not session.get('selected_doctor_id'):
        return redirect(url_for('login'))
    return render_template('index3.html')

# Chatbot route
@app.route('/chat', methods=['POST'])
@login_required
def chat():
    global question_index
    input_data = request.json
    input_text = input_data.get('text', '')

    if not input_text:
        return jsonify({"error": "No input text provided"}), 400

    # Append user input to conversation history
    conversation_history.append(f"User: {input_text}")

    # Check if we have more questions to ask
    if question_index < len(medical_questions):
        bot_response = medical_questions[question_index]
        question_index += 1
        all_questions_answered = False
    else:
        # If all questions are answered, end the conversation
        bot_response = "Terima kasih, jawaban Anda sudah kami terima."
        all_questions_answered = True

    conversation_history.append(f"Bot: {bot_response}")

    # Return the bot response (the medical question)
    return jsonify({"chatbot_response": bot_response,
                    "all_questions_answered": all_questions_answered})

# Inisialisasi chat
@app.route('/start_chat', methods=['POST'])
@login_required
def start_chat():
    global question_index
    question_index = 0  # Reset indeks pertanyaan untuk memulai percakapan baru

    # Sapaan awal dari bot
    greeting_message = "Halo, selamat datang di layanan chatbot kesehatan kami! Saya akan menanyakan beberapa pertanyaan terkait kesehatan Anda."

    # Ambil pertanyaan pertama dari daftar
    first_question = medical_questions[question_index]
    question_index += 1

    # Gabungkan sapaan dan pertanyaan pertama
    initial_message = f"{greeting_message} {first_question}"

    # Simpan dalam riwayat percakapan
    conversation_history.append(f"Bot: {initial_message}")

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

    # patientUsername = input_data.get('username')
    # patientUsername = 'bambang'
    patientUsername = session.get('username')
    # doctorName = input_data.get('doctor')
    doctorName = session.get('selected_doctor_id')

    print(f"Summarizing for patient: {patientUsername}, doctor: {doctorName}")  # Tambahkan log

    if not conversation_history:
        return jsonify({"summary": "No conversation to summarize!"})

    summary_input = " ".join(conversation_history)
    summary = generator(summary_input, max_new_tokens=50, num_return_sequences=1)[0]["generated_text"]

    # Simpan summary ke dalam data
    pdf_file_path = r"D:\Pythonproj\NLP\llm_task\static\{patient_username}_summary.pdf"
    summary_data[patientUsername] = {
        'doctor': doctorName,
        'summary': summary,
        'pdf_file': pdf_file_path  # Anda mungkin perlu menyimpan path file
    }

    print("Summary Data:", summary_data[patientUsername])

    print(f"Doctor for {patientUsername}: {summary_data[patientUsername]['doctor']}")

    return jsonify({"summary": summary, "pdf_file": pdf_file_path}), 200


@app.route('/generate_pdf', methods=['POST'])
@login_required
def generate_pdf():
    summary = request.json.get('summary', '')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Rangkuman Kesehatan Pengguna', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, summary)

    # Simpan PDF
    pdf_file_path = r"D:\Pythonproj\NLP\llm_task\static\{patient_username}_summary.pdf"
    pdf.output(pdf_file_path)

    return jsonify({"message": "PDF berhasil dihasilkan", "pdf_file": pdf_file_path})


@app.route('/get_patient_data', methods=['GET', 'POST'])
def get_patient_data():
    # doctorName = request.args.get('doctor')

    # Cek isi summary_data
    print("Current summary_data:", summary_data)  # Tambahkan log untuk memeriksa isi data

    doctorName = session.get('selected_doctor_id')
    doctorsession_now = session.get('doctor_id')

    if doctorName == doctorsession_now:
        patients_for_doctor = {patient: data for patient, data in summary_data.items() if data['doctor'] == doctorName}
        print(f"Patients found: {patients_for_doctor}")
        return jsonify(patients_for_doctor), 200

    else:
        return jsonify({"message": "No patients found for this doctor."}), 404

# Serve the PDF file for download
# @app.route('/download_pdf')
# @login_required
# def download_pdf():
#     pdf_file = "conversation_summary.pdf"
#     if os.path.exists(pdf_file):
#         return send_file(pdf_file, as_attachment=True)
#     else:
#         return jsonify({"error": "PDF file not found."}), 404

@app.route('/download_pdf', methods=['GET'])
@login_required
def download_pdf():
    try:
        # Path ke file PDF yang sudah dibuat
        pdf_file_path = r"D:\Pythonproj\NLP\llm_task\static\{patient_username}_summary.pdf"

        # Kirim file PDF ke pengguna
        return send_file(pdf_file_path, as_attachment=True)
    except Exception as e:
        return str(e), 404

# ========================================================================================Doctor Back-end========================================================================================

@app.route('/get_doctors', methods=['GET'])
def get_doctors():
    # Ambil hanya data yang role-nya "dokter"
    doctor_data = {username: info for username, info in users.items() if info.get('role') == 'dokter'}

    # Kembalikan data dokter dalam bentuk JSON
    return jsonify({"doctors": doctor_data})

@app.route('/check_session', methods=['GET'])
def check_session():
    # Cek apakah dokter sudah dipilih
    selected_doctor_id = session.get('selected_doctor_id', None)
    selected_doctor_name = session.get('selected_doctor_name', None)

    if selected_doctor_id:
        return jsonify({"doctor_id": selected_doctor_id, "doctor_name": selected_doctor_name})

    else:
        return jsonify({"error": "No doctor selected in session"})


@app.route('/set_doctor', methods=['POST'])
def set_doctor():
    input_data = request.json
    print("Received data:", input_data)  # Logging received data

    selected_doctor_id = input_data.get('doctor_id')

    if not selected_doctor_id:
        return jsonify({"error": "Doctor ID is missing"}), 400

    # Log doctor ID
    print("Doctor ID:", selected_doctor_id)

    # Simpan dokter yang dipilih dalam sesi
    session['selected_doctor_id'] = selected_doctor_id

    return jsonify({"success": True, "doctor_id": selected_doctor_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)

