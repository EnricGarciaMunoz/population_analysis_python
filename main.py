import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# DATA CLEANING

# Get CSV files from the 'sources' directory
file_paths = glob.glob('sources/*.csv')

# List to store each years DataFrame
df_list = []

# Read and load each CSV file in a DataFrame
for file in file_paths:
    df = pd.read_csv(file)
    df_list.append(df[['Data_Referencia', 'Nom_Districte', 'Nom_Barri', 'Seccio_Censal', 'Valor']])

# Comine all the DataFrames in one
combined_df = pd.concat(df_list, ignore_index=True)

# Rename the columns
combined_df.columns = ['Date', 'District_Name', 'Neighborhood_Name', 'Sensus_Area', 'Population']

# Exploratory Analysis
print("\nFirst DataFrame rows:")
print(combined_df.head())
print("Numeric Type Data description:")
print(combined_df.describe())

# NULL Values counting
null_values_count = combined_df.isnull().sum().sum()
print(f"Total NULL values: {null_values_count}")
# Even we don't have NULL values, we'll delete them, just in case we add new data in the future.
cleaned_df = combined_df.dropna()

# Duplicate rows counting
duplicated_rows_count = combined_df.duplicated().sum()
print(f"Total duplicate rows: {duplicated_rows_count}")
# Even we don't have duplicate rows, we'll delete them, just in case we add new data in the future.
combined_df = combined_df.drop_duplicates()

# Data Types
data_types = combined_df.dtypes
print("Tipos de datos de cada columna en el DataFrame:")
print(data_types)
# Date data is an 'object' type. We'll change it into a datetime tyme ('datetime64[ns])
combined_df['Date'] = pd.to_datetime(combined_df['Date'])
data_types = combined_df.dtypes
print("Tipos de datos de cada columna en el DataFrame:")
print(data_types)

# Save the DataFrame after cleaning the Data (we'll use it to make analysis and a Power BI report)
cleaned_df.to_csv('data_cleaning/cleaned_population_data.csv', index=False)

print("All data combined and cleaned properly. Stored in 'datacleaning/cleaned_population_data.csv'.")


# DATA ANALYSIS
import matplotlib.pyplot as plt
import seaborn as sns


### DONAR DADES NUMÉRIQUES ABANS DE COMENÇAR AMB ELS GRÁFICS


# 2024 population analysis
def population_analysis_2024(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df_2024 = df[df['Date'] == '2024-01-01']
    
    # District Population in 2024
    district_population_mean = df_2024.groupby('District_Name')['Population'].sum().sort_values(ascending=False)
    district_population_mean.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Population per District in 2024')
    plt.xlabel('District')
    plt.ylabel('Population')
    plt.savefig('analysis_results/district_population_2024.png')
    plt.grid(axis='y')
    plt.show()
    
    # Neigborhood Population in 2024
    neighborhood_population_mean = df_2024.groupby('Neighborhood_Name')['Population'].sum().sort_values(ascending=False)
    neighborhood_population_mean.plot(kind='bar', figsize=(15, 9))
    plt.title('Population per Neighorhood in 2024')
    plt.xlabel('Neighorhood')
    plt.ylabel('Population')
    plt.savefig('analysis_results/neighborhood_population_2024.png')
    plt.grid(axis='y')
    plt.show()
    
    # District and Neighborhood Population in 2024
    district_population_mean = df_2024.groupby(['District_Name', 'Neighborhood_Name'])['Population'].sum().unstack().fillna(0) # SI HE ELIMINAT ELS NULLS, NO HAURIA DE CALER AQUEST PAS
    district_population_mean.plot(kind='bar', stacked=True, figsize=(15, 9))
    plt.title('District and Neighborhood Population in 2024')
    plt.xlabel('District')
    plt.ylabel('Population')
    plt.legend(title='Neighborhood', prop={'size': 4})
    plt.savefig('analysis_results/district_neighborhood_population_2024.png')
    plt.grid(axis='y')
    plt.show()

def population_evolution_analysis(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df_2024 = df[df['Date'] == '2024-01-01']

    # Population evolution over time in Barcelona
    population_growth = df.groupby('Date')['Population'].sum()
    population_growth.plot(figsize=(10, 6), linewidth=2, marker='o')
    plt.title('Population evolution over time in Barcelona')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.savefig('analysis_results/population_growth.png')
    plt.grid(axis='y')
    plt.show()

    # Population evolution over time per District in Barcelona
    population_growth = df.groupby(['Date', 'District_Name'])['Population'].sum().unstack().fillna(0)
    population_growth.plot(figsize=(15, 9), linewidth=2, marker='o')
    plt.title('Population evolution over time per District in Barcelona')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.legend(title='District')
    plt.savefig('analysis_results/population_growth_per_district.png')
    plt.grid(axis='y')
    plt.show()

def population_comparison_2015_2024(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df_2015 = df[df['Date'] == '2015-01-01']
    df_2024 = df[df['Date'] == '2024-01-01']

    # Population per District 2015 vs. 2024
    population_2015 = df_2015.groupby('District_Name')['Population'].sum()
    population_2024 = df_2024.groupby('District_Name')['Population'].sum()
    
    comparison_df = pd.DataFrame({
        '2015': population_2015,
        '2024': population_2024
    }).reset_index()
    
    comparison_df = comparison_df.melt(id_vars='District_Name', var_name='Year', value_name='Population')
    
    plt.figure(figsize=(15, 9))
    sns.barplot(data=comparison_df, x='District_Name', y='Population', hue='Year')
    plt.title('Population per District 2015 vs. 2024')
    plt.xlabel('District')
    plt.ylabel('Population')
    plt.xticks(rotation=45)
    plt.savefig('analysis_results/2024-2015_population_comparison_per_district.png')
    plt.grid(axis='y')
    plt.show()

    # 2024/2015 population ratio per District
    ratio_population = population_2024 / population_2015
    ratio_population_sorted = ratio_population.sort_values(ascending=False)
    print("2024/2015 population ratio per District:")
    print(ratio_population_sorted)

    # 2024/2015 Population Ratio per District
    plt.figure(figsize=(12, 8))
    sns.barplot(x=ratio_population_sorted.index, y=ratio_population_sorted.values, order=ratio_population_sorted.index)
    plt.title('2024/2015 Population Ratio per District')
    plt.xlabel('District')
    plt.ylabel('Ratio')
    plt.xticks(rotation=45)
    plt.ylim(0.8, None)
    plt.savefig('analysis_results/2024-2015_population_ratio_per_district.png')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


population_analysis_2024(cleaned_df)
population_evolution_analysis(cleaned_df)
population_comparison_2015_2024(cleaned_df)