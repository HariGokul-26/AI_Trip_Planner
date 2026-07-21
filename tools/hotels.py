from langchain.tools import tool
import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/Indian_Hotels_Cleaned.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Fill missing feature values
feature_columns = [
    "Feature_1",
    "Feature_2",
    "Feature_3",
    "Feature_4",
    "Feature_5",
    "Feature_6",
    "Feature_7",
    "Feature_8",
    "Feature_9",
]

for col in feature_columns:
    df[col] = df[col].fillna("").astype(str)


@tool
def search_hotels(
    city: str,
    min_rating: float = 0,
    max_price: float = 999999,
    required_features: list[str] | None = None,
) -> str:
    """
    Search hotels by city, minimum rating, maximum price,
    and optional hotel features.
    """

    # -----------------------------
    # Normalize User Input
    # -----------------------------
    city = city.strip().title()

    # -----------------------------
    # Filter City
    # -----------------------------
    hotels = df[df["City"].str.title() == city]

    # -----------------------------
    # Filter Rating
    # -----------------------------
    hotels = hotels[hotels["Hotel_Rating"] >= min_rating]

    # -----------------------------
    # Filter Price
    # -----------------------------
    hotels = hotels[hotels["Hotel_Price"] <= max_price]

    # -----------------------------
    # Feature Filtering
    # -----------------------------
    if required_features:

        required_features = [
            feature.lower().strip()
            for feature in required_features
        ]

        # Merge all feature columns into one searchable string
        hotels = hotels.copy()

        hotels["All_Features"] = (
            hotels[feature_columns]
            .astype(str)
            .agg(" ".join, axis=1)
            .str.lower()
        )

        for feature in required_features:
            hotels = hotels[
                hotels["All_Features"].str.contains(
                    feature,
                    case=False,
                    na=False,
                )
            ]

    # -----------------------------
    # Sort Results
    # -----------------------------
    hotels = hotels.sort_values(
        by=["Hotel_Rating", "Hotel_Price"],
        ascending=[False, True],
    )

    # -----------------------------
    # Top 5
    # -----------------------------
    hotels = hotels.head(5)

    # -----------------------------
    # No Hotels
    # -----------------------------
    if hotels.empty:
        return "No hotels found matching your search."

    # -----------------------------
    # Format Results
    # -----------------------------
    results = []

    for _, hotel in hotels.iterrows():

        features = []

        for col in feature_columns:
            value = str(hotel[col]).strip()

            if value and value.lower() != "not available":
                features.append(value)

        hotel_info = f"""
Hotel Name : {hotel['Hotel_Name']}
City       : {hotel['City']}
Rating     : ⭐ {hotel['Hotel_Rating']}
Price      : ₹{hotel['Hotel_Price']}

Features:
{", ".join(features)}
"""

        results.append(hotel_info)

    return "\n" + ("\n" + "-" * 60 + "\n").join(results)