# SERGIA: AI-Powered Anamnesis and Summarization for JKN

## Description

SERGIA (Sistem Ringkas Rekam Medis Otomatis Berbasis Generative AI) is a comprehensive web application that integrates with the Indonesian National Health Insurance (JKN) system. It provides a mobile-friendly interface for patients to register for appointments, undergo AI-driven anamnesis (pre-consultation questioning), and generate automated medical summaries. The system simulates sending data to clinic/hospital internal systems for efficient healthcare delivery.

## Features

- **Mobile JKN Interface:** Responsive mobile app simulation for JKN services, including appointment booking.
- **AI Anamnesis Chatbot:** Interactive chatbot that asks patients 8 standardized medical questions in Indonesian.
- **Automated Summarization:** Generates concise medical summaries using AI models (with fallback to simple text processing).
- **PDF Report Generation:** Creates professional PDF reports including patient details, conversation history, and summaries.
- **Clinic Integration Simulation:** Saves reports to a dedicated folder and logs data transmission to clinic systems.
- **User Authentication:** Secure login system with role-based access (patients and doctors).
- **Database Integration:** Uses SQLite for storing user data, appointments, and summaries.
- **Voice Input Support:** Includes microphone functionality for voice-to-text input.

## Project Structure

```
SERGIA-AI-Chatbot-and-Summarization/
├── main.py                 # Flask application entry point
├── data.py                 # Data models and constants
├── sergia.db               # SQLite database
├── requirements.txt        # Python dependencies
├── clinic_summaries/       # Folder for generated PDF reports
├── static/
│   ├── css/
│   │   └── home1.css       # Styles for mobile interface
│   ├── js/
│   │   └── home1.js        # JavaScript for mobile interface
│   └── images/             # Static images (logos, etc.)
├── templates/
│   ├── login1.html         # Login page
│   ├── home1.html          # Main mobile JKN interface
│   └── index4.html         # Standalone chatbot interface
└── README.md
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SERGIA-AI-Chatbot-and-Summarization
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Access the app:**
   Open your browser and go to `http://localhost:5000`

## Usage

### For Patients:
1. **Login:** Use patient credentials (e.g., username: pas1, password: a)
2. **Book Appointment:** Select "Ambil Antrean" and choose facility type
3. **Fill Details:** Enter facility, date, department, and doctor
4. **Anamnesis:** Answer 8 AI-guided questions about symptoms and medical history
5. **Generate Summary:** Click "Selesai" to create PDF summary and send to clinic system

### For Doctors:
1. **Login:** Use doctor credentials (e.g., username: dok1, password: a)
2. **View Patients:** Access patient summaries (simulated in current version)

## Key Components

### AI Summarization
- Uses Hugging Face transformers for text summarization
- Fallback to simple text processing if model unavailable
- Generates Indonesian medical summaries

### Database Schema
- **users:** Stores patient and doctor information
- **antrean:** Records appointment bookings with queue numbers

### API Endpoints
- `/login`: User authentication
- `/chat`: Chatbot interaction
- `/summarize`: Generate summary and PDF
- `/save_antrean`: Save appointment data
- `/clinic_summaries/<filename>`: Serve PDF reports

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **AI/ML:** Transformers, Torch
- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
- **PDF Generation:** FPDF

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

