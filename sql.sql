CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT DEFAULT NULL,
    borrower_id INTEGER DEFAULT NULL,
    last_borrowed DATETIME DEFAULT NULL,
    expected_return_time DATETIME DEFAULT NULL,
    added_to_library DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL DEFAULT 1,
    comments TEXT DEFAULT "",
    FOREIGN KEY (borrower_id) REFERENCES user(id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    role INTEGER NOT NULL,
    birthdate DATETIME,
    status BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrowed_time DATETIME NOT NULL,
    expected_return_time DATETIME NOT NULL,
    actual_return_time DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);



-- INSERT INTO user (name, password, role, status) VALUES ('nobody', '', 1, 1);
INSERT INTO user (name, password, role, birthdate, status) VALUES ('admin', 'admin', 0, '1991-08-03', 1);
INSERT INTO user (name, password, role, birthdate, status) VALUES ('user1', 'user1', 1, '1999-04-01', 1);
INSERT INTO user (name, password, role, birthdate, status) VALUES ('user2', 'user2', 1, '1985-01-01', 1);
INSERT INTO user (name, password, role, birthdate, status) VALUES ('user3', 'user3', 1, '2000-01-01', 1);

INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Name of the Wind', 'Patrick Rothfuss', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ("The Wise Man\'s Fear", 'Patrick Rothfuss', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('A Game of Thrones', 'George R. R. Martin', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('A Clash of Kings', 'George R. R. Martin', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('A Storm of Swords', 'George R. R. Martin', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('A Feast for Crows', 'George R. R. Martin', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('A Dance with Dragons', 'George R. R. Martin', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Fellowship of the Ring', 'J.R.R. Tolkien', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Two Towers', 'J.R.R. Tolkien', 'Fantasy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('1984', 'George Orwell', 'Dystopian', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('Pride and Prejudice', 'Jane Austen', 'Romance', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 'Tragedy', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('Moby Dick', 'Herman Melville', 'Adventure', NULL, NULL, 1, '');
INSERT INTO book (book_name, author, genre, borrower_id, last_borrowed, status, comments) 
VALUES ('The Da Vinci Code', 'Dan Brown', 'Thriller', NULL, NULL, 1, '');

INSERT INTO record (user_id, book_id, borrowed_time, expected_return_time, actual_return_time) VALUES (2, 1, '2020-01-01', '2020-01-08', '2020-01-07');