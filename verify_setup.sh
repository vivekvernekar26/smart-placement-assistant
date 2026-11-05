#!/bin/bash

# Smart Placement Preparation Assistant - Setup Verification Script
# This script checks if all prerequisites are met before running the application

echo "================================================"
echo "Smart Placement Preparation Assistant"
echo "Setup Verification Script"
echo "================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to print check result
check_passed() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

check_failed() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

check_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "Checking prerequisites..."
echo ""

# Check Python
echo "1. Python Installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    check_passed "Python is installed (version $PYTHON_VERSION)"
else
    check_failed "Python 3 is not installed"
    echo "   Install from: https://www.python.org/"
fi
echo ""

# Check MySQL
echo "2. MySQL Installation"
if command -v mysql &> /dev/null; then
    MYSQL_VERSION=$(mysql --version | cut -d " " -f 6 | cut -d "," -f 1)
    check_passed "MySQL is installed (version $MYSQL_VERSION)"
    
    # Check if MySQL is running
    if pgrep -x "mysqld" > /dev/null; then
        check_passed "MySQL service is running"
    else
        check_warning "MySQL service is not running"
        echo "   Start with: sudo systemctl start mysql"
    fi
else
    check_failed "MySQL is not installed"
    echo "   Install from: https://dev.mysql.com/downloads/"
fi
echo ""

# Check project structure
echo "3. Project Structure"
if [ -f "backend/main.py" ]; then
    check_passed "Backend files found"
else
    check_failed "Backend files missing"
fi

if [ -f "frontend/index.html" ]; then
    check_passed "Frontend files found"
else
    check_failed "Frontend files missing"
fi

if [ -f "database/schema.sql" ]; then
    check_passed "Database schema found"
else
    check_failed "Database schema missing"
fi
echo ""

# Check backend dependencies
echo "4. Backend Configuration"
if [ -f "backend/.env" ]; then
    check_passed "Environment file (.env) exists"
else
    check_warning "Environment file (.env) not found"
    echo "   Create from: cp .env.example backend/.env"
    echo "   Then edit with your MySQL password"
fi

if [ -f "backend/requirements.txt" ]; then
    check_passed "Requirements file exists"
else
    check_failed "Requirements file missing"
fi
echo ""

# Check virtual environment
echo "5. Virtual Environment"
if [ -d "venv" ] || [ -d ".venv" ]; then
    check_passed "Virtual environment exists"
    
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        check_passed "Virtual environment is activated"
    else
        check_warning "Virtual environment exists but not activated"
        echo "   Activate with: source venv/bin/activate"
    fi
else
    check_warning "Virtual environment not created"
    echo "   Create with: python3 -m venv venv"
fi
echo ""

# Check Python packages
echo "6. Python Packages"
if [[ "$VIRTUAL_ENV" != "" ]]; then
    if python3 -c "import fastapi" 2>/dev/null; then
        check_passed "FastAPI is installed"
    else
        check_warning "FastAPI not installed"
        echo "   Install with: pip install -r backend/requirements.txt"
    fi
    
    if python3 -c "import mysql.connector" 2>/dev/null; then
        check_passed "MySQL connector is installed"
    else
        check_warning "MySQL connector not installed"
        echo "   Install with: pip install -r backend/requirements.txt"
    fi
else
    check_warning "Activate virtual environment to check packages"
fi
echo ""

# Check database
echo "7. Database Setup"
if command -v mysql &> /dev/null; then
    DB_EXISTS=$(mysql -u root -e "SHOW DATABASES LIKE 'placement_assistant';" 2>/dev/null | grep placement_assistant)
    if [ ! -z "$DB_EXISTS" ]; then
        check_passed "Database 'placement_assistant' exists"
        
        # Check tables
        TABLES=$(mysql -u root placement_assistant -e "SHOW TABLES;" 2>/dev/null | wc -l)
        if [ $TABLES -ge 4 ]; then
            check_passed "Database tables exist"
        else
            check_warning "Database tables may be missing"
            echo "   Run: mysql -u root -p < database/schema.sql"
        fi
    else
        check_warning "Database 'placement_assistant' does not exist"
        echo "   Run: mysql -u root -p < database/schema.sql"
    fi
else
    check_warning "Cannot verify database (MySQL not in PATH)"
fi
echo ""

# Summary
echo "================================================"
echo "VERIFICATION SUMMARY"
echo "================================================"
echo -e "${GREEN}Checks Passed:${NC} $CHECKS_PASSED"
if [ $CHECKS_FAILED -gt 0 ]; then
    echo -e "${RED}Checks Failed:${NC} $CHECKS_FAILED"
fi
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Setup looks good!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Ensure MySQL password is in backend/.env"
    echo "2. Start backend: cd backend && python main.py"
    echo "3. Start frontend: cd frontend && python3 -m http.server 8080"
    echo "4. Visit: http://localhost:8080"
else
    echo -e "${RED}✗ Please fix the failed checks above${NC}"
    echo ""
    echo "See QUICKSTART.md for detailed setup instructions"
fi

echo ""
echo "================================================"
