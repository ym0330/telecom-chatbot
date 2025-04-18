// Global variables
let currentUser = null;
let accessToken = null;

// DOM Elements
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const chatSection = document.getElementById('chatSection');
const loginSection = document.getElementById('loginSection');
const registerSection = document.getElementById('registerSection');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const profileSection = document.getElementById('profileSection');
const profileData = document.getElementById('profileData');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check for stored token
    const storedToken = localStorage.getItem('accessToken');
    if (storedToken) {
        accessToken = storedToken;
        fetchUserProfile();
    }
});

loginForm.addEventListener('submit', handleLogin);
registerForm.addEventListener('submit', handleRegister);
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Navigation Functions
function showLogin() {
    loginSection.style.display = 'block';
    registerSection.style.display = 'none';
    chatSection.style.display = 'none';
    profileSection.style.display = 'none';
}

function showRegister() {
    loginSection.style.display = 'none';
    registerSection.style.display = 'block';
    chatSection.style.display = 'none';
    profileSection.style.display = 'none';
}

function showChat() {
    loginSection.style.display = 'none';
    registerSection.style.display = 'none';
    chatSection.style.display = 'block';
    profileSection.style.display = 'none';
    loadChatHistory();
}

function showProfile() {
    loginSection.style.display = 'none';
    registerSection.style.display = 'none';
    chatSection.style.display = 'none';
    profileSection.style.display = 'block';
    displayProfileData();
}

// Authentication Functions
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            accessToken = data.access_token;
            localStorage.setItem('accessToken', accessToken);
            currentUser = data.user;
            showChat();
        } else {
            // Show more specific error message
            const errorMessage = data.detail || 'Login failed. Please check your username and password.';
            alert(errorMessage);
            console.error('Login error:', data);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            showLogin();
        } else {
            alert(data.detail || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

// Chat Functions
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        
        if (response.ok) {
            appendMessage('user', message);
            appendMessage('bot', data.response);
            messageInput.value = '';
        } else {
            alert(data.detail || 'Failed to send message');
        }
    } catch (error) {
        console.error('Chat error:', error);
        alert('Failed to send message. Please try again.');
    }
}

async function loadChatHistory() {
    try {
        const response = await fetch('/chat-history', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        
        if (response.ok) {
            chatMessages.innerHTML = '';
            data.history.forEach(msg => {
                appendMessage(msg.role, msg.content);
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

function appendMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Profile Functions
async function fetchUserProfile() {
    try {
        const response = await fetch('/profile', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        
        if (response.ok) {
            currentUser = data;
            displayProfileData();
        } else {
            localStorage.removeItem('accessToken');
            showLogin();
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
        localStorage.removeItem('accessToken');
        showLogin();
    }
}

function displayProfileData() {
    if (!currentUser) return;

    const profileHTML = `
        <h2>Account Information</h2>
        <div class="profile-info">
            <p><strong>Username:</strong> ${currentUser.username}</p>
            <p><strong>Email:</strong> ${currentUser.email}</p>
            <p><strong>Account Number:</strong> ${currentUser.account_number}</p>
            <p><strong>Plan Type:</strong> ${currentUser.plan_type}</p>
            <p><strong>Monthly Fee:</strong> ${currentUser.monthly_fee}</p>
            <p><strong>Balance:</strong> ${currentUser.balance}</p>
            <p><strong>Last Bill Date:</strong> ${currentUser.last_bill_date || 'N/A'}</p>
            <p><strong>Last Bill Amount:</strong> ${currentUser.last_bill_amount}</p>
            <p><strong>Status:</strong> ${currentUser.status}</p>
            <p><strong>Data Usage:</strong> ${currentUser.data_usage} / ${currentUser.data_limit}</p>
            <p><strong>Contract End Date:</strong> ${currentUser.contract_end_date || 'N/A'}</p>
            <p><strong>Payment Method:</strong> ${currentUser.payment_method || 'Not set'}</p>
            <p><strong>Auto Pay:</strong> ${currentUser.auto_pay ? 'Enabled' : 'Disabled'}</p>
            <p><strong>Paperless Billing:</strong> ${currentUser.paperless_billing ? 'Enabled' : 'Disabled'}</p>
        </div>
        <button onclick="showLogin()">Logout</button>
    `;
    
    profileData.innerHTML = profileHTML;
}

// Logout Function
function logout() {
    localStorage.removeItem('accessToken');
    accessToken = null;
    currentUser = null;
    showLogin();
} 