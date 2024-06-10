import pandas as pd
import psycopg2

# Step 1: Extract - Read data from CSV file
csv_file_path = 'DBfiles/users.csv'
df = pd.read_csv(csv_file_path, dtype={
    'ProductArticle': str
})

def get_id_mapping(table_name, id_col, name_col, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {table_name}")
    records = cursor.fetchall()
    cursor.close()
    return {record[1]: record[0] for record in records}


try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname="CourseWork",
        user="postgres",
        password="root",
        host="localhost"
    )

    product_mapping = get_id_mapping("Product", "ProductID", "ProductArticle", connection)
    df['ProductID'] = df['ProductArticle'].map(product_mapping)

    # Step 2: Load - Insert or update data in the customer table
    cursor = connection.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Users (Username, Password, Email, FirstName, LastName)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (Email) DO UPDATE SET
                Username = EXCLUDED.Username,
                Password = EXCLUDED.Password,
                FirstName = EXCLUDED.FirstName,
                LastName = EXCLUDED.LastName
            RETURNING UserID
        """, (row['Username'], row['Password'], row['Email'], row['FirstName'], row['LastName']))
        user_id = cursor.fetchone()[0]

        if row['Wishlist'] == 'yes':
            cursor.execute("""
                INSERT INTO Wishlist (UserID, ProductID)
                VALUES (%s, %s)
                ON CONFLICT (UserID, ProductID) DO NOTHING
             """, (user_id, row['ProductID']))

    # Commit the transaction
    connection.commit()

except Exception as error:
    print(f"Error: {error}")
    if connection:
        connection.rollback()

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("Data import completed successfully.")
