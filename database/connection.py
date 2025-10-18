# from sqlalchemy import create_engine, text
# import pathlib

# # Correct relative path to your file
# db_path = pathlib.Path("database/olist_ecommerce.sqlite")

# engine = create_engine(f"sqlite:///{db_path}")

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
#     tables = [row[0] for row in result]
#     print("Tables in DB:", tables)


from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///database/olist_ecommerce.sqlite")

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM customers LIMIT 5;")}')
