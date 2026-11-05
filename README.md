# Smart Placement Preparation Assistant

A full-stack web application built with Python, FastAPI, MySQL, and JavaScript to help engineering students prepare for technical placement interviews.

## 📋 Project Overview

This platform allows students to:
- Browse and solve Python programming questions
- Take quizzes and track progress
- Get instant help from a rule-based chatbot
- Monitor performance with detailed statistics

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python + FastAPI |
| **Validation** | Pydantic |
| **Database** | MySQL |
| **Integration** | Fetch API + JSON |
| **Chatbot** | Python rule-based function |

## ✨ Features

### Must-Have Features (Implemented)
- ✅ Display list of programming questions with category and difficulty
- ✅ View individual question details with sample input/output
- ✅ Submit answers and mark questions as completed
- ✅ Store attempts and scores in MySQL database
- ✅ Track progress with attempt count and average score
- ✅ Rule-based chatbot for technical questions
- ✅ Fetch API integration for all backend communication
- ✅ Proper error handling for empty inputs and failed requests

### Optional Extensions (Not Implemented)
- ⬜ Administrator page to manage questions
- ⬜ Timed multiple-choice quizzes with automatic scoring
- ⬜ Advanced filtering by topic or difficulty
- ⬜ Personalized topic recommendations
- ⬜ User authentication and login

## 📁 Project Structure

```
smart-placement-assistant/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── database.py          # Database connection and query functions
│   ├── schemas.py           # Pydantic models for validation
│   ├── chatbot.py           # Rule-based chatbot logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html          # Home page
│   ├── questions.html      # Questions list and details
│   ├── progress.html       # Student progress dashboard
│   ├── chatbot.html        # Chatbot interface
│   ├── style.css           # Application styles
│   └── app.js              # API communication functions
├── database/
│   └── schema.sql          # Database schema and sample data
├── screenshots/            # Application screenshots
└── README.md              # This file
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- A modern web browser

### Step 1: Clone the Repository
```bash
cd /path/to/your/projects
git clone <repository-url>
cd smart-placement-assistant
```

### Step 2: Set Up MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database and tables
source database/schema.sql

# Verify data
USE placement_assistant;
SELECT COUNT(*) FROM questions;
SELECT * FROM students;
```

### Step 3: Configure Environment Variables
Create a `.env` file in the `backend/` directory:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=placement_assistant
```

**Important:** Never commit the `.env` file to version control!

### Step 4: Install Python Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 5: Run the Backend Server
```bash
# From project root
cd backend
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Step 6: Run the Frontend
```bash
# Open a new terminal
cd frontend

# Start a simple HTTP server
# Python 3:
python3 -m http.server 8080

# The frontend will be available at http://localhost:8080
```

## 📚 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/questions` | Get all questions (supports filtering) |
| GET | `/questions/{id}` | Get specific question |
| POST | `/questions` | Create new question (admin) |
| POST | `/attempts` | Submit question attempt |
| GET | `/students/{id}/progress` | Get student progress |
| POST | `/chat` | Chat with rule-based bot |

### Example API Requests

**Get all questions:**
```bash
curl http://localhost:8000/questions
```

**Get questions filtered by category:**
```bash
curl "http://localhost:8000/questions?category=Strings"
```

**Submit an attempt:**
```bash
curl -X POST http://localhost:8000/attempts \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "question_id": 1,
    "submitted_answer": "def reverse(s): return s[::-1]",
    "score": 100,
    "completed": true
  }'
```

**Chat with bot:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Python?"}'
```

## 🤖 Chatbot Information

The chatbot is **rule-based** and uses keyword matching to provide predefined responses. It is **NOT** a Generative AI model like ChatGPT.

### Supported Topics:
- Python programming basics
- REST APIs and HTTP methods
- FastAPI framework features
- MySQL and relational databases
- Technical interview preparation tips
- Data structures and algorithms
- Time and space complexity

### Example Questions:
- "What is Python?"
- "How do REST APIs work?"
- "Tell me about FastAPI"
- "Explain MySQL databases"
- "Interview preparation tips"

### Future Enhancement
The architecture supports replacing the rule-based function with an LLM API (like OpenAI GPT) by modifying `backend/chatbot.py` to make external API calls instead of using keyword matching.

## 🧪 Testing

### Manual Testing Checklist
- [ ] Backend starts without errors
- [ ] API documentation loads at `/docs`
- [ ] GET `/questions` returns question list
- [ ] Invalid question ID returns 404
- [ ] Attempt submission saves to database
- [ ] Progress page shows attempt history
- [ ] Frontend fetches real data from backend
- [ ] Chatbot responds to known keywords
- [ ] Empty inputs are rejected
- [ ] Error messages display when backend is stopped

### Testing with API Docs
1. Navigate to `http://localhost:8000/docs`
2. Use the interactive interface to test each endpoint
3. Verify responses and status codes

## 📊 Database Schema

### Students Table
```sql
student_id (PK) | full_name | branch | study_year
```

### Questions Table
```sql
question_id (PK) | title | category | difficulty | description | sample_input | expected_output
```

### Attempts Table
```sql
attempt_id (PK) | student_id (FK) | question_id (FK) | submitted_answer | score | completed | attempted_at
```

## 🔒 Security Considerations

- ✅ Parameterized SQL queries to prevent SQL injection
- ✅ Pydantic validation for all API inputs
- ✅ Environment variables for database credentials
- ✅ CORS middleware configured
- ❌ Authentication not implemented (demo version uses student ID 1)
- ❌ No rate limiting on API endpoints

## 📈 Known Limitations

1. **Authentication:** The application uses a demo student (ID: 1) instead of real login
2. **Single User:** No multi-user support or session management
3. **Chatbot:** Rule-based only, not AI-powered
4. **No Admin Panel:** Questions must be added via SQL or API calls
5. **Basic Validation:** Submitted code is not executed or validated automatically
6. **No File Upload:** Students cannot upload solution files

## 👥 Team Contributions

This project can be divided among team members as follows:

**Member 1 - Backend Developer:**
- FastAPI endpoints and routing
- Pydantic schemas and validation
- Error handling

**Member 2 - Database Engineer:**
- MySQL schema design
- Sample data creation
- Query optimization

**Member 3 - Frontend Developer:**
- HTML/CSS interface
- JavaScript Fetch API integration
- Responsive design

**Member 4 - Chatbot & QA:**
- Rule-based chatbot logic
- Testing all features
- Documentation and screenshots

## 📸 Screenshots

Screenshots are stored in the `screenshots/` directory:
1. Home page with features
2. Questions list with filters
3. Question detail with submission form
4. Progress dashboard
5. Chatbot conversation

## 🎓 Learning Outcomes Achieved

Students who complete this project will understand:
- ✅ Python functions, data structures, and conditional logic
- ✅ REST API design with FastAPI
- ✅ Request validation using Pydantic
- ✅ MySQL table design and CRUD operations
- ✅ Frontend-backend integration with Fetch API
- ✅ Difference between rule-based and AI chatbots
- ✅ Full-stack application testing and deployment

## 🚦 Future Enhancements

1. **User Authentication:** Implement JWT-based login system
2. **Code Execution:** Integrate a code runner to test submitted solutions
3. **AI Integration:** Connect OpenAI or similar API for smarter chatbot
4. **Advanced Analytics:** Add charts for progress visualization
5. **Social Features:** Allow students to share solutions and discuss
6. **Mobile App:** Build React Native or Flutter mobile version
7. **Competitive Mode:** Add leaderboards and timed challenges

## 📄 License

This is an educational project created for academic purposes.

## 🤝 Contributing

This is a student mini-project. For academic integrity, please complete your own implementation before referring to this code.

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Verify database connection and table creation
3. Check browser console for JavaScript errors
4. Ensure backend is running before testing frontend

## 🎯 Project Completion Criteria

A project is considered complete when:
- ✅ Students can view questions from database through browser
- ✅ Students can submit attempts and see progress
- ✅ Chatbot accepts messages and returns responses
- ✅ Frontend and backend communicate via HTTP/JSON
- ✅ Team can explain all technologies used
- ✅ Documentation and screenshots are complete
- ✅ No secrets are exposed in code repository

---

**Built with ❤️ for engineering students preparing for placements**
