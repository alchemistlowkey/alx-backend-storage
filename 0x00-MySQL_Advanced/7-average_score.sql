-- An SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- Note: An average score can be a decimal
-- Requirements:
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value
-- (you can assume user_id is linked to an existing users)

-- Create a stored procedure ComputeAverageScoreForUser
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Compute total score and total projects for the user
    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO total_score, total_projects
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Update the average score for the user
    UPDATE users
    SET users.average_score = IF(total_projects > 0,
				 total_score / total_projects, 0)
    WHERE users.id = user_id;
END $$

DELIMITER ;
