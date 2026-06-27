CREATE TABLE nav_history (
    amfi_code INTEGER,
    date DATE,
    nav REAL
);

CREATE TABLE transactions (
    transaction_id INTEGER,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount REAL,
    state TEXT,
    kyc_status TEXT,
    transaction_date DATE
);

CREATE TABLE performance (
    amfi_code INTEGER,
    scheme_name TEXT,
    category TEXT,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL
);