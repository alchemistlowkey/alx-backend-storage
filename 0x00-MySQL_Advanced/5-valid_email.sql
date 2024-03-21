-- AN SQL script that creates a trigger that resets the attribute valid_email
-- only when the email has been changed.

-- Create a trigger to reset valid_email
DELIMITER $$

CREATE TRIGGER reset_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email attribute is being updated
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END $$

DELIMITER ;
