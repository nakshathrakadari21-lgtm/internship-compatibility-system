import sqlite3

def init_db():
    connection = sqlite3.connect('internships.db')
    cursor = connection.cursor()

    # Drop table if exists to start fresh
    cursor.execute('DROP TABLE IF EXISTS internships')

    # Create table
    cursor.execute('''
        CREATE TABLE internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            skills TEXT NOT NULL,
            min_cgpa REAL NOT NULL,
            domain TEXT NOT NULL
        )
    ''')

    # Dummy data
    internships_data = [
        ('Full Stack Developer', 'python,flask,javascript,sql,html', 7.5, 'Web Dev'),
        ('Data Analyst', 'python,sql,statistics,excel', 7.0, 'Data Science'),
        ('AI Research Intern', 'pytorch,tensorflow,calculus,python', 8.5, 'AI/ML')
    ]

    cursor.executemany('''
        INSERT INTO internships (role, skills, min_cgpa, domain)
        VALUES (?, ?, ?, ?)
    ''', internships_data)

    connection.commit()
    connection.close()
    print("Database initialized and populated with dummy data.")

if __name__ == '__main__':
    init_db()
