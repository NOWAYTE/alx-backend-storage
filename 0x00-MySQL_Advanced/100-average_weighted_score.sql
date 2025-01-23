-- average weighted score

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE weighted_avg_score DECIMAL(10, 2);
    DECLARE total_weights INT;

    -- Compute the total weights for the user
    SELECT SUM(weight) INTO total_weights
    FROM corrections
    WHERE user_id = user_id;

    -- Compute the weighted average score for the user
    SELECT SUM(score * weight) / total_weights INTO weighted_avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average weighted score in the users table
    UPDATE users
    SET average_weighted_score = weighted_avg_score
    WHERE id = user_id;
END$$

DELIMITER ;

