"""
Rule-based chatbot for Smart Placement Preparation Assistant
This is a simple rule-based chatbot, NOT a Generative AI model.
It returns predefined responses based on keyword matching.
"""

def get_chatbot_response(message: str) -> str:
    """
    Process user message and return a predefined response based on keywords.
    
    Args:
        message: User's input message
        
    Returns:
        str: Predefined response based on matched keywords
    """
    message_lower = message.lower().strip()
    
    # Greeting responses
    if any(keyword in message_lower for keyword in ['hello', 'hi', 'hey', 'greetings']):
        return ("Hello! I'm your Smart Placement Preparation Assistant. "
                "I can help you with questions about Python, REST APIs, FastAPI, MySQL, "
                "and technical interview preparation. How can I assist you today?")
    
    # Python related
    if 'python' in message_lower:
        return ("Python is a high-level, interpreted programming language known for its "
                "simplicity and readability. It's widely used in web development, data science, "
                "automation, and machine learning. Python is popular in technical interviews because "
                "it allows you to express solutions clearly and concisely.")
    
    # REST API related
    if any(keyword in message_lower for keyword in ['rest api', 'api', 'rest']):
        return ("REST (Representational State Transfer) API is an architectural style for designing "
                "networked applications. It uses HTTP methods like GET (retrieve data), POST (create data), "
                "PUT (update data), and DELETE (remove data). REST APIs communicate using JSON format "
                "and are stateless, making them scalable and easy to use.")
    
    # FastAPI related
    if 'fastapi' in message_lower:
        return ("FastAPI is a modern, fast Python web framework for building APIs. It uses Python type hints "
                "for automatic request validation with Pydantic, generates interactive API documentation "
                "automatically at /docs, and offers high performance comparable to Node.js and Go. "
                "It's excellent for building production-ready APIs quickly.")
    
    # MySQL related
    if any(keyword in message_lower for keyword in ['mysql', 'database', 'sql']):
        return ("MySQL is a popular open-source relational database management system. It stores data in "
                "tables with rows and columns, supports ACID properties for reliable transactions, and uses "
                "SQL (Structured Query Language) for querying. Key concepts include tables, primary keys, "
                "foreign keys for relationships, and indexes for performance.")
    
    # Interview preparation
    if any(keyword in message_lower for keyword in ['interview', 'placement', 'prepare', 'preparation']):
        return ("For technical interview preparation: 1) Practice coding problems regularly on strings, arrays, "
                "and data structures. 2) Understand time and space complexity (Big O notation). "
                "3) Learn to explain your approach before coding. 4) Practice writing clean, readable code. "
                "5) Review common algorithms like sorting, searching, and recursion. "
                "6) Mock interviews help build confidence. Use this platform to track your progress!")
    
    # Help or guidance
    if any(keyword in message_lower for keyword in ['help', 'what can you do', 'topics', 'guide']):
        return ("I can answer questions about the following topics:\n"
                "• Python programming basics\n"
                "• REST APIs and HTTP methods\n"
                "• FastAPI framework\n"
                "• MySQL and databases\n"
                "• Technical interview preparation tips\n\n"
                "Try asking me something like 'What is Python?' or 'How do REST APIs work?'")
    
    # Data structures
    if any(keyword in message_lower for keyword in ['data structure', 'array', 'list', 'dictionary', 'dict']):
        return ("Python offers several built-in data structures:\n"
                "• Lists: Ordered, mutable collections [1, 2, 3]\n"
                "• Tuples: Ordered, immutable collections (1, 2, 3)\n"
                "• Dictionaries: Key-value pairs {'key': 'value'}\n"
                "• Sets: Unordered collections of unique elements {1, 2, 3}\n"
                "Understanding when to use each data structure is crucial for efficient coding.")
    
    # Algorithm complexity
    if any(keyword in message_lower for keyword in ['complexity', 'big o', 'time complexity', 'space complexity']):
        return ("Time and space complexity measure algorithm efficiency:\n"
                "• O(1): Constant time - same regardless of input size\n"
                "• O(log n): Logarithmic - efficient for large inputs (binary search)\n"
                "• O(n): Linear - proportional to input size\n"
                "• O(n log n): Log-linear - efficient sorting algorithms\n"
                "• O(n²): Quadratic - nested loops\n"
                "Always aim for the most efficient solution for your problem.")
    
    # Default response for unknown queries
    return ("I don't have a predefined answer for that question. "
            "I'm a rule-based chatbot with knowledge about Python, REST APIs, FastAPI, MySQL, "
            "and interview preparation. Please try asking about one of these topics, or type 'help' "
            "to see what I can assist you with.")
