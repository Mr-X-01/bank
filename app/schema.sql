DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS credit;
DROP TABLE IF EXISTS payment;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  inn TEXT,
  pdf_path TEXT,
  verification_status TEXT DEFAULT 'Не проверен'
);

CREATE TABLE credit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  date TEXT NOT NULL,
  status TEXT NOT NULL,
  bank TEXT NOT NULL,
  interest_rate REAL NOT NULL,
  term INTEGER NOT NULL,
  monthly_payment REAL NOT NULL,
  next_payment_date TEXT NOT NULL,
  remaining_amount REAL NOT NULL,
  overdue_amount REAL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE payment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  credit_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  date TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (credit_id) REFERENCES credit (id)
);
