-- task 7: Average score
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
compute_average:
BEGIN
  DECLARE project_sum INT DEFAULT 0;
  DECLARE project_count INT DEFAULT 0;

  SELECT COUNT(*) INTO project_count FROM corrections c WHERE c.user_id = user_id;
  IF project_count > 0 THEN
    SELECT SUM(score) INTO project_sum FROM corrections c WHERE c.user_id = user_id;
  END IF;
  UPDATE users SET average_score = IF(project_count = 0, 0, project_sum / project_count) WHERE id = user_id;
END compute_average$$
DELIMITER ;
