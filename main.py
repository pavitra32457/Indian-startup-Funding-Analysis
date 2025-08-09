pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/content/startup_funding.csv')
# Display first 5 rows
display(df.head())

# Display DataFrame info (columns, data types, missing values)
display(df.info())


# Drop the 'Remarks' column due to a high number of missing values
df = df.drop('Remarks', axis=1, errors='ignore')

# Handle missing values in 'Industry Vertical', 'SubVertical', 'City Location',
# 'Investors Name', and 'InvestmentInType' by filling with 'Unknown'
for col in ['Industry Vertical', 'SubVertical', 'City  Location', 'Investors Name', 'InvestmentnType']:
    df[col].fillna("Unknown", inplace=True)

# Clean 'Amount in USD': remove commas and '+' signs, convert to numeric, fill missing values with 0
df['Amount in USD'] = df['Amount in USD'].astype(str).str.replace(',', '', regex=False).str.replace('+', '', regex=False)
df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')
df['Amount in USD'].fillna(0, inplace=True)

# Clean 'Date dd/mm/yyyy': convert to datetime objects, handle potential errors
df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'], format='%d/%m/%Y', errors='coerce')

# Handle inconsistent formats in 'Startup Name', 'Industry Vertical', 'SubVertical', 'City Location',
# 'Investors Name', and 'InvestmentInType'
for col in ['Startup Name', 'Industry Vertical', 'SubVertical', 'City  Location', 'Investors Name', 'InvestmentnType']:
    df[col] = df[col].astype(str).str.strip().str.replace(r'[\xa0\u200b]', '', regex=True)  # Remove non-breaking spaces
    df[col] = df[col].apply(lambda x: ' '.join(x.split()))  # Remove multiple spaces
    df[col] = df[col].str.lower()  # Convert to lowercase for consistency


# Clean 'Amount in USD': remove commas and '$' signs, convert to numeric, fill missing values with 0
df['Amount in USD'] = df['Amount in USD'].astype(str).str.replace(',', '', regex=False).str.replace('$', '', regex=False)
df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')
df['Amount in USD'].fillna(0, inplace=True)

# Clean 'Date dd/mm/yyyy': convert to datetime objects, handle potential errors
df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'], format='%d/%m/%Y', errors='coerce')

# Handle inconsistent formats in string columns
for col in ['Startup Name', 'Industry Vertical', 'SubVertical', 'City  Location', 'Investors Name', 'InvestmentnType']:
    df[col] = df[col].astype(str).str.strip().str.replace(r'\xa0', '', regex=True)  # Remove non-breaking spaces and trim
    df[col] = df[col].apply(lambda x: ' '.join(x.split()))  # Handle multiple spaces
    df[col] = df[col].str.lower()  # Convert to lowercase for consistency

# Display the cleaned DataFrame info and first 5 rows
display(df.info())
display(df.head())


# Ensure the Date column is in datetime format
df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'], dayfirst=True)

# Extract year and month
df['FundingYear'] = df['Date dd/mm/yyyy'].dt.year
df['FundingMonth'] = df['Date dd/mm/yyyy'].dt.month

# Group and aggregate
yearly_funding_trends = df.groupby('FundingYear').agg(
    total_funding_usd=('Amount in USD', 'sum'),
    number_of_deals=('Sr No', 'count')
).reset_index()

# Display result
display(yearly_funding_trends)

monthly_funding_trends = df.groupby('FundingMonth').agg(
    total_funding_usd=('Amount in USD', 'sum'),
    number_of_deals=('Sr No', 'count')
).reset_index()

display(monthly_funding_trends)

# Group by Industry Vertical and sum the funding amount
sector_funding = df.groupby('Industry Vertical')['Amount in USD'].sum().reset_index()
sector_funding = sector_funding.sort_values(by='Amount in USD', ascending=False)
print("Top 10 Sectors by Funding:")
display(sector_funding.head(10))

# Group by City Location and sum the funding amount
city_funding = df.groupby('City  Location')['Amount in USD'].sum().reset_index()
city_funding = city_funding.sort_values(by='Amount in USD', ascending=False)
print("\nTop 10 Cities by Funding:")
display(city_funding.head(10))

# Analyze active investors and store the result in investor_activity
investor_activity = active_investors(df, top_n=10)

# Top 10 investors by total funding
top_investors_by_funding = investor_activity.sort_values(
    by='sum',  # Use 'sum' as the column name from the active_investors function
    ascending=False
)
print("Top 10 Investors by Total Funding:")
display(top_investors_by_funding.head(10))

# Top 10 investors by number of deals
top_investors_by_deals = investor_activity.sort_values(
    by='count', # Use 'count' as the column name from the active_investors function
    ascending=False
)
print("\nTop 10 Investors by Number of Deals:")
display(top_investors_by_deals.head(10))

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Yearly Funding Trends
plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_funding_trends, x='FundingYear', y='total_funding_usd',
             marker='o', label='Total Funding (USD)')
sns.lineplot(data=yearly_funding_trends, x='FundingYear', y='number_of_deals',
             marker='o', label='Number of Deals')
plt.title('Yearly Funding Trends')
plt.xlabel('Year')
plt.ylabel('Amount / Count')
plt.xticks(yearly_funding_trends['FundingYear'])
plt.grid(True)
plt.legend()
plt.show()

# 2. Top 10 Sectors by Funding
plt.figure(figsize=(14, 7))
sns.barplot(data=sector_funding.head(10), x='Industry Vertical', y='Amount in USD', palette='viridis')
plt.title('Top 10 Sectors by Total Funding')
plt.xlabel('Industry Vertical')
plt.ylabel('Total Funding (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3. Top 10 Cities by Funding
plt.figure(figsize=(14, 7))
sns.barplot(data=city_funding.head(10), x='City  Location', y='Amount in USD', palette='viridis')
plt.title('Top 10 Cities by Total Funding')
plt.xlabel('City Location')
plt.ylabel('Total Funding (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Calculate top 10 startups by total funding
top_startups = top_entities(df, CONFIG["company_col"], by_amount=True, top_n=10)

# Convert the top_startups Series to a DataFrame for plotting
top_startups_df = top_startups.reset_index()
top_startups_df.columns = ['Startup Name', 'Total Funding (USD)']

# Top 10 Startups by Total Funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_startups_df.head(10), # Use the DataFrame
    x='Total Funding (USD)', # Use the column name in the DataFrame for x-axis
    y='Startup Name', # Use the column name in the DataFrame for y-axis
    palette='viridis'
)
plt.title("Top 10 Startups by Total Funding")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Startup Name")
plt.tight_layout()
plt.show()

# Top 10 Investors by Total Funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_investors_by_funding.head(10),
    x='sum', # Use 'sum' column for funding amount
    y=top_investors_by_funding.head(10).index, # Use index for investor name
    palette='viridis'
)
plt.title("Top 10 Investors by Total Funding")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Investor Name")
plt.tight_layout()
plt.show()

# Top 10 Investors by Number of Deals
plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_investors_by_deals.head(10),
    x='count', # Use 'count' column for number of deals
    y=top_investors_by_deals.head(10).index, # Use index for investor name
    palette='viridis'
)
plt.title("Top 10 Investors by Number of Deals")
plt.xlabel("Number of Deals")
plt.ylabel("Investor Name")
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# Calculate total funding and number of deals by Investment Type
investment_type_summary = df.groupby(CONFIG["investment_type_col"]).agg(
    total_funding_usd=('Amount in USD', 'sum'),
    number_of_deals=('Sr No', 'count') # Assuming 'Sr No' can be used as a deal counter
).reset_index()

# Sort by total funding for plotting
investment_type_summary_by_funding = investment_type_summary.sort_values(by='total_funding_usd', ascending=False)

# Sort by number of deals for plotting
investment_type_summary_by_deals = investment_type_summary.sort_values(by='number_of_deals', ascending=False)


# 7. Top 10 Investment Types by Funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=investment_type_summary_by_funding.head(10),
    x=CONFIG["investment_type_col"], # Use the correct column name from the DataFrame
    y='total_funding_usd',
    palette='viridis'
)
plt.title('Top 10 Investment Types by Total Funding')
plt.xlabel('Investment Type')
plt.ylabel('Total Funding (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 8. Top 10 Investment Types by Deals
plt.figure(figsize=(14, 7))
sns.barplot(
    data=investment_type_summary_by_deals.head(10),
    x=CONFIG["investment_type_col"], # Use the correct column name from the DataFrame
    y='number_of_deals',
    palette='viridis'
)
plt.title('Top 10 Investment Types by Number of Deals')
plt.xlabel('Investment Type')
plt.ylabel('Number of Deals')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Example: top 10 investment types by total funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=investment_type_summary_by_funding.head(10),
    x="InvestmentnType",
    y="total_funding_usd",
    palette="viridis"
)
plt.title("Top 10 Investment Types by Total Funding (USD)")
plt.xlabel("Investment Type")
plt.ylabel("Total Funding (USD)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# Example: top 10 investment types by number of deals
plt.figure(figsize=(14, 7))
sns.barplot(
    data=investment_type_summary_by_deals.head(10),
    x="InvestmentnType",
    y="number_of_deals",
    palette="viridis"
)
plt.title("Top 10 Investment Types by Number of Deals")
plt.xlabel("Investment Type")
plt.ylabel("Number of Deals")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# Ensure city_funding, top_startups_df, and top_investors_by_funding are available from previous cells
# city_funding is generated in cell 9wMUq-ieQ7fH
# top_startups_df and top_investors_by_funding are generated/used in cell SCmKQuw9S9Z0


# 3. Top 10 Cities by Funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=city_funding.head(10),
    x='City  Location', # Corrected column name
    y='Amount in USD',
    palette='viridis'
)
plt.title('Top 10 Cities by Total Funding')
plt.xlabel('City Location')
plt.ylabel('Total Funding (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 4. Top 10 Startups by Funding
# Using the top_startups_df DataFrame created in a previous step (e.g., cell SCmKQuw9S9Z0)
# If top_startups_df is not available, you might need to recreate it:
# top_startups = top_entities(df, CONFIG["company_col"], by_amount=True, top_n=10)
# top_startups_df = top_startups.reset_index()
# top_startups_df.columns = ['Startup Name', 'Total Funding (USD)']

plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_startups_df.head(10), # Using top_startups_df
    x='Total Funding (USD)', # Corrected column name
    y='Startup Name', # Corrected column name
    palette='viridis'
)
plt.title('Top 10 Startups by Total Funding')
plt.xlabel('Total Funding (USD)') # Corrected label
plt.ylabel('Startup Name') # Corrected label
plt.xticks(rotation=45, ha='right') # Keep rotation if needed
plt.tight_layout()
plt.show()

# 5. Top 10 Investors by Funding
# Using the top_investors_by_funding DataFrame created in a previous step (e.g., cell SCmKQuw9S9Z0)
plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_investors_by_funding.head(10),
    x='sum', # Corrected: use 'sum' column for funding amount
    y=top_investors_by_funding.head(10).index, # Corrected: use index for investor name
    palette='viridis'
)
plt.title('Top 10 Investors by Total Funding')
plt.xlabel('Total Funding (USD)') # Corrected label
plt.ylabel('Investor Name') # Corrected label
plt.xticks(rotation=45, ha='right') # Keep rotation if needed
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# 6. Top 10 Investors by Deals
plt.figure(figsize=(14, 7))
sns.barplot(
    data=top_investors_by_deals.head(10),
    x='count',   # Corrected: use 'count' column for number of deals
    y=top_investors_by_deals.head(10).index, # Corrected: use index for investor name
    palette='viridis'
)
plt.title('Top 10 Investors by Number of Deals')
plt.xlabel('Number of Deals') # Corrected label
plt.ylabel('Investor Name') # Corrected label
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 7. Top 10 Investment Types by Funding
plt.figure(figsize=(14, 7))
sns.barplot(
    data=investment_type_summary_by_funding.head(10),
    x='InvestmentnType',   # Corrected: use 'InvestmentnType' column
    y='total_funding_usd',
    palette='viridis'
)
plt.title('Top 10 Investment Types by Total Funding')
plt.xlabel('Investment Type')
plt.ylabel('Total Funding (USD)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Group by InvestmentType and calculate total funding & number of deals
investment_type_summary = df.groupby('InvestmentnType').agg(
    total_funding_usd=('Amount in USD', 'sum'),
    number_of_deals=('Sr No', 'count')
).reset_index()

# Sort by total funding
investment_type_summary_by_funding = investment_type_summary.sort_values(
    by='total_funding_usd', ascending=False
)
print("Investment Types by Total Funding:")
display(investment_type_summary_by_funding)

# Sort by number of deals
investment_type_summary_by_deals = investment_type_summary.sort_values(
    by='number_of_deals', ascending=False
)
print("\nInvestment Types by Number of Deals:")
display(investment_type_summary_by_deals)


import matplotlib.pyplot as plt
import seaborn as sns

# Example: yearly_funding_trends should be a DataFrame with columns:
# 'FundingYear', 'total_funding_usd', 'number_of_deals'

plt.figure(figsize=(12, 6))

# Plot total funding
sns.lineplot(
    data=yearly_funding_trends,
    x='FundingYear',
    y='total_funding_usd',
    marker='o',
    label='Total Funding (USD)'
)

# Plot number of deals
sns.lineplot(
    data=yearly_funding_trends,
    x='FundingYear',
    y='number_of_deals',
    marker='o',
    label='Number of Deals'
)

plt.title('Yearly Funding Trends')
plt.xlabel('Year')
plt.ylabel('Amount / Count')
plt.xticks(yearly_funding_trends['FundingYear'], rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Group by investor name and calculate total funding and number of deals
investor_activity = df.groupby('Investors Name').agg(
    total_funding_usd=('Amount in USD', 'sum'),
    number_of_deals=('Sr No', 'count')
).reset_index()

# Sort by total funding in descending order
top_investors_by_funding = investor_activity.sort_values(
    by='total_funding_usd', ascending=False
)

print("Top 10 Investors by Total Funding")
display(top_investors_by_funding.head(10))

# Sort by number of deals in descending order
top_investors_by_deals = investor_activity.sort_values(
    by='number_of_deals', ascending=False
)

print("\nTop 10 Investors by Number of Deals")
display(top_investors_by_deals.head(10))


# Group by Industry Vertical and sum the funding amount
sector_funding = (
    df.groupby('Industry Vertical', as_index=False)['Amount in USD']
    .sum()
    .sort_values(by='Amount in USD', ascending=False)
)
print("Top 10 Sectors by Funding:")
display(sector_funding.head(10))

# Group by City Location and sum the funding amount
city_funding = (
    df.groupby('City  Location', as_index=False)['Amount in USD']
    .sum()
    .sort_values(by='Amount in USD', ascending=False)
)
print("\nTop 10 Cities by Funding:")
display(city_funding.head(10))

# Group by Startup Name and sum the funding amount
startup_funding = (
    df.groupby('Startup Name', as_index=False)['Amount in USD']
    .sum()
    .sort_values(by='Amount in USD', ascending=False)
)
print("\nTop 10 Startups by Funding:")
display(startup_funding.head(10)) 