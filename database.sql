-- Create database
CREATE DATABASE AcademicCompanion;
USE AcademicCompanion;

-- Users Table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50),
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Branch VARCHAR(100),
    CurrentSemester INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses Table
CREATE TABLE Courses (
    CourseID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Credits INT,
    CourseName VARCHAR(100) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_courses_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Attendance Table
CREATE TABLE Attendance (
    UserID INT,
    CourseID INT,
    AttendanceDate DATE NOT NULL,
    Status ENUM('present', 'absent', 'other', 'no class') NOT NULL,
    CONSTRAINT fk_attendance_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_course FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE,
    PRIMARY KEY (UserID, CourseID, AttendanceDate)
);

-- Assignments Table
CREATE TABLE Assignments (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    CourseID INT,
    Title VARCHAR(100) NOT NULL,
    Description TEXT,
    DueDate DATE,
    CONSTRAINT fk_assignments_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_assignments_course FOREIGN KEY (CourseID) REFERENCES Courses(CourseID) ON DELETE CASCADE,
    UNIQUE (UserID, CourseID, Title)
);

-- Notes Table
CREATE TABLE Notes (
    NoteID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    NoteTitle VARCHAR(100) NOT NULL,
    NoteContent TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notes_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
);

-- Calendar Table
CREATE TABLE Calendar (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    EventTitle VARCHAR(100) NOT NULL,
    EventDescription TEXT,
    EventDate DATE NOT NULL,
    StartTime TIME,
    EndTime TIME,
    CONSTRAINT fk_calendar_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE SET NULL
);

-- Resources Table
CREATE TABLE Resources (
    ResourceID INT AUTO_INCREMENT PRIMARY KEY,      
    UserID INT,                            
    file_name VARCHAR(255) NOT NULL,        
    file_type VARCHAR(50),                 
    file_size BIGINT,                      
    file_path VARCHAR(255) NOT NULL,        
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    description TEXT,                      
    visibility ENUM('private', 'public') DEFAULT 'private', 
    CONSTRAINT fk_resources_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- CodeEditor Table
CREATE TABLE CodeEditor (
    CodeEditorID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,                                
    FileName VARCHAR(255) NOT NULL,        
    code TEXT NOT NULL,                     
    Language VARCHAR(50) DEFAULT 'cpp',  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_codeeditor_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE 

);

-- GeminiIntegration Table
CREATE TABLE GeminiIntegration (
    GeminiID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,                                
    RequestText TEXT NOT NULL,         
    ResponseText TEXT NOT NULL,           
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When the interaction occurred
    CONSTRAINT fk_gemini_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE 
);



