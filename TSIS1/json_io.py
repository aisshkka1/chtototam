import json
from connect import get_connection


def export_to_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)

    rows = cur.fetchall()

    data = {}

    for r in rows:
        cid = r[0]

        if cid not in data:
            data[cid] = {
                "name": r[1],
                "email": r[2],
                "birthday": str(r[3]) if r[3] else None,
                "group": r[4],
                "phones": []
            }

        if r[5]:
            data[cid]["phones"].append({
                "phone": r[5],
                "type": r[6]
            })

    with open(filename, "w") as f:
        json.dump(list(data.values()), f, indent=4)

    print("Exported to JSON")


def import_from_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename) as f:
        data = json.load(f)

    for item in data:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, item["email"], item["birthday"]))

        cid = cur.fetchone()[0]

        if item.get("group"):
            cur.execute("CALL move_to_group(%s, %s)", (name, item["group"]))

        for phone in item.get("phones", []):
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, phone["phone"], phone["type"]))

    conn.commit()
    print("Imported from JSON")