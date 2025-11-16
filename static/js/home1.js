// Fungsi untuk menampilkan layar utama
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Fungsi untuk menampilkan modal (Pop-up)
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
    // Sembunyikan scrollbar pada layar utama saat modal aktif
    document.getElementById('homeScreen').style.overflowY = 'hidden';
}

// Fungsi untuk menyembunyikan modal
function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    // Kembalikan scrollbar layar utama
    document.getElementById('homeScreen').style.overflowY = 'auto';
}

function selectAntrean(type) {
    hideModal('antreanModal');
    showScreen('confirmationScreen');
    // Store selected type if needed
    console.log('Selected antrean type:', type);
}

function goBackToForms() {
    document.querySelectorAll('.form-group').forEach(el => el.style.display = 'block');
    document.querySelector('.section-title').style.display = 'block';
    document.querySelector('button[onclick="startAnamnesis()"]').style.display = 'block';
    document.getElementById('chatbox').classList.add('hidden');
    document.getElementById('inputSection').classList.add('hidden');
    document.getElementById('summarySectionBtn').classList.add('hidden');
    document.getElementById('summarySection').classList.add('hidden');
}

// Update doctors based on selected poli
document.getElementById('poliSelect').addEventListener('change', updateDoctors);

function updateDoctors() {
    const poli = document.getElementById('poliSelect').value;
    const doctorSelect = document.getElementById('doctorSelect');
    doctorSelect.innerHTML = '';

    if (poli === 'Poli Umum') {
        doctorSelect.innerHTML = `
            <option>Dr. Siti Aisyah - 09:00</option>
            <option>Dr. Ahmad - 10:00</option>
            <option>Dr. Lina - 11:00</option>
        `;
    } else if (poli === 'Poli Anak') {
        doctorSelect.innerHTML = `
            <option>Dr. Budi - 09:00</option>
            <option>Dr. Citra - 14:00</option>
            <option>Dr. Dedi - 15:00</option>
        `;
    } else if (poli === 'Poli Jantung') {
        doctorSelect.innerHTML = `
            <option>Dr. Eko - 10:00</option>
            <option>Dr. Fani - 13:00</option>
        `;
    } else if (poli === 'Poli Kandungan') {
        doctorSelect.innerHTML = `
            <option>Dr. Gina - 08:00</option>
            <option>Dr. Hana - 12:00</option>
        `;
    } else if (poli === 'Poli Mata') {
        doctorSelect.innerHTML = `
            <option>Dr. Iwan - 09:00</option>
            <option>Dr. Joko - 16:00</option>
        `;
    } else {
        doctorSelect.innerHTML = '<option>Pilih poli terlebih dahulu</option>';
    }
}

async function startAnamnesis() {
    // Get form data
    const faskes = document.getElementById('faskesSelect').value;
    const date = document.getElementById('dateInput').value;
    const poli = document.getElementById('poliSelect').value;
    const doctor = document.getElementById('doctorSelect').value;

    // Save antrean
    const formData = new FormData();
    formData.append('faskes', faskes);
    formData.append('date', date);
    formData.append('poli', poli);
    formData.append('doctor', doctor);

    try {
        const response = await fetch('/save_antrean', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        console.log('Antrean saved:', data.antrean_number);
        // Store data for later use
        window.savedAntrean = {
            faskes: faskes,
            date: date,
            poli: poli,
            doctor: doctor,
            antrean_number: data.antrean_number
        };
    } catch (error) {
        console.error('Error saving antrean:', error);
    }

    // Hide forms and show chat
    document.querySelectorAll('.form-group').forEach(el => el.style.display = 'none');
    document.querySelector('.section-title').style.display = 'none';
    document.querySelector('button[onclick="startAnamnesis()"]').style.display = 'none';
    document.getElementById('chatbox').classList.remove('hidden');
    document.getElementById('inputSection').classList.remove('hidden');
    document.getElementById('summarySectionBtn').classList.remove('hidden');
    // Start chat
    sendInitialMessage();
}

// Chat functions
const chatbox = document.getElementById("chatbox");

async function sendInitialMessage() {
    const response = await fetch('/start_chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    const botResponse = data.chatbot_response;

    chatbox.innerHTML += `
        <div class="flex items-center mb-4">
            <div class="w-12 flex-shrink-0 flex items-center justify-center">
                <div class="h-10 w-10 rounded-full bg-blue-500 text-white font-bold text-lg flex items-center justify-center">B</div>
            </div>
            <div class="ml-2 bg-white text-gray-800 py-2 px-4 rounded-xl shadow-sm max-w-xs text-sm">${botResponse}</div>
        </div>
        `;
    chatbox.scrollTop = chatbox.scrollHeight;
}

let allQuestionsAnswered = false;

async function sendMessage() {
    if (allQuestionsAnswered) {
        alert("All questions have been answered. No further responses are required.");
        return;
    }

    const userInput = document.getElementById("userInput").value;
    if (userInput === '') {
        alert("Please enter a message.");
        return;
    }

    chatbox.innerHTML += `
    <div class="flex justify-end items-center mb-4">
        <div class="mr-2 bg-white text-gray-800 py-2 px-4 rounded-xl shadow-sm max-w-xs text-sm">${userInput}</div>
        <div class="flex items-center justify-center h-10 w-10 rounded-full bg-purple-500 text-white font-bold text-lg">U</div>
    </div>
    `;

    document.getElementById("userInput").value = '';

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: userInput })
    });

    const data = await response.json();
    const botResponse = data.chatbot_response;

    chatbox.innerHTML += `
    <div class="flex items-center mb-4">
            <div class="w-12 flex-shrink-0 flex items-center justify-center">
                <div class="h-10 w-10 rounded-full bg-blue-500 text-white font-bold text-lg flex items-center justify-center">B</div>
            </div>
            <div class="ml-2 bg-white text-gray-800 py-2 px-4 rounded-xl shadow-sm max-w-xs text-sm">${botResponse}</div>
    </div>
    `;

    chatbox.scrollTop = chatbox.scrollHeight;

    if (data.all_questions_answered) {
        allQuestionsAnswered = true;
        disableInput();
    }
}

function disableInput() {
    document.getElementById("userInput").disabled = true;
    document.getElementById("sendMessage").disabled = true;
}

function startSpeechToText() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'id-ID';

    recognition.start();

    recognition.onresult = function(event) {
        const speechToText = event.results[0][0].transcript;
        document.getElementById("userInput").value = speechToText;
        sendMessage();
    };
}

// Function for showing summary
async function showSummary() {
    // Display the antrean details first
    const antrean = window.savedAntrean;
    if (antrean) {
        document.getElementById('summaryContent').innerHTML = `
            <h4>Nomor Antrean: ${antrean.antrean_number}</h4>
            <p><strong>Faskes:</strong> ${antrean.faskes}</p>
            <p><strong>Poli:</strong> ${antrean.poli}</p>
            <p><strong>Dokter:</strong> ${antrean.doctor}</p>
            <p><strong>Tanggal:</strong> ${antrean.date}</p>
            <p>Rekaman keluhan Anda sudah dikirimkan ke dokter.</p>
        `;
        document.getElementById('summarySection').style.display = 'block';
    } else {
        document.getElementById('summaryContent').innerHTML = `<p>Data antrean tidak ditemukan.</p>`;
        document.getElementById('summarySection').style.display = 'block';
    }

    // Add home button
    const homeButton = document.createElement('button');
    homeButton.textContent = 'Kembali ke Home';
    homeButton.className = 'btn primary full-width mt-2';
    homeButton.onclick = () => showScreen('homeScreen');
    document.getElementById('summarySection').appendChild(homeButton);

    // Try to generate summary/PDF
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: "test",
                doctor: "test"
            })
        });

        const data = await response.json();
        if (!response.ok) {
            console.error("Failed to generate summary:", data.summary || "Unknown error");
        }
    } catch (error) {
        console.error("Error fetching summary from server:", error);
    }
}

// Add enter key listener for send message
document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Placeholder for voice input logic using microphone
document.getElementById('micButton').addEventListener('click', startSpeechToText);