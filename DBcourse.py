import traceback

import pandas as pd
import psycopg2

# Step 1: Extract - Read data from CSV file
csv_file_path = 'DBfiles/User.csv'
df = pd.read_csv(csv_file_path)

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname="CourseWork",
        user="postgres",
        password="root",
        host="localhost"
    )

    # Step 2: Load - Insert or update data in the customer table
    cursor = connection.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO User (User, Password, Email, FirstName, LastName)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (Email) DO UPDATE SET
                User = EXCLUDED.User,
                Password = EXCLUDED.Password,
                FirstName = EXCLUDED.FirstName,
                LastName = EXCLUDED.LastName,
        """, (row['User'], row['Password'], row['Email'], row['FirstName'], row['LastName'], ))

    # Commit the transaction
    connection.commit()

except Exception as error:
    print(f"Error: {error}")
    print("Detailed traceback:")
    traceback.print_exc()  # This prints the complete traceback to the console
    if connection:
        connection.rollback()

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("Data import completed successfully.")
