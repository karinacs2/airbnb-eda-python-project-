import pandas as pd
import matplotlib.pyplot as plt
CSV_FILEPATH = '/Users/maiconlucinda/Documents/higherdiploma/Python/Projects/projeto_final/data/airbnb_listings.csv'

# Get data
def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {filepath} was not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {filepath} is empty.")
        exit(1)
    except pd.errors.ParserError:
        print(f"Error: The file at {filepath} could not be parsed.")
        exit(1)

# Check if the column exists
def validate_columns(data, required_columns):
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Error: The following columns are missing from the dataset: {', '.join(missing_columns)}")
        exit(1)

# Top 10 rated Airbnbs for at least 8 nights and instantly bookable
def top_10_airbnbs(data):
    required_columns = ['minimum_nights', 'instant_bookable', 'review_scores_rating']
    validate_columns(data, required_columns)
    
    filtered_data = data[(data['minimum_nights'] <= 8) & (data['instant_bookable'] == 't')]
    sorted_data = filtered_data.sort_values(by='review_scores_rating', ascending=False)
    return sorted_data.head(10)

# Distribution of host response rates in a pie chart
def plot_response_rate_distribution(data):
    required_columns = ['host_response_rate']
    validate_columns(data, required_columns)
    
    response_rates = data['host_response_rate'].dropna()
    response_rates = response_rates.str.rstrip('%').astype('float') / 100.0
    response_rates.value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Host Response Rates Distribution')
    plt.show()

# Count of Airbnbs in a neighborhood with cleanliness rating > 4.0
def count_clean_airbnbs(data, neighborhood):
    required_columns = ['neighbourhood_cleansed', 'review_scores_cleanliness']
    validate_columns(data, required_columns)
    
    filtered_data = data[(data['neighbourhood_cleansed'] == neighborhood) & (data['review_scores_cleanliness'] > 4.0)]
    return len(filtered_data)

# Descriptions of listings (ex start:12 end:15)
def get_descriptions(data, start_row, end_row):
    print(start_row)
    print(end_row)
    required_columns = ['description']
    validate_columns(data, required_columns)
    
    return data.loc[start_row:end_row, 'description']

# Average price per neighborhood
def average_price_neighborhood(data, neighborhood):
    required_columns = ['neighbourhood_cleansed', 'price']
    validate_columns(data, required_columns)
    
    neighborhood_data = data[data['neighbourhood_cleansed'] == neighborhood]
    neighborhood_data['price'] = neighborhood_data['price'].str.replace('$', '').str.replace(',', '').astype(float)
    average_price = neighborhood_data['price'].mean()
    return average_price

# Total listings per host
def total_listings_per_host(data):
    required_columns = ['host_id', 'host_total_listings_count']
    validate_columns(data, required_columns)
    
    return data.groupby('host_id')['host_total_listings_count'].max()

# Listings with specific amenities
def listings_with_amenities(data, amenities):
    required_columns = ['amenities']
    validate_columns(data, required_columns)
    
    filtered_data = data[data['amenities'].apply(lambda x: all(amenity in x for amenity in amenities))]
    return filtered_data

# Distribution of review scores
def plot_review_scores_distribution(data):
    required_columns = ['review_scores_rating']
    validate_columns(data, required_columns)
    
    data['review_scores_rating'].dropna().plot.hist(bins=20)
    plt.title('Distribution of Review Scores')
    plt.xlabel('Review Score')
    plt.ylabel('Frequency')
    plt.show()

def main():
    # Load data
    data = load_data(CSV_FILEPATH)
    
    print("Welcome to the CLI - Airbnb!")
    print("Type 'Exit' to exit.")
    
    while True:
        command = input(f"Type one of the commands\n - top10 (Top 10 rated Airbnbs for at least 8 nights and instantly bookable)\n - pie (Distribution of host response rates in a pie chart)\n - count (Count of Airbnbs in a neighborhood with cleanliness rating > 4.0)\n - desc (Descriptions of listings (ex start:12 end:15)\n - avg_price (Average price per neighborhood)\n - total_listings (Total listings per host)\n - amenities (Listings with specific amenities)\n - review_dist (Distribution of review scores\n Enter:").strip().lower()
        
        if command == 'exit':
            print("Stopping the program...")
            break
        
        elif command == 'top10':
            print(top_10_airbnbs(data))
        
        elif command == 'pie':
            plot_response_rate_distribution(data)
        
        elif command == 'count':
            neighborhood = input("Type the name of the neighborhood: ").strip()
            print(f"The amount of Airbnbs in {neighborhood} with cleanliness score > 4.0: {count_clean_airbnbs(data, neighborhood)}")
        
        elif command == 'desc':
            try:
                start_row = int(input("Type the start row: ").strip())
                end_row = int(input("Enter the end row: ").strip())
                descriptions = get_descriptions(data, start_row, end_row)
                for i, description in descriptions.items():
                    print(f"Line {i}: {description}")
            except ValueError:
                print("Error: Please, type valid numbers to get the correct lines.")
        
        elif command == 'avg_price':
            neighborhood = input("Type the name of the neighborhood: ").strip()
            avg_price = average_price_neighborhood(data, neighborhood)
            print(f"The average price is {neighborhood} é ${avg_price:.2f}")
        
        elif command == 'total_listings':
            print(total_listings_per_host(data))
        
        elif command == 'amenities':
            amenities = input("Type the amenity to filter (ex: 'Hot water kettle'): ").strip().split(',')
            listings = listings_with_amenities(data, amenities)
            print(f"Number of results with the amenity chosen: {len(listings)}")
        
        elif command == 'review_dist':
            plot_review_scores_distribution(data)
        
        else:
            print("This command is not recongnized. Try again.")

if __name__ == '__main__':
    main()