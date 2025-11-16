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

}

# Medical questions for chatbot
medical_questions = [
    "Apa keluhan utama yang Anda rasakan?",
    "Sejak kapan keluhan ini muncul?",
    "Apakah ada hal yang memperburuk atau memperbaiki keluhan tersebut?",
    "Apakah ada gejala lain yang Anda rasakan?",
    "Apakah Anda sudah melakukan pengobatan? Jika iya, obat apa yang sudah dikonsumsi?",
    "Apakah Anda memiliki riwayat penyakit, operasi, atau alergi terhadap obat-obatan atau makanan?",
    "Apakah pada anggota keluarga memiliki penyakit atau keluhan serupa seperti yang anda alami saat ini?",
    "Apakah ada informasi tambahan yang ingin Anda sampaikan?"
]

# Global variables for conversation
conversation_history = []
summary_data = {}
question_index = 0
all_questions_answered = False