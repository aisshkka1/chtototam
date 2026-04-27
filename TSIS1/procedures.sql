-- ADD PHONE
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;

    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found';
    ELSE
        INSERT INTO phones(contact_id, phone, type)
        VALUES (cid, p_phone, p_type);
    END IF;
END;
$$;


-- MOVE TO GROUP
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name)
        RETURNING id INTO gid;
    END IF;

    UPDATE contacts
    SET group_id = gid
    WHERE name = p_contact_name;
END;
$$;


-- SEARCH EVERYTHING
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_name VARCHAR,
    contact_email VARCHAR,
    phone_number VARCHAR,
    group_name VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name, 
        c.email, 
        p.phone, 
        g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%';
END;
$$;

-- PAGINATION FOR TSIS 1
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    group_name VARCHAR
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name, 
        c.email, 
        p.phone, 
        g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit 
    OFFSET p_offset;
END;
$$;