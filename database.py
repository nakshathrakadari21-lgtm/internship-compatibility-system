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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')


    # Dummy data
    internships_data = [
        ('Full Stack Developer', 'python,flask,javascript,sql,html', 7.5, 'Web Development'),
        ('Data Analyst', 'python,sql,statistics,excel', 7.0, 'Data Science'),
        ('AI Research Intern', 'pytorch,tensorflow,calculus,python', 8.5, 'AI/ML'),
        ('Backend Developer', 'java,spring boot,sql,api,python', 7.0, 'Backend Development'),
        ('DevOps Engineer', 'docker,kubernetes,jenkins,linux,bash', 7.5, 'DevOps'),
        ('Cloud Engineer', 'aws,azure,gcp,networking,linux', 7.5, 'Cloud Computing'),
        ('Cybersecurity Analyst', 'networks,linux,pentesting,python,security', 7.0, 'Cybersecurity'),
        ('Mobile App Developer', 'flutter,dart,react native,java,swift', 7.0, 'Mobile Development'),
        ('Software Tester', 'selenium,java,python,pytest,manual testing', 6.5, 'Software Testing'),
        ('Blockchain Developer', 'solidity,ethereum,smart contracts,rust', 8.0, 'Blockchain'),
        ('AI Engineer', 'python,tensorflow,pytorch,nlp,opencv', 8.0, 'AI/ML'),
        ('Data Engineer', 'sql,python,spark,hadoop,aws', 7.5, 'Data Science'),
        ('UI Developer', 'html,css,javascript,react,figma', 7.0, 'Web Development'),
        ('Machine Learning Engineer', 'python,scikit-learn,pandas,numpy,math', 8.0, 'AI/ML'),
        ('System Administrator', 'linux,windows server,networking,bash', 6.5, 'DevOps')
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
