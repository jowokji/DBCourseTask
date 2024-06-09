import pandas as pd
import psycopg2
import traceback

# Read the CSV file into a DataFrame
csv_file_path = 'DBfiles/Product.csv'
df = pd.read_csv(csv_file_path)

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname="CourseWork",
        user="postgres",
        password="root",
        host="localhost"
    )

    # Load - Insert or update data in the Product table
    cursor = connection.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Product (ProductID, Name, Description, Price, StockLevel, BrandID, CategoryID, Material, Condition, YearReleased)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ProductID) DO UPDATE SET
                Name = EXCLUDED.Name,
                Description = EXCLUDED.Description,
                Price = EXCLUDED.Price,
                StockLevel = EXCLUDED.StockLevel,
                BrandID = EXCLUDED.BrandID,
                CategoryID = EXCLUDED.CategoryID,
                Material = EXCLUDED.Material,
                Condition = EXCLUDED.Condition,
                YearReleased = EXCLUDED.YearReleased
        """, (row['ProductID'], row['Name'], row['Description'], row['Price'], row['StockLevel'],
              row['BrandID'], row['CategoryID'], row['Material'], row['Condition'], row['YearReleased']))

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
