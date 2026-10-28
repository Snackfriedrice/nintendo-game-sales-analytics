-- Create the video game sales table
-- Source: cleaned video game sales CSV

CREATE TABLE IF NOT EXISTS video_game_sales (
    rank INTEGER,
    name TEXT,
    platform TEXT,
    year INTEGER,
    genre TEXT,
    publisher TEXT,
    na_sales NUMERIC(10,2),
    eu_sales NUMERIC(10,2),
    jp_sales NUMERIC(10,2),
    other_sales NUMERIC(10,2),
    global_sales NUMERIC(10,2)
);