/**
 * Smart Placement Preparation Assistant - Frontend JavaScript
 * This file contains all API communication functions using Fetch API
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetch all questions with optional filtering
 */
async function fetchQuestions(category = null, difficulty = null) {
    try {
        let url = `${API_BASE_URL}/questions`;
        const params = new URLSearchParams();
        
        if (category) params.append('category', category);
        if (difficulty) params.append('difficulty', difficulty);
        
        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching questions:', error);
        throw error;
    }
}

/**
 * Fetch a single question by ID
 */
async function fetchQuestion(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Question not found');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching question:', error);
        throw error;
    }
}

/**
 * Create a new question (admin feature)
 */
async function createQuestion(questionData) {
    try {
        const response = await fetch(`${API_BASE_URL}/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(questionData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating question:', error);
        throw error;
    }
}

/**
 * Submit a question attempt
 */
async function createAttempt(attemptData) {
    try {
        const response = await fetch(`${API_BASE_URL}/attempts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(attemptData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating attempt:', error);
        throw error;
    }
}

/**
 * Fetch student progress
 */
async function fetchProgress(studentId) {
    try {
        const response = await fetch(`${API_BASE_URL}/students/${studentId}/progress`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Student not found');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching progress:', error);
        throw error;
    }
}

/**
 * Send a chat message to the chatbot
 */
async function sendChatMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error sending chat message:', error);
        throw error;
    }
}

/**
 * Check if backend is running
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        
        if (!response.ok) {
            return false;
        }
        
        const data = await response.json();
        return data.status === 'active';
    } catch (error) {
        console.error('Backend health check failed:', error);
        return false;
    }
}

/**
 * Display error message
 */
function showError(message, elementId = 'errorMessage') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

/**
 * Hide error message
 */
function hideError(elementId = 'errorMessage') {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

/**
 * Show loading state
 */
function showLoading(elementId = 'loadingMessage') {
    const loadingElement = document.getElementById(elementId);
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
}

/**
 * Hide loading state
 */
function hideLoading(elementId = 'loadingMessage') {
    const loadingElement = document.getElementById(elementId);
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchQuestions,
        fetchQuestion,
        createQuestion,
        createAttempt,
        fetchProgress,
        sendChatMessage,
        checkBackendHealth
    };
}
