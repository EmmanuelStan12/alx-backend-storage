-- Task 2: Number of fans
SELECT origin, SUM(mb.fans) AS nb_fans FROM metal_bands mb GROUP BY origin ORDER BY nb_fans DESC;
