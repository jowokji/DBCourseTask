import pandas as pd
import psycopg2

# Step 1: Extract - Read data from CSV file
csv_file_path = 'DBfiles/product.csv'
df = pd.read_csv(csv_file_path)


# Step 2: Transform - (Mapping category_name and pet_type_name to their respective IDs)
def get_id_mapping(table_name, id_col, name_col, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {table_name}")
    records = cursor.fetchall()
    cursor.close()
    return {record[1]: record[0] for record in records}


def upsert_category_and_brand(df, connection):
    cursor = connection.cursor()

    # Upsert categories
    for category in df['CategoryName'].unique():
        cursor.execute("""
            INSERT INTO Category (Name) VALUES (%s)
            ON CONFLICT (Name) DO NOTHING
        """, (category,))

    # Upsert brands
    for brand in df['BrandName'].unique():
        cursor.execute("""
            INSERT INTO Brand (Name) VALUES (%s)
            ON CONFLICT (Name) DO NOTHING
        """, (brand,))

    connection.commit()
    cursor.close()


try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        dbname="CourseWork",
        user="postgres",
        password="root",
        host="localhost"
    )

    # Step 2.1: Upsert category and pet type data
    upsert_category_and_brand(df, connection)

    # Step 2.2: Get category and pet type ID mappings
    category_mapping = get_id_mapping("Category", "CategoryID", "Name", connection)
    brand_mapping = get_id_mapping("Brand", "BrandID", "Name", connection)

    # Prepare the DataFrame with ID mappings
    df['CategoryID'] = df['CategoryName'].map(category_mapping)
    df['BrandID'] = df['BrandName'].map(brand_mapping)

    # Step 3: Load - Insert or update data in the product table
    cursor = connection.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Product (Name, Price, BrandID, CategoryID, Material, Condition, ProductArticle)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ProductArticle) DO UPDATE SET
                Name = EXCLUDED.Name,
                Price = EXCLUDED.Price,
                CategoryID = EXCLUDED.CategoryID,
                BrandID = EXCLUDED.BrandID,
                Material = EXCLUDED.Material,
                Condition = EXCLUDED.Condition
        """, (row['Name'], row['Price'], row['BrandID'], row['CategoryID'], row['Material'], row['Condition'], row['ProductArticle']))

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
