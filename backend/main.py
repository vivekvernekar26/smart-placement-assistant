"""
Smart Placement Preparation Assistant - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from schemas import (
    QuestionCreate, QuestionResponse, AttemptCreate, 
    AttemptResponse, ProgressResponse, ChatRequest, ChatResponse
)
from database import db
from chatbot import get_chatbot_response

app = FastAPI(
    title="Smart Placement Preparation Assistant API",
    description="REST API for technical interview preparation platform",
    version="1.0.0"
)

# CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    db.connect()
    print("Database connected successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from database on shutdown"""
    db.disconnect()
    print("Database disconnected")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Smart Placement Preparation Assistant API is running",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/questions", response_model=List[QuestionResponse])
async def get_questions(category: Optional[str] = None, difficulty: Optional[str] = None):
    """
    Get all questions with optional filtering by category and difficulty
    
    Query Parameters:
    - category: Filter by question category (optional)
    - difficulty: Filter by difficulty level (optional)
    """
    try:
        if category and difficulty:
            query = "SELECT * FROM questions WHERE category = %s AND difficulty = %s"
            questions = db.fetch_query(query, (category, difficulty))
        elif category:
            query = "SELECT * FROM questions WHERE category = %s"
            questions = db.fetch_query(query, (category,))
        elif difficulty:
            query = "SELECT * FROM questions WHERE difficulty = %s"
            questions = db.fetch_query(query, (difficulty,))
        else:
            query = "SELECT * FROM questions"
            questions = db.fetch_query(query)
        
        return questions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching questions: {str(e)}"
        )

@app.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int):
    """
    Get a specific question by ID
    
    Path Parameters:
    - question_id: The ID of the question to retrieve
    """
    try:
        query = "SELECT * FROM questions WHERE question_id = %s"
        question = db.fetch_one(query, (question_id,))
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        
        return question
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching question: {str(e)}"
        )

@app.post("/questions", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate):
    """
    Create a new question (Admin feature)
    
    Request Body:
    - title: Question title
    - category: Question category (e.g., Strings, Lists, etc.)
    - difficulty: Difficulty level (Beginner, Intermediate, Advanced)
    - description: Full question description
    - sample_input: Example input (optional)
    - expected_output: Expected output (optional)
    """
    try:
        query = """
        INSERT INTO questions (title, category, difficulty, description, sample_input, expected_output)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        question_id = db.execute_query(
            query, 
            (
                question.title,
                question.category,
                question.difficulty,
                question.description,
                question.sample_input,
                question.expected_output
            )
        )
        
        if not question_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create question"
            )
        
        # Fetch and return the created question
        created_question = db.fetch_one(
            "SELECT * FROM questions WHERE question_id = %s",
            (question_id,)
        )
        return created_question
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating question: {str(e)}"
        )

@app.post("/attempts", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
async def create_attempt(attempt: AttemptCreate):
    """
    Record a student's attempt at a question
    
    Request Body:
    - student_id: ID of the student
    - question_id: ID of the question attempted
    - submitted_answer: Student's answer (optional)
    - score: Score achieved (0-100)
    - completed: Whether the attempt is marked as completed
    """
    try:
        # Verify student exists
        student = db.fetch_one("SELECT * FROM students WHERE student_id = %s", (attempt.student_id,))
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {attempt.student_id} not found"
            )
        
        # Verify question exists
        question = db.fetch_one("SELECT * FROM questions WHERE question_id = %s", (attempt.question_id,))
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {attempt.question_id} not found"
            )
        
        # Insert attempt
        query = """
        INSERT INTO attempts (student_id, question_id, submitted_answer, score, completed)
        VALUES (%s, %s, %s, %s, %s)
        """
        attempt_id = db.execute_query(
            query,
            (
                attempt.student_id,
                attempt.question_id,
                attempt.submitted_answer,
                attempt.score,
                attempt.completed
            )
        )
        
        if not attempt_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to record attempt"
            )
        
        # Fetch and return the created attempt
        created_attempt = db.fetch_one(
            "SELECT * FROM attempts WHERE attempt_id = %s",
            (attempt_id,)
        )
        return created_attempt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error recording attempt: {str(e)}"
        )

@app.get("/students/{student_id}/progress", response_model=ProgressResponse)
async def get_student_progress(student_id: int):
    """
    Get progress summary for a student
    
    Path Parameters:
    - student_id: The ID of the student
    
    Returns:
    - total_attempts: Total number of attempts made
    - completed_questions: Number of questions marked as completed
    - average_score: Average score across all attempts
    - attempts: List of all attempts with question details
    """
    try:
        # Verify student exists
        student = db.fetch_one("SELECT * FROM students WHERE student_id = %s", (student_id,))
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        # Get all attempts for the student with question details
        attempts_query = """
        SELECT a.*, q.title, q.category, q.difficulty
        FROM attempts a
        JOIN questions q ON a.question_id = q.question_id
        WHERE a.student_id = %s
        ORDER BY a.attempted_at DESC
        """
        attempts = db.fetch_query(attempts_query, (student_id,))
        
        # Calculate statistics
        total_attempts = len(attempts)
        completed_questions = sum(1 for a in attempts if a['completed'])
        average_score = sum(a['score'] for a in attempts) / total_attempts if total_attempts > 0 else 0
        
        return {
            "student_id": student_id,
            "total_attempts": total_attempts,
            "completed_questions": completed_questions,
            "average_score": round(average_score, 2),
            "attempts": attempts
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching progress: {str(e)}"
        )

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """
    Chat with the rule-based assistant
    
    Request Body:
    - message: User's question or message
    
    Returns:
    - message: Original user message
    - response: Chatbot's response based on predefined rules
    """
    try:
        if not chat_request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        response = get_chatbot_response(chat_request.message)
        
        return {
            "message": chat_request.message,
            "response": response
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
