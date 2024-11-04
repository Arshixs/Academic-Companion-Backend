-- College Table
CREATE TABLE College (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(255) UNIQUE,
    college_location VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Course Table
CREATE TABLE Course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id VARCHAR(10),
    course_name VARCHAR(100),
    college_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (course_id, college_id),
    FOREIGN KEY (college_id) REFERENCES College(id) ON DELETE SET NULL
);

-- User Table
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    password VARCHAR(128),
    email VARCHAR(254),
    branch VARCHAR(100),
    current_semester INT,
    college_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES College(id) ON DELETE SET NULL
);

-- Enrollment Table
CREATE TABLE Enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    course_id INT,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    UNIQUE (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE
);

-- Attendance Table
CREATE TABLE Attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT,
    attendance_date DATE,
    status ENUM('present', 'absent', 'no class'),
    UNIQUE (enrollment_id, attendance_date),
    FOREIGN KEY (enrollment_id) REFERENCES Enrollment(id) ON DELETE CASCADE
);

-- Label Table
CREATE TABLE Label (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (name, user_id),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Assignment Table
CREATE TABLE Assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    status ENUM('todo', 'in-progress', 'done', 'backlog', 'canceled') DEFAULT 'todo',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    label_id INT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (label_id) REFERENCES Label(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

-- CodeSnippet Table
CREATE TABLE CodeSnippet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    code TEXT,
    language ENUM('python', 'cpp', 'c', 'javascript'),
    user_id INT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    INDEX (user_id, language),
    INDEX (is_public, created_at)
);

-- CalendarEvent Table
CREATE TABLE CalendarEvent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    date DATE,
    start_time TIME,
    end_time TIME,
    color ENUM('blue', 'red', 'green', 'yellow') DEFAULT 'blue',
    created_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES User(id) ON DELETE CASCADE
);

-- Note Table
CREATE TABLE Note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(200),
    content TEXT,
    color VARCHAR(50) DEFAULT 'default',
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    INDEX (is_pinned, updated_at)
);

