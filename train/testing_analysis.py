import pandas as pd 

df_feeds = pd.read_csv('train_data_feeds.csv').dropna() #no harm in dropping na's 

#Advertisers Dataset 
df_ads = pd.read_csv('train_data_ads.csv').dropna()

# Print shapes
print(f"Final DataFrame Of The Publisher Dataset shape: {df_feeds.shape}")
print(f"Final DataFrame Of The Advertiser Dataset shape: {df_ads.shape}")


#%%Code for Age Group Distribution 
import matplotlib.pyplot as plt

def plot_age_distribution(df_ads, df_feeds):
    #Common IDs between both datasets
    ads_ids = set(df_ads['user_id'].unique())
    feeds_ids = set(df_feeds['u_userId'].unique())
    common_ids = ads_ids.intersection(feeds_ids)
    
    # Filter ads dataset to include only common IDs
    ads_with_common_ids = df_ads[df_ads['user_id'].isin(common_ids)]
    
    # Get the age distribution and sort by age
    ages_counts = ads_with_common_ids['age'].value_counts().sort_index()
    
    # Plot distribution
    plt.figure(figsize=(10, 6))
    plt.bar(ages_counts.index, ages_counts.values, color='skyblue')
    plt.xlabel('Unique Value of Ages')
    plt.ylabel('Number of Users')
    plt.title('Distribution of Ages Among Users Who Click on Ads')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(ages_counts.index)  # Ensure x-axis labels are aligned correctly
    
    # Add text annotations
    for age, count in zip(ages_counts.index, ages_counts.values):
        plt.text(age, count + 0.5, str(count), ha='center', va='bottom', fontsize=8)
    
    plt.show()

# Example usage
# Assuming df_ads and df_feeds are your DataFrames
plot_age_distribution(df_ads, df_feeds)

#%%Geographic Distribution

def plot_city_distribution(df_ads, df_feeds):
    # Common IDs between both datasets
    common_ids = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))
    
    # Filter ads dataset to include only common IDs
    ads_with_common_ids = df_ads[df_ads['user_id'].isin(common_ids)]
    
    # Get the city distribution and sort by frequency
    cities_counts = ads_with_common_ids['city'].value_counts().sort_values(ascending=False)
   
    #Would city_rank be better? 
    
    # Top 10 since there are too many cities 
    top_n = 10
    top_cities = cities_counts.head(top_n)
    
    # Plot distribution
    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_cities.index, top_cities.values, color='skyblue')
    plt.xlabel('City Value')
    plt.ylabel('Number of Users')
    plt.title(f'Top {top_n} Cities Among Users Who Click on Ads')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45, ha='right')  
    
    # Add text annotations with city names and counts
    for bar, (city, count) in zip(bars, top_cities.items()):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{city}\n({count})", ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()  
    plt.show()


plot_city_distribution(df_ads, df_feeds)

#%%Distribution of Devices that are being used 

def plot_devices_distribution(df_ads, df_feeds):
    # Common IDs between both datasets
    common_ids = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))
    
    # Filter ads dataset to include only common IDs
    ads_with_common_ids = df_ads[df_ads['user_id'].isin(common_ids)]
    
    # Get the device distribution and sort by frequency
    devices_counts = ads_with_common_ids['device_size'].value_counts().sort_values(ascending=False)
    
    top_n = 10
    top_devices = devices_counts.head(top_n)
    
    # Plot distribution
    plt.figure(figsize=(15, 8))
    bars = plt.bar(top_devices.index, top_devices.values, color='skyblue')
    plt.xlabel('Device Size')
    plt.ylabel('Number of Users')
    plt.title(f'Top {top_n} Devices Sizes Among Users Who Click on Ads')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    

    for bar, (device_size, count) in zip(bars, top_devices.items()):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{device_size}\n({count})", ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()  
    plt.show()

plot_devices_distribution(df_ads, df_feeds)


#%%Engagement Patterns
import seaborn as sns

common_ids = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))
    
# Filter ads dataset to include only common IDs
ads_with_common_ids = df_ads[df_ads['user_id'].isin(common_ids)]
  
# 'pt_d' is a string column representing dates in the format 'YYYYMMDDHHMM'
df_ads['timestamp'] = pd.to_datetime(ads_with_common_ids['pt_d'], format='%Y%m%d%H%M')

# Extract hour and day of the week from the timestamp
df_ads['hour'] = df_ads['timestamp'].dt.hour
df_ads['day_of_week'] = df_ads['timestamp'].dt.dayofweek

# Count ad clicks per hour
hourly_clicks = df_ads.groupby('hour').size()

plt.figure(figsize=(12,6))
sns.barplot(x=hourly_clicks.index, y=hourly_clicks.values, palette='viridis')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Ad Clicks')
plt.title('Ad Clicks by Hour of the Day')
plt.grid(True, linestyle='--', alpha=0.6)
for i, v in enumerate(hourly_clicks.values):
    plt.text(i, v + 1, str(v), ha='center')
plt.show()

# Count ad clicks per day of the week
daily_clicks = df_ads.groupby('day_of_week').size()

plt.figure(figsize=(12,6))
sns.barplot(x=daily_clicks.index, y=daily_clicks.values, palette='viridis')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Ad Clicks')
plt.title('Ad Clicks by Day of the Week')
plt.xticks(ticks=range(7), labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.grid(True, linestyle='--', alpha=0.6)
for i, v in enumerate(daily_clicks.values):
    plt.text(i, v + 1, str(v), ha='center')
plt.show()
#%% Content Preferences
import seaborn as sns

# If is probability not necessary; Used it because something wasn't working before 
if 'u_newsCatInterestsST' in df_feeds.columns and 'u_newsCatInterests' in df_feeds.columns:
    # Find common IDs between both datasets
    common_ids = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))

    # Filter ads dataset to include only common IDs
    ads_with_common_ids = df_ads[df_ads['user_id'].isin(common_ids)]

    # Combine
    combined_interests = df_feeds['u_newsCatInterestsST'].dropna() + '^' + df_feeds['u_newsCatInterests'].dropna()

    # Split the combined strings, then flatten the list
    combined_interests = combined_interests.str.strip('^')
    all_interests = combined_interests.str.split('^').explode()

    # Count the frequency of each unique value
    category_counts = all_interests.value_counts().sort_values(ascending=False)

    # Get the top 10 categories since there are too many values 
    top10 = category_counts.head(10)

    # Plot the distribution
    plt.figure(figsize=(12, 6)) 
    sns.barplot(x=top10.index, y=top10.values, palette='viridis')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Distribution of Top 10 News Category Interests')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.grid(True, linestyle='--', alpha=0.6)

    # Add text annotations
    for i, v in enumerate(top10.values):
        plt.text(i, v + 0.5, str(v), ha='center')

    plt.tight_layout(pad=2.0)  
    plt.show()
else:
    print("There's an Error, GG")


#%% Task 2 Identifying Potential Customers 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

print("Data types of ads_df:")
print(df_ads.dtypes)
print("\nData types of feeds_df:")
print(df_feeds.dtypes)

# Identify potential customers
potential_customers = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))

# Filter dataframes to only include potential customers
ads_df = df_ads[df_ads['user_id'].isin(potential_customers)]
feeds_df = df_feeds[df_feeds['u_userId'].isin(potential_customers)]

feeds_df['u_userId'] = feeds_df['u_userId'].astype('int64')

# Merge the dataframes on user_id
merged_df = pd.merge(ads_df, feeds_df, left_on='user_id', right_on='u_userId')


# Feature Engineering
# Select a subset of features and target variable
features = ['age', 'gender', 'city', 'device_size', 'u_newsCatInterestsST', 'u_newsCatInterests']
target = 'label'

# Drop rows with missing values in features and target
merged_df = merged_df[features + [target]].dropna()

# Ensure correct data types
for col in features:
    if merged_df[col].dtype == 'object':
        print(f"Column {col} is of type object, which is unexpected.")

# Convert numerical features explicitly
numerical_features = ['age', 'device_size', 'u_newsCatInterestsST', 'u_newsCatInterests']
for col in numerical_features:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

# Check for any remaining NaNs
print(merged_df[numerical_features].isna().sum())

# Drop any rows that have NaNs after conversion
merged_df = merged_df.dropna()

# Separate features and target variable
X = merged_df[features]
y = merged_df[target]

# Encode categorical variables
X = pd.get_dummies(X, columns=['gender', 'city'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical features
scaler = StandardScaler()
X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test[numerical_features] = scaler.transform(X_test[numerical_features])

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Evaluate the model
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba)}")