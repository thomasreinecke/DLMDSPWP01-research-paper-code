import pandas as pd  # pandas for data manipulation
import ssl  # ssl for handling SSL context

# Set the default SSL context to an unverified context to bypass SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# URL of the Wikipedia page containing the list of S&P 500 companies
link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"

# Read the HTML table from the Wikipedia page into a pandas DataFrame
df = pd.read_html(link, header=0)[0]

# Write the DataFrame to a CSV file without including the DataFrame's index
df.to_csv("data/sp500_constituents.csv", index=False)
