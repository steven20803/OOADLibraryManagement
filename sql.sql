CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    borrowed BOOLEAN NOT NULL DEFAULT FALSE,
    borrower_id INTEGER DEFAULT 1,
    last_borrowed DATETIME DEFAULT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE,
    comments TEXT DEFAULT "",
    FOREIGN KEY (borrower_id) REFERENCES user(id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    role INTEGER NOT NULL,
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
INSERT INTO user (name, password, role, status) VALUES ('admin', 'admin', 0, 1);
INSERT INTO user (name, password, role, status) VALUES ('user', 'user', 1, 1);

INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('The Name of the Wind', 'Patrick Rothfuss', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ("The Wise Man\'s Fear", 'Patrick Rothfuss', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('A Game of Thrones', 'George R. R. Martin', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('A Clash of Kings', 'George R. R. Martin', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('A Storm of Swords', 'George R. R. Martin', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('A Feast for Crows', 'George R. R. Martin', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('A Dance with Dragons', 'George R. R. Martin', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('The Hobbit', 'J.R.R. Tolkien', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('The Fellowship of the Ring', 'J.R.R. Tolkien', 0, -1, NULL, 1, '');
INSERT INTO book (book_name, author, borrowed, borrower_id, last_borrowed, status, comments) VALUES ('The Two Towers', 'J.R.R. Tolkien', 0, -1, NULL, 1, '');


INSERT INTO record (user_id, book_id, borrowed_time, expected_return_time, actual_return_time) VALUES (2, 1, '2020-01-01', '2020-01-08', '2020-01-07');