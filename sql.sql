/*CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer',  -- viewer, analyst, admin
    created_at TIMESTAMP DEFAULT NOW()
);
*/

/*
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(12, 2) NOT NULL,
    type VARCHAR(10) NOT NULL,        -- 'income' or 'expense'
    category VARCHAR(100) NOT NULL,   -- e.g. food, salary, rent
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);*/

CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    limit_amount DECIMAL(12, 2) NOT NULL,
    month INTEGER NOT NULL,   -- 1-12
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);