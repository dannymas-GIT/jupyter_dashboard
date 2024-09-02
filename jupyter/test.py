import pandas as pd
import matplotlib.pyplot as plt

try:
    # Load the CSV file
    df = pd.read_csv('MOCK_DATA.csv', delimiter=',', quotechar='"')
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
    exit(1)

# Display the first few rows of the DataFrame
print(df.head())

# Basic summary statistics
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Example: Filter data for a specific job title
job_title = 'Web Designer II'
filtered_df = df[df['Job Title'].str.strip() == job_title]
print(filtered_df)

# Example: Group by year and count occurrences
yearly_counts = df.groupby('Year').size()
print(yearly_counts)

# Plot the yearly counts
yearly_counts.plot(kind='bar')
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Yearly Job Counts')
plt.show()
