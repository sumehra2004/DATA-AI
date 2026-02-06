import pandas as pd

data = {
    "Movie": ["Aa Aa", "RRR", "Khushi", "Darling", "OW", "Sanam Teri Kasam"],
    "Genre": ["Romance", "Action", "Romance", "Romantic Comedy", "Musical", "Romance"],
    "Rating": [4.2,4.1,3.5,3.8,4.3,4.9]
}
df = pd.DataFrame(data)
print("Movie Dataset")
print(df)
print("\nAverage Rating:", df["Rating"].mean())
