import json
from connect import get_connection


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    res = cur.fetchone()

    if res:
        gid = res[0]
    else:
        cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group,))
        gid = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO contacts(name,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, gid)
    )
    cid = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id,phone,type) VALUES (%s,%s,%s)",
        (cid, phone, ptype)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Added!")


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def search():
    q = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    g = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, p.phone
        FROM contacts c
        JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
        WHERE g.name=%s
    """, (g,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str, indent=4)

    print("Exported!")

    cur.close()
    conn.close()


def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for row in data:
        name, email, birthday, group, phone, ptype = row

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        if cur.fetchone():
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        g = cur.fetchone()
        if g:
            gid = g[0]
        else:
            cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group,))
            gid = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO contacts(name,email,birthday,group_id) VALUES (%s,%s,%s,%s) RETURNING id",
            (name, email, birthday, gid)
        )
        cid = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO phones(contact_id,phone,type) VALUES (%s,%s,%s)",
            (cid, phone, ptype)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Imported!")


def menu():
    while True:
        print("\n1.Add 2.Show 3.Search 4.Filter 5.Export 6.Import 0.Exit")
        c = input("Choose: ")

        if c == "1":
            add_contact()
        elif c == "2":
            show_contacts()
        elif c == "3":
            search()
        elif c == "4":
            filter_by_group()
        elif c == "5":
            export_json()
        elif c == "6":
            import_json()
        elif c == "0":
            break


menu()