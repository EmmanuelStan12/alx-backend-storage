-- Average weighted score
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
compute_average:
BEGIN
  DECLARE total_weight FLOAT DEFAULT 0;
  DECLARE project_average FLOAT DEFAULT 0;
  SELECT SUM(p.weight) INTO total_weight FROM projects p INNER JOIN corrections c ON p.id = c.project_id WHERE c.user_id = user_id;
  IF total_weight > 0 THEN
    SELECT SUM(c.score * p.weight) INTO project_average FROM corrections c INNER JOIN projects p ON c.project_id = p.id WHERE c.user_id = user_id;
    SET project_average = project_average / total_weight;
  END IF;
  UPDATE users SET average_score = project_average WHERE id = user_id;
END compute_average$$
DELIMITER ;
