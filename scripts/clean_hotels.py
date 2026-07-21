import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
print("Loading dataset...")

df = pd.read_csv("data/Indian_Hotels.csv")

print(f"Original Shape : {df.shape}")

# -----------------------------
# Clean Column Names
# -----------------------------
df.columns = df.columns.str.strip()

# -----------------------------
# Standardize City Names
# -----------------------------
df["City"] = (
    df["City"]
    .astype(str)
    .str.strip()
    .str.title()
)

# -----------------------------
# Remove Duplicate Rows
# -----------------------------
duplicate_rows = df.duplicated().sum()
print(f"Duplicate Rows : {duplicate_rows}")

df = df.drop_duplicates()

# -----------------------------
# Remove Duplicate Hotels
# Keep the highest-rated entry
# -----------------------------
df = (
    df.sort_values(
        by=["Hotel_Rating", "Hotel_Price"],
        ascending=[False, True]
    )
    .drop_duplicates(
        subset=["Hotel_Name", "City"],
        keep="first"
    )
)

# -----------------------------
# Handle Missing Values
# -----------------------------

# Replace missing hotel names
df["Hotel_Name"] = df["Hotel_Name"].fillna("Unknown Hotel")

# Replace missing ratings with 0
df["Hotel_Rating"] = df["Hotel_Rating"].fillna(0)

# Replace missing prices with median price
median_price = df["Hotel_Price"].median()

df["Hotel_Price"] = df["Hotel_Price"].fillna(median_price)

# Replace missing features
feature_columns = [
    "Feature_1",
    "Feature_2",
    "Feature_3",
    "Feature_4",
    "Feature_5",
    "Feature_6",
    "Feature_7",
    "Feature_8",
    "Feature_9"
]

for column in feature_columns:
    df[column] = df[column].fillna("Not Available")

# -----------------------------
# Remove Invalid Ratings
# -----------------------------
df = df[
    (df["Hotel_Rating"] >= 0) &
    (df["Hotel_Rating"] <= 5)
]

# -----------------------------
# Remove Invalid Prices
# -----------------------------
df = df[df["Hotel_Price"] > 0]

# -----------------------------
# Reset Index
# -----------------------------
df = df.reset_index(drop=True)

# -----------------------------
# Save Clean Dataset
# -----------------------------
output_path = "data/Indian_Hotels_Cleaned.csv"

df.to_csv(output_path, index=False)

print("\nCleaning Completed Successfully!")
print(f"Cleaned Shape : {df.shape}")
print(f"Saved File : {output_path}")

# -----------------------------
# Dataset Summary
# -----------------------------
print("\nDataset Summary")
print("-" * 40)

print(f"Total Hotels : {len(df)}")
print(f"Unique Cities : {df['City'].nunique()}")

print("\nTop 10 Cities")

print(df["City"].value_counts().head(10))

print("\nRating Statistics")

print(df["Hotel_Rating"].describe())

print("\nPrice Statistics")

print(df["Hotel_Price"].describe())