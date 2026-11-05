-- Smart Placement Preparation Assistant Database Schema

CREATE DATABASE IF NOT EXISTS placement_assistant;
USE placement_assistant;

-- Students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    branch VARCHAR(60),
    study_year INT
);

-- Questions table
CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(60) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'Beginner',
    description TEXT NOT NULL,
    sample_input TEXT,
    expected_output TEXT
);

-- Attempts table
CREATE TABLE attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    question_id INT NOT NULL,
    submitted_answer TEXT,
    score DECIMAL(5,2) DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

-- Sample student data
INSERT INTO students (full_name, branch, study_year) VALUES 
('Demo Student', 'Computer Science', 3);

-- Sample Python questions
INSERT INTO questions (title, category, difficulty, description, sample_input, expected_output) VALUES
('Reverse a String', 'Strings', 'Beginner', 'Write a Python function to reverse a given string.', 'hello', 'olleh'),
('Find Maximum in List', 'Lists', 'Beginner', 'Write a function that finds the maximum value in a list of integers.', '[3, 7, 2, 9, 1]', '9'),
('Check Palindrome', 'Strings', 'Beginner', 'Write a function to check if a string is a palindrome.', 'radar', 'True'),
('Sum of List Elements', 'Lists', 'Beginner', 'Write a function that returns the sum of all elements in a list.', '[1, 2, 3, 4, 5]', '15'),
('Count Vowels', 'Strings', 'Beginner', 'Write a function to count the number of vowels in a string.', 'education', '5'),
('Factorial Calculation', 'Functions', 'Intermediate', 'Write a recursive function to calculate the factorial of a number.', '5', '120'),
('Dictionary Merge', 'Dictionaries', 'Intermediate', 'Write a function to merge two dictionaries.', "{'a': 1}, {'b': 2}", "{'a': 1, 'b': 2}"),
('Prime Number Check', 'Numbers', 'Intermediate', 'Write a function to check if a number is prime.', '17', 'True'),
('List Comprehension Filter', 'Lists', 'Intermediate', 'Use list comprehension to filter even numbers from a list.', '[1, 2, 3, 4, 5, 6]', '[2, 4, 6]'),
('Find Duplicates', 'Lists', 'Intermediate', 'Write a function to find duplicate elements in a list.', '[1, 2, 3, 2, 4, 3]', '[2, 3]'),
('Fibonacci Sequence', 'Functions', 'Advanced', 'Write a function to generate the first n Fibonacci numbers.', '7', '[0, 1, 1, 2, 3, 5, 8]'),
('Two Sum Problem', 'Lists', 'Advanced', 'Find two numbers in a list that add up to a target sum.', '[2, 7, 11, 15], target=9', '[0, 1]');
