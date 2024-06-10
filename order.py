import pandas as pd
import psycopg2

csv_file_path = 'DBfiles/order.csv'
df = pd.read_csv(csv_file_path)


def get_id_mapping(table_name, id_col, name_col, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {table_name}")
    records = cursor.fetchall()
    cursor.close()
    return {record[1]: record[0] for record in records}


try:
    connection = psycopg2.connect(
        dbname="CourseWork",
        user="postgres",
        password="root",
        host="localhost"
    )

    # Get product ID mappings
    product_mapping = get_id_mapping("Product", "ProductID", "ProductArticle", connection)

    # Get customer ID mappings
    user_mapping = get_id_mapping("Users", "UserID", "Email", connection)

    # Prepare the DataFrame with ID mappings
    df['ProductID'] = df['ProductArticle'].map(product_mapping)
    df['UserID'] = df['Email'].map(user_mapping)

    # Insert or update data in the necessary tables
    cursor = connection.cursor()
    for _, row in df.iterrows():
        # Insert or update sales_order
        cursor.execute("""
            INSERT INTO Cart (UserID, ProductID, Quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (UserID, ProductID) DO UPDATE SET
                Quantity = EXCLUDED.Quantity
        """, (row['UserID'], row['ProductID'], row['CartQuantity']))

        # Insert or update sales_line
        cursor.execute("""
            INSERT INTO "Order" (UserID, OrderDate, Status, ShippingAddress, BillingAddress, PaymentMethod)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (OrderID) DO UPDATE SET
                OrderDate = EXCLUDED.OrderDate,
                Status = EXCLUDED.Status,
                ShippingAddress = EXCLUDED.ShippingAddress,
                BillingAddress = EXCLUDED.BillingAddress,
                PaymentMethod = EXCLUDED.PaymentMethod
            RETURNING OrderID
        """, (row['UserID'], row['OrderDate'], row['Status'], row['ShippingAddress'], row['BillingAddress'], row['PaymentMethod']))

        order_id = cursor.fetchone()[0]

        # Insert inventory_transaction
        cursor.execute("""
            INSERT INTO Order_Item (OrderID, ProductID,Quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (OrderID, ProductID) DO UPDATE SET
                Quantity = EXCLUDED.Quantity
        """, (order_id, row['ProductID'], row['OrderQuantity']))


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
