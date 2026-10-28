-- ==========================================
-- VIDEO GAME SALES ANALYSIS
-- ==========================================

-- 1. Top 10 gaming platforms by global sales
-- Business Question:
-- Which platforms have the highest reported game sales?

SELECT
    platform,
    ROUND(SUM(global_sales), 2) AS total_sales
FROM video_game_sales
GROUP BY platform
ORDER BY total_sales DESC
LIMIT 10;


-- 2. Top 10 Nintendo-published games
-- Business Question:
-- Which Nintendo-published games sold the most?

SELECT
    name,
    platform,
    year,
    global_sales
FROM video_game_sales
WHERE publisher = 'Nintendo'
ORDER BY global_sales DESC
LIMIT 10;


-- 3. Nintendo sales by region
-- Business Question:
-- Which regions account for the most Nintendo game sales?

SELECT
    ROUND(SUM(na_sales), 2) AS north_america,
    ROUND(SUM(eu_sales), 2) AS europe,
    ROUND(SUM(jp_sales), 2) AS japan,
    ROUND(SUM(other_sales), 2) AS other_regions
FROM video_game_sales
WHERE publisher = 'Nintendo';


-- 4. Top 10 publishers by global sales
-- Business Question:
-- How does Nintendo compare with other publishers?

SELECT
    publisher,
    COUNT(*) AS total_games,
    ROUND(SUM(global_sales), 2) AS total_sales,
    ROUND(AVG(global_sales), 2) AS avg_sales_per_game
FROM video_game_sales
GROUP BY publisher
ORDER BY total_sales DESC
LIMIT 10;


-- 5. Nintendo's top games as a percentage of total sales
-- Business Question:
-- How much do individual blockbuster games contribute?

SELECT
    name,
    platform,
    global_sales,
    ROUND(
        100 * global_sales /
        (SELECT SUM(global_sales)
         FROM video_game_sales
         WHERE publisher = 'Nintendo'),
        2
    ) AS percent_of_nintendo_sales
FROM video_game_sales
WHERE publisher = 'Nintendo'
ORDER BY global_sales DESC
LIMIT 10;


-- 6. Nintendo sales by release year
-- Business Question:
-- How do Nintendo game sales vary by release year?

SELECT
    year,
    COUNT(*) AS total_games,
    ROUND(SUM(global_sales), 2) AS total_sales
FROM video_game_sales
WHERE publisher = 'Nintendo'
GROUP BY year
ORDER BY year;


-- 7. Nintendo's top 10 release years
-- Business Question:
-- Which release years produced the strongest game sales?

SELECT
    year,
    COUNT(*) AS total_games,
    ROUND(SUM(global_sales), 2) AS total_sales,
    ROUND(AVG(global_sales), 2) AS avg_sales_per_game
FROM video_game_sales
WHERE publisher = 'Nintendo'
GROUP BY year
ORDER BY total_sales DESC
LIMIT 10;