--ATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT ph.id, ph.name, ph.phone
    FROM phonebook ph
    WHERE ph.name ILIKE '%' || p || '%'
       OR ph.phone ILIKE '%' || p || '%';
END;
$$;


-- PAGINATION
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT ph.id, ph.name, ph.phone
    FROM phonebook ph
    LIMIT lim OFFSET offs;
END;
$$;
--берет текст и ищет в фонбуке 
--select frommen 