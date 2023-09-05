import psycopg2


def create_database_tables():
    db_params = {
        'dbname': 'contracts_and_projects',
        'user': 'user',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

    conn = psycopg2.connect(**db_params)

    cursor = conn.cursor()

    create_table_contracts = """
    CREATE TABLE IF NOT EXISTS contracts (
        contract_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        creation_date DATE NOT NULL,
        sign_date DATE,
        status VARCHAR(20) DEFAULT 'черновик',
        project_id INT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );
    """

    create_table_projects = """
    CREATE TABLE IF NOT EXISTS projects (
        project_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        creation_date DATE NOT NULL
    );
    """

    cursor.execute(create_table_projects)
    cursor.execute(create_table_contracts)

    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database_tables()
