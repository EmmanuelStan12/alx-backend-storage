-- Average weighted score for all
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
compute_average:
BEGIN
  DECLARE total_weight FLOAT DEFAULT 0;
  DECLARE project_average FLOAT DEFAULT 0;
  DECLARE done INT DEFAULT FALSE;
  DECLARE user_id INT;

  DECLARE user_cursor CURSOR FOR SELECT id FROM users;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN user_cursor;

  user_loop:
  LOOP
    FETCH user_cursor INTO user_id;

    IF done THEN
      LEAVE user_loop;
    END IF;

    SET total_weight = 0;
    SET project_average = 0;

    SELECT SUM(p.weight) INTO total_weight FROM projects p INNER JOIN corrections c ON p.id = c.project_id WHERE c.user_id = user_id;
    IF total_weight > 0 THEN
      SELECT SUM(c.score * p.weight) INTO project_average FROM corrections c INNER JOIN projects p ON c.project_id = p.id WHERE c.user_id = user_id;
      SET project_average = project_average / total_weight;
    END IF;
    UPDATE users SET average_score = project_average WHERE id = user_id;
  END LOOP;

  CLOSE user_cursor;
END compute_average$$
DELIMITER ;
