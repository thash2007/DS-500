import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []

for page in range(1, 12):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Scraping page {page}")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all(
        "article",
        class_="product_pod"
    )

    print(f"Books found on page: {len(products)}")

    for book in products:

        title = book.h3.a["title"]

        price_tag = book.find(
            "p",
            class_="price_color"
        )

        if price_tag:
            price = price_tag.get_text(strip=True)
        else:
            price = ""

        rating = ""

        for p in book.find_all("p"):

            classes = p.get("class", [])

            if "star-rating" in classes:

                rating = classes[1]
                break

        availability = "In Stock"

        books.append([
            title,
            price,
            rating,
            availability
        ])

df = pd.DataFrame(
    books,
    columns=[
        "Title",
        "Price",
        "Rating",
        "Availability"
    ]
)

print("\nTOTAL BOOKS:", len(df))

print("\nFIRST 5 ROWS:")
print(df.head())

df.to_csv(
    "books_dataset.csv",
    index=False
)

print("\nCSV CREATED SUCCESSFULLY")