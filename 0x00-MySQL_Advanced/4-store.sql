-- SQL script that creates a trigger that decreases the quantity of an item
-- after adding a new order.
-- Quantity in the table items can be negative.

-- Create the trigger
DELIMITER $$
CREATE TRIGGER after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Decrease the quantity of the ordered item in the table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END $$
DELIMITER ;
