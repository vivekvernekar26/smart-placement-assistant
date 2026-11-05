# Quick Start Guide

Get the Smart Placement Preparation Assistant running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] MySQL 8.0+ installed and running
- [ ] Git installed (optional)

## Quick Setup (5 Steps)

### 1️⃣ Setup Database (2 minutes)

```bash
# Login to MySQL
mysql -u root -p

# Run the schema
source database/schema.sql

# Exit MySQL
exit
```

### 2️⃣ Configure Backend (1 minute)

```bash
# Create .env file in backend directory
cd backend
cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=placement_assistant
EOF
```

### 3️⃣ Install Dependencies (1 minute)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 4️⃣ Start Backend (30 seconds)

```bash
# Start FastAPI server
python main.py

# You should see: "Database connected successfully"
# API available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

### 5️⃣ Start Frontend (30 seconds)

```bash
# Open NEW terminal
cd frontend

# Start HTTP server
python3 -m http.server 8080

# Open browser to: http://localhost:8080
```

## ✅ Verification

Test that everything works:

1. **Backend Health Check:**
   - Visit http://localhost:8000
   - Should see: `{"message": "Smart Placement Preparation Assistant API is running"...}`

2. **API Documentation:**
   - Visit http://localhost:8000/docs
   - Try the "GET /questions" endpoint
   - Should see a list of 12 sample questions

3. **Frontend:**
   - Visit http://localhost:8080
   - Home page should load with platform statistics
   - Click "View Questions" - should show question cards
   - Click "Chat Now" - type "What is Python?" and test chatbot

## 🐛 Common Issues

### Issue: "Can't connect to MySQL server"
**Solution:** Ensure MySQL is running
```bash
# Check MySQL status
sudo systemctl status mysql    # Linux
brew services list             # Mac with Homebrew
```

### Issue: "Database 'placement_assistant' doesn't exist"
**Solution:** Run the schema file again
```bash
mysql -u root -p < database/schema.sql
```

### Issue: "Module not found"
**Solution:** Activate virtual environment and reinstall
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Issue: "CORS error in browser"
**Solution:** Make sure backend is running and CORS is enabled (already configured in main.py)

### Issue: "Port 8000 already in use"
**Solution:** Kill the process or use a different port
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or run on different port
uvicorn main:app --port 8001
```

## 🎯 Next Steps

Once running:
1. Browse questions at http://localhost:8080/questions.html
2. Submit an attempt on any question
3. View your progress at http://localhost:8080/progress.html
4. Chat with the bot at http://localhost:8080/chatbot.html

## 📚 Learning Path

1. **Understand the Flow:**
   - Frontend → Fetch API → FastAPI Backend → MySQL
   - Read `frontend/app.js` to see API calls
   - Read `backend/main.py` to see endpoint logic

2. **Explore the API:**
   - Go to http://localhost:8000/docs
   - Try each endpoint with the interactive interface
   - See request/response examples

3. **Modify the Code:**
   - Add a new question via the API
   - Create a new chatbot response in `chatbot.py`
   - Customize the CSS in `style.css`

## 💡 Pro Tips

- Keep both backend and frontend terminals open to see logs
- Use browser Developer Tools (F12) to debug Fetch API calls
- Check the Network tab to see all API requests/responses
- Backend auto-reloads on code changes (when using --reload flag)

## 🎓 For Students

This project demonstrates:
- ✅ Full-stack web development
- ✅ RESTful API design
- ✅ Database integration
- ✅ Modern JavaScript (async/await)
- ✅ Pydantic validation
- ✅ CRUD operations

Spend time understanding each component before making changes!

---

**Need help? Check the full README.md for detailed documentation.**
