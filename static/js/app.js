// AarogyaSarvam Client Application Controller
let currentTab = 'intake';
let chatHistory = [];
let doctorsList = [];
let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

// Audio player cache
const globalAudio = new Audio();

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    loadDoctors();
    loadAppointments();
    loadInsuranceClaims();
    loadReminders();
    setupAudioRecording();
}

// Tab Switching
function switchTab(tabId) {
    currentTab = tabId;
    ['intake', 'insurance', 'reminders', 'overview'].forEach(tab => {
        const el = document.getElementById(`tab-content-${tab}`);
        const btn = document.getElementById(`nav-btn-${tab}`);
        if (tab === tabId) {
            el.classList.remove('hidden');
            btn.classList.add('bg-teal-600', 'text-white', 'shadow-md');
            btn.classList.remove('text-slate-600', 'hover:bg-slate-100');
        } else {
            el.classList.add('hidden');
            btn.classList.remove('bg-teal-600', 'text-white', 'shadow-md');
            btn.classList.add('text-slate-600', 'hover:bg-slate-100');
        }
    });

    if (tabId === 'overview') {
        updateStats();
    }
}

// ----------------------------------------------------
// 1. INTAKE & APPOINTMENT MODULE
// ----------------------------------------------------
async function loadDoctors() {
    try {
        const res = await fetch('/api/doctors');
        const data = await res.json();
        doctorsList = data.doctors || [];
        
        const docSelect = document.getElementById('doctor-select');
        if (docSelect) {
            docSelect.innerHTML = '<option value="">-- Choose Specialist Doctor --</option>';
            doctorsList.forEach(doc => {
                const opt = document.createElement('option');
                opt.value = doc.id;
                opt.textContent = `${doc.name} (${doc.specialty}) - ₹${doc.fee}`;
                docSelect.appendChild(opt);
            });
        }
        renderDoctorsList();
    } catch (e) {
        console.error('Failed to load doctors:', e);
    }
}

function renderDoctorsList() {
    const container = document.getElementById('doctors-roster-container');
    if (!container) return;
    container.innerHTML = doctorsList.map(doc => `
        <div class="p-3 bg-white border border-slate-200 rounded-xl hover:border-teal-500 transition-all cursor-pointer" onclick="selectDoctorForBooking('${doc.id}')">
            <div class="flex items-center justify-between">
                <div>
                    <h4 class="font-semibold text-slate-800 text-sm">${doc.name}</h4>
                    <p class="text-xs text-teal-600 font-medium">${doc.specialty}</p>
                </div>
                <span class="text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded-full font-medium">₹${doc.fee}</span>
            </div>
            <div class="mt-2 flex items-center gap-1 flex-wrap">
                ${doc.languages.map(l => `<span class="text-[10px] bg-teal-50 text-teal-700 px-1.5 py-0.5 rounded">${l}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

function selectDoctorForBooking(docId) {
    const select = document.getElementById('doctor-select');
    if (select) {
        select.value = docId;
        select.scrollIntoView({ behavior: 'smooth' });
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    appendChatMessage('user', msg);

    // Typing indicator
    const typingId = appendTypingIndicator();

    try {
        const res = await fetch('/api/chat/intake', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, history: chatHistory })
        });
        const data = await res.json();
        removeTypingIndicator(typingId);

        const reply = data.reply || "I am here to assist with your medical care.";
        appendChatMessage('assistant', reply);
        chatHistory.push({ role: 'user', content: msg });
        chatHistory.push({ role: 'assistant', content: reply });
    } catch (err) {
        removeTypingIndicator(typingId);
        appendChatMessage('assistant', "Apologies, there was an error communicating with Sarvam AI: " + err.message);
    }
}

function appendChatMessage(role, text) {
    const container = document.getElementById('chat-messages');
    const isUser = role === 'user';
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`;

    msgDiv.innerHTML = `
        <div class="max-w-[85%] rounded-2xl px-4 py-3 ${isUser ? 'bg-teal-600 text-white rounded-br-none' : 'bg-white border border-slate-200 text-slate-800 shadow-sm rounded-bl-none'}">
            <div class="flex items-center gap-2 mb-1">
                <span class="text-xs font-semibold ${isUser ? 'text-teal-100' : 'text-teal-700'}">${isUser ? 'Patient' : 'AarogyaSarvam (105B)'}</span>
            </div>
            <p class="text-sm leading-relaxed whitespace-pre-line">${escapeHtml(text)}</p>
            ${!isUser ? `
                <div class="mt-2 pt-2 border-t border-slate-100 flex items-center gap-2">
                    <button onclick="playTTS(this, '${encodeURIComponent(text)}')" class="text-xs text-teal-600 hover:text-teal-700 flex items-center gap-1 font-medium bg-teal-50 px-2 py-1 rounded">
                        <i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Listen (Bulbul Voice)
                    </button>
                    <button onclick="fillBookingFromChat('${encodeURIComponent(text)}')" class="text-xs text-slate-500 hover:text-slate-700 flex items-center gap-1 font-medium">
                        <i data-lucide="calendar" class="w-3.5 h-3.5"></i> Book Appointment
                    </button>
                </div>
            ` : ''}
        </div>
    `;

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
    lucide.createIcons();
}

function appendTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'flex justify-start mb-3';
    div.innerHTML = `
        <div class="bg-white border border-slate-200 text-slate-500 rounded-2xl px-4 py-3 rounded-bl-none shadow-sm flex items-center gap-2">
            <span class="text-xs font-medium">AarogyaSarvam is thinking</span>
            <div class="flex gap-1">
                <div class="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce"></div>
                <div class="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                <div class="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.4s]"></div>
            </div>
        </div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// Voice Recording (Sarvam Saaras STT)
function setupAudioRecording() {
    const micBtn = document.getElementById('mic-record-btn');
    if (!micBtn) return;

    micBtn.addEventListener('click', async () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });
}

let activeMimeType = 'audio/webm';

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Detect supported MIME type
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            activeMimeType = 'audio/webm;codecs=opus';
        } else if (MediaRecorder.isTypeSupported('audio/webm')) {
            activeMimeType = 'audio/webm';
        } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
            activeMimeType = 'audio/ogg;codecs=opus';
        } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
            activeMimeType = 'audio/mp4';
        } else {
            activeMimeType = '';
        }

        const options = activeMimeType ? { mimeType: activeMimeType } : {};
        mediaRecorder = new MediaRecorder(stream, options);
        audioChunks = [];

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };

        mediaRecorder.onstop = async () => {
            const blobType = activeMimeType || 'audio/webm';
            const audioBlob = new Blob(audioChunks, { type: blobType });
            await processVoiceRecording(audioBlob, blobType);
            stream.getTracks().forEach(t => t.stop());
        };

        mediaRecorder.start();
        isRecording = true;
        updateMicUI(true);
    } catch (err) {
        alert("Microphone permission denied or not supported in this browser: " + err.message);
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        updateMicUI(false);
    }
}

function updateMicUI(recording) {
    const btn = document.getElementById('mic-record-btn');
    const statusText = document.getElementById('mic-status-text');
    if (recording) {
        btn.classList.add('bg-red-500', 'text-white', 'recording-pulse');
        btn.classList.remove('bg-slate-100', 'text-slate-700');
        if (statusText) statusText.textContent = "Listening... Click mic again when done to send to Sarvam Saaras STT";
    } else {
        btn.classList.remove('bg-red-500', 'text-white', 'recording-pulse');
        btn.classList.add('bg-slate-100', 'text-slate-700');
        if (statusText) statusText.textContent = "Voice Assistant ready (Hindi, Tamil, Marathi, Telugu, English)";
    }
}

async function processVoiceRecording(blob, mimeType) {
    const langSelect = document.getElementById('intake-lang-select');
    const selectedLang = langSelect ? langSelect.value : 'unknown';

    const ext = mimeType.includes('webm') ? 'webm' : (mimeType.includes('ogg') ? 'ogg' : 'wav');
    const formData = new FormData();
    formData.append('file', blob, `patient_voice.${ext}`);
    formData.append('language_code', selectedLang);

    const input = document.getElementById('chat-input');
    input.placeholder = "Transcribing with Sarvam Saaras v4...";

    try {
        const res = await fetch('/api/voice/transcribe', {
            method: 'POST',
            body: formData
        });
        if (!res.ok) {
            const errJson = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(errJson.detail || "Server returned status " + res.status);
        }
        const data = await res.json();
        input.placeholder = "Describe symptoms or speak in any Indian language...";
        if (data.success && data.transcript) {
            input.value = data.transcript;
            sendChatMessage();
        } else {
            alert("Could not transcribe voice audio: " + (data.error || "Please try speaking clearly"));
        }
    } catch (e) {
        input.placeholder = "Describe symptoms or speak in any Indian language...";
        alert("STT Error: " + e.message + "\nPlease make sure the server is running on http://localhost:8000");
    }
}

// Text to Speech Player (Sarvam Bulbul TTS)
async function playTTS(btn, encodedText) {
    const text = decodeURIComponent(encodedText);
    const origHtml = btn.innerHTML;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> Generating Voice...`;
    lucide.createIcons();

    const langSelect = document.getElementById('intake-lang-select');
    const lang = langSelect ? langSelect.value : 'hi-IN';

    try {
        const res = await fetch('/api/voice/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                language_code: lang,
                speaker: "shubh"
            })
        });
        const data = await res.json();
        btn.innerHTML = origHtml;
        lucide.createIcons();

        if (data.success && data.audio_base64) {
            globalAudio.src = `data:audio/wav;base64,${data.audio_base64}`;
            globalAudio.play();
        } else {
            alert("Could not generate voice: " + (data.error || "Unknown error"));
        }
    } catch (e) {
        btn.innerHTML = origHtml;
        lucide.createIcons();
        alert("TTS Error: " + e.message);
    }
}

// Booking Form Submit
async function submitBookingForm(e) {
    e.preventDefault();
    const btn = document.getElementById('book-submit-btn');
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Confirming Booking...`;
    lucide.createIcons();

    const form = e.target;
    const payload = {
        patient_name: form.patient_name.value,
        phone: form.phone.value,
        age: parseInt(form.age.value) || 35,
        gender: form.gender.value,
        doctor_id: form.doctor_id.value,
        date: form.date.value,
        time: form.time.value,
        symptoms: form.symptoms.value,
        language_preference: form.language_preference.value,
        booking_mode: "Sarvam AI Multilingual Intake"
    };

    try {
        const res = await fetch('/api/appointments/book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4"></i> Confirm Appointment`;
        lucide.createIcons();

        if (data.success) {
            showConfirmationModal(data.appointment, data.confirmation_message);
            form.reset();
            loadAppointments();
        }
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4"></i> Confirm Appointment`;
        lucide.createIcons();
        alert("Booking failed: " + err.message);
    }
}

function showConfirmationModal(apt, msg) {
    const modal = document.getElementById('booking-modal');
    document.getElementById('modal-apt-id').textContent = apt.id;
    document.getElementById('modal-patient-name').textContent = apt.patient_name;
    document.getElementById('modal-doc-name').textContent = `${apt.doctor_name} (${apt.specialty})`;
    document.getElementById('modal-slot').textContent = `${apt.date} at ${apt.time}`;
    document.getElementById('modal-conf-text').textContent = msg;
    modal.classList.remove('hidden');
}

function closeBookingModal() {
    document.getElementById('booking-modal').classList.add('hidden');
}

async function loadAppointments() {
    try {
        const res = await fetch('/api/appointments');
        const data = await res.json();
        const container = document.getElementById('appointments-table-body');
        if (!container) return;

        container.innerHTML = (data.appointments || []).map(apt => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="py-3 px-4 font-mono text-xs font-semibold text-teal-700">${apt.id}</td>
                <td class="py-3 px-4 text-sm font-medium text-slate-800">${apt.patient_name} <span class="text-xs text-slate-400">(${apt.age}y, ${apt.gender})</span></td>
                <td class="py-3 px-4 text-sm text-slate-700">${apt.doctor_name}</td>
                <td class="py-3 px-4 text-sm text-slate-600">${apt.date} ${apt.time}</td>
                <td class="py-3 px-4 text-xs text-slate-500 max-w-xs truncate">${apt.symptoms}</td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 text-xs rounded-full bg-emerald-50 text-emerald-700 font-medium">${apt.status}</span>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Failed to load appointments:', e);
    }
}

// ----------------------------------------------------
// 2. CASHLESS INSURANCE & PRE-AUTH MODULE
// ----------------------------------------------------
async function loadInsuranceClaims() {
    try {
        const res = await fetch('/api/insurance/claims');
        const data = await res.json();
        const container = document.getElementById('claims-table-body');
        if (!container) return;

        container.innerHTML = (data.claims || []).map(c => `
            <tr class="border-b border-slate-100 hover:bg-slate-50">
                <td class="py-3 px-4 font-mono text-xs font-semibold text-teal-700">${c.id}</td>
                <td class="py-3 px-4 text-sm font-medium text-slate-800">${c.patient_name}</td>
                <td class="py-3 px-4 text-sm text-slate-700">
                    <div>${c.insurer}</div>
                    <div class="text-xs text-slate-400 font-mono">${c.policy_number}</div>
                </td>
                <td class="py-3 px-4 text-sm text-slate-700 max-w-xs truncate">${c.treatment_name}</td>
                <td class="py-3 px-4 text-sm text-slate-600">₹${Number(c.estimated_cost).toLocaleString()}</td>
                <td class="py-3 px-4 text-sm font-semibold text-emerald-600">₹${Number(c.approved_amount).toLocaleString()}</td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 text-xs rounded-full ${c.approval_status === 'Approved' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'} font-medium">
                        ${c.approval_status}
                    </span>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        console.error('Failed to load claims:', e);
    }
}

async function loadSamplePolicy(sampleKey) {
    try {
        const res = await fetch(`/api/insurance/sample/${sampleKey}`);
        const data = await res.json();
        
        const form = document.getElementById('preauth-form');
        form.patient_name.value = data.insured_name || '';
        form.policy_number.value = data.policy_number || '';
        form.insurer.value = data.insurer || '';
        form.sum_insured.value = data.sum_insured || 500000;
        form.treatment_name.value = data.proposed_treatment || '';
        form.estimated_cost.value = data.estimated_hospital_bill || 50000;
        form.room_category.value = data.hospital_room || 'Twin Sharing';
        form.policy_age_years.value = data.policy_age_years || 3;
        form.document_text.value = data.document_text || '';

        // Flash container to show loaded sample
        const preview = document.getElementById('doc-preview-box');
        if (preview) {
            preview.classList.add('ring-2', 'ring-teal-500');
            setTimeout(() => preview.classList.remove('ring-2', 'ring-teal-500'), 1000);
        }
    } catch (e) {
        alert("Failed to load sample: " + e.message);
    }
}

async function submitPreAuthForm(e) {
    e.preventDefault();
    const btn = document.getElementById('verify-preauth-btn');
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Sarvam AI Adjudicating Claim...`;
    lucide.createIcons();

    const form = e.target;
    const payload = {
        patient_name: form.patient_name.value,
        policy_number: form.policy_number.value,
        insurer: form.insurer.value,
        tpa: "In-House Hospital TPA Desk",
        sum_insured: parseFloat(form.sum_insured.value) || 500000,
        treatment_name: form.treatment_name.value,
        estimated_cost: parseFloat(form.estimated_cost.value) || 50000,
        room_category: form.room_category.value,
        policy_age_years: parseInt(form.policy_age_years.value) || 3,
        pre_existing_status: form.pre_existing_status.value || "None",
        document_text: form.document_text.value || ""
    };

    try {
        const res = await fetch('/api/insurance/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="shield-check" class="w-4 h-4"></i> Run Cashless Pre-Authorization`;
        lucide.createIcons();

        if (data.success) {
            renderPreAuthResult(data.claim, data.adjudication);
            loadInsuranceClaims();
        }
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="shield-check" class="w-4 h-4"></i> Run Cashless Pre-Authorization`;
        lucide.createIcons();
        alert("Pre-auth verification failed: " + err.message);
    }
}

function renderPreAuthResult(claim, adj) {
    const card = document.getElementById('preauth-result-card');
    card.classList.remove('hidden');
    card.scrollIntoView({ behavior: 'smooth' });

    document.getElementById('res-auth-code').textContent = claim.pre_auth_code;
    document.getElementById('res-status-badge').textContent = claim.approval_status;
    document.getElementById('res-approved-amt').textContent = `₹${Number(claim.approved_amount).toLocaleString()}`;
    document.getElementById('res-patient-liability').textContent = `₹${Number(claim.patient_liability).toLocaleString()}`;
    document.getElementById('res-estimated-amt').textContent = `₹${Number(claim.estimated_cost).toLocaleString()}`;
    document.getElementById('res-summary-text').textContent = adj.adjudication_summary || claim.remarks;

    const checklistEl = document.getElementById('res-checklist');
    if (checklistEl && adj.coordinator_checklist) {
        checklistEl.innerHTML = adj.coordinator_checklist.map(item => `
            <li class="flex items-center gap-2 text-xs text-slate-700">
                <i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-teal-600"></i> ${item}
            </li>
        `).join('');
        lucide.createIcons();
    }
}

// ----------------------------------------------------
// 3. PROACTIVE CARE REMINDERS MODULE
// ----------------------------------------------------
async function loadReminders() {
    try {
        const res = await fetch('/api/reminders');
        const data = await res.json();
        const container = document.getElementById('reminders-grid');
        if (!container) return;

        container.innerHTML = (data.reminders || []).map(r => `
            <div class="p-4 bg-white border border-slate-200 rounded-xl card-hover flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-mono font-semibold text-teal-700">${r.id}</span>
                        <span class="text-[11px] font-medium px-2 py-0.5 rounded-full bg-teal-50 text-teal-700">${r.language_code}</span>
                    </div>
                    <h4 class="font-semibold text-slate-800 text-sm mb-1">${r.patient_name}</h4>
                    <p class="text-xs text-slate-500 mb-2">${r.campaign_type}</p>
                    <div class="p-3 bg-slate-50 rounded-lg text-xs text-slate-700 mb-3 border border-slate-100 italic">
                        "${r.message}"
                    </div>
                </div>
                <div>
                    <div class="flex items-center justify-between text-xs text-slate-500 mb-2">
                        <span><i data-lucide="clock" class="w-3 h-3 inline"></i> ${r.scheduled_time}</span>
                        <span class="font-medium text-emerald-600">${r.status}</span>
                    </div>
                    <button onclick="playReminderVoice(this, '${encodeURIComponent(r.message)}', '${r.language_code}')" class="w-full py-1.5 px-3 bg-teal-50 text-teal-700 hover:bg-teal-100 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all">
                        <i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Listen to Native Voice Call
                    </button>
                </div>
            </div>
        `).join('');
        lucide.createIcons();
    } catch (e) {
        console.error('Failed to load reminders:', e);
    }
}

async function playReminderVoice(btn, encodedText, langCode) {
    const text = decodeURIComponent(encodedText);
    const orig = btn.innerHTML;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> Generating Sarvam Voice...`;
    lucide.createIcons();

    try {
        const res = await fetch('/api/voice/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                language_code: langCode,
                speaker: "shubh"
            })
        });
        const data = await res.json();
        btn.innerHTML = orig;
        lucide.createIcons();

        if (data.success && data.audio_base64) {
            globalAudio.src = `data:audio/wav;base64,${data.audio_base64}`;
            globalAudio.play();
        } else {
            alert("TTS playback error: " + (data.error || "Failed to generate audio"));
        }
    } catch (e) {
        btn.innerHTML = orig;
        lucide.createIcons();
        alert("Playback error: " + e.message);
    }
}

async function submitReminderDispatch(e) {
    e.preventDefault();
    const btn = document.getElementById('dispatch-reminder-btn');
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Dispatching Voice Call...`;
    lucide.createIcons();

    const form = e.target;
    const payload = {
        patient_name: form.patient_name.value,
        phone: form.phone.value,
        campaign_type: form.campaign_type.value,
        language_code: form.language_code.value,
        custom_message: form.custom_message.value,
        generate_voice: true
    };

    try {
        const res = await fetch('/api/reminders/dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="send" class="w-4 h-4"></i> Dispatch Proactive Outreach`;
        lucide.createIcons();

        if (data.success) {
            alert(`Voice outreach dispatched successfully to ${payload.patient_name} in ${payload.language_code}!`);
            form.reset();
            loadReminders();
        }
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="send" class="w-4 h-4"></i> Dispatch Proactive Outreach`;
        lucide.createIcons();
        alert("Dispatch failed: " + err.message);
    }
}

// ----------------------------------------------------
// 4. OVERVIEW / KPI STATS
// ----------------------------------------------------
async function updateStats() {
    try {
        const [aptRes, claimRes, remRes] = await Promise.all([
            fetch('/api/appointments'),
            fetch('/api/insurance/claims'),
            fetch('/api/reminders')
        ]);
        const apts = await aptRes.json();
        const claims = await claimRes.json();
        const rems = await remRes.json();

        document.getElementById('stat-apts-count').textContent = (apts.appointments || []).length;
        document.getElementById('stat-claims-count').textContent = (claims.claims || []).length;
        document.getElementById('stat-reminders-count').textContent = (rems.reminders || []).length;
    } catch (e) {
        console.error('Failed to update stats:', e);
    }
}

// Helper: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function fillBookingFromChat(encodedText) {
    const text = decodeURIComponent(encodedText);
    const form = document.getElementById('appointment-booking-form');
    if (form) {
        form.symptoms.value = text.slice(0, 150);
        form.scrollIntoView({ behavior: 'smooth' });
    }
}

