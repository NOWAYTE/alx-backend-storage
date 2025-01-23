--decreases the quantity of an item afer adding a new order
CREATE TRIGGER decrement_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;

