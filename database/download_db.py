import kagglehub
import pathlib
import shutil

# Dataset info
dataset_name = "terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database"
target_filename = "olist_ecommerce.sqlite"

# Ensure /database folder exists
db_folder = pathlib.Path("database")
db_folder.mkdir(exist_ok=True)

# Path to save inside /database folder
local_path = db_folder / target_filename

# Skip download if already present
if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    print("Downloading dataset from Kaggle...")
    dataset_path = kagglehub.dataset_download(dataset_name)
    print(f"Dataset downloaded to: {dataset_path}")

    # Find the .sqlite file in the downloaded dataset folder
    sqlite_files = list(pathlib.Path(dataset_path).rglob("*.sqlite"))

    if not sqlite_files:
        raise FileNotFoundError("No .sqlite file found in the downloaded dataset.")

    # Copy the first .sqlite file into /database folder
    shutil.copy(sqlite_files[0], local_path)
    print(f"File copied to {local_path}")

print("✅ Done!")
