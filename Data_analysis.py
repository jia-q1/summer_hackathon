import pandas as pd

# Function to optimize data types
def optimize_types(df):
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        if pd.api.types.is_integer_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], downcast='signed')  # downcast to int32
        else:
            df[col] = pd.to_numeric(df[col], downcast='float')  # downcast to float32
    return df

# Optimizing and loading dataset in chunks
def load_and_optimize_csv(file_path, chunk_size=1000):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk = chunk.dropna()  # Drop NA in chunks
        chunk = optimize_types(chunk)
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    return df

# Load and optimize datasets
feeds_file_path = r'C:\Users\jiaqi\Downloads\train_data_feeds.csv'
ads_file_path = r'C:\Users\jiaqi\Downloads\train_data_ads.csv'

# Load and optimize datasets
#Publisher Dataset
df_feeds = load_and_optimize_csv(feeds_file_path)
#Advertiser Dataset
df_ads = load_and_optimize_csv(ads_file_path)


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

#%%PCA
import numpy as np
from sklearn.decomposition import PCA
from scipy import stats

# Identify potential customers
potential_customers = set(df_ads['user_id']).intersection(set(df_feeds['u_userId']))

# Filter dataframes to only include potential customers
ads_df = df_ads[df_ads['user_id'].isin(potential_customers)]
feeds_df = df_feeds[df_feeds['u_userId'].isin(potential_customers)]

feeds_df['u_userId'] = feeds_df['u_userId'].astype('int64')

# Merge the dataframes on user_id
merged_df = pd.merge(ads_df, feeds_df, left_on='user_id', right_on='u_userId')

X = merged_df[['age', 'gender', 'city', 'device_size', 'u_newsCatInterestsST', 'u_newsCatInterests']]

# Standardize the features (z-score)
zscoredData = stats.zscore(X)

# Fit PCA
pca = PCA()
pca.fit(zscoredData)

#Loadings
loadings = pca.components_*-1

# Proportion of variance explained by each component
eigVals = pca.explained_variance_

    
kaiserThreshold = 1
print('Number of factors selected by Kaiser criterion:', np.count_nonzero(eigVals > kaiserThreshold))

n_components = len(pca.explained_variance_ratio_)

    
varExplained = eigVals/sum(eigVals)*100
print("\nCumulative proportion of variance explained by components:")
for ii in range(len(varExplained)):
    print(varExplained[ii].round(3))
    
cumulative_variance = varExplained[0] + varExplained[1] + varExplained[2]
print("Cumulative variance explained by the first three principal components:", cumulative_variance)


#%% Part two
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from imblearn.over_sampling import SMOTE

def split_and_expand(df, column_name):
    # Split each cell value based on '^' 
    categories = df[column_name].str.split('^')
    
    # Determine the maximum number of categories
    max_categories = categories.apply(len).max()
    
    # Expand categories into separate columns and ensure all have max_categories columns
    expanded_categories = categories.apply(lambda x: pd.Series(x + [pd.NA] * (max_categories - len(x))))
    
    # Rename columns to indicate they are from the original column
    expanded_categories.columns = [f"{column_name}_{i+1}" for i in range(max_categories)]
    
    return expanded_categories

df_feeds = load_and_optimize_csv(feeds_file_path)
df_ads = load_and_optimize_csv(ads_file_path)

df_ads['user_id'] = df_ads['user_id'].astype('int64')
df_feeds['u_userId'] = df_feeds['u_userId'].astype('int64')

df_ads = df_ads.drop_duplicates(subset=['user_id'])
df_feeds = df_feeds.drop_duplicates(subset=['u_userId'])

merged_df = pd.merge(df_ads, df_feeds, left_on='user_id', right_on='u_userId', how='inner')
merged_df=merged_df.drop(columns=['u_userId'])
merged_df['target'] = 1

# Non-potential customers
publisher_only = df_ads[~df_ads['user_id'].isin(merged_df['user_id'])].copy()
advertiser_only = df_feeds[~df_feeds['u_userId'].isin(merged_df['user_id'])].copy()

publisher_only['target'] = 0 
advertiser_only['target'] = 0 

# Apply split_and_expand function to both columns POSSIBLE PROBLEM HERE 
u_newsCatInterestsST_y_expanded = split_and_expand(merged_df, 'u_newsCatInterestsST_y')
u_newsCatInterests_expanded = split_and_expand(merged_df, 'u_newsCatInterests')

merged_df = pd.concat([merged_df, u_newsCatInterestsST_y_expanded, u_newsCatInterests_expanded], axis=1)

# Drop original columns POSSIBLE PROBLEM HERE 
merged_df = merged_df.drop(columns=['u_newsCatInterestsST_y', 'u_newsCatInterests'])

# Combine merged_df with publisher_only and advertiser_only
final = pd.concat([merged_df, publisher_only, advertiser_only], ignore_index=True)

selected_columns = ['age', 'city', 'device_size', 'u_newsCatInterestsST_y_1', 'u_newsCatInterestsST_y_2', 'u_newsCatInterestsST_y_3', 'u_newsCatInterestsST_y_4','u_newsCatInterestsST_y_5','u_newsCatInterests_1','u_newsCatInterests_2','u_newsCatInterests_3','u_newsCatInterests_4','u_newsCatInterests_5', 'target']
#merged_df = merged_df[selected_columns]

final=final[selected_columns].dropna()

print(final.shape)
print("Columns in merged_df:")
print(final.columns)

# Create X 
X = final.copy()

# Ensure all columns are of type float or int
#for col in selected_columns:
   # if X[col].dtype == 'object':
        #X[col] = X[col].astype('category').cat.codes
   # else:
       # X[col] = X[col].astype(float)

# Convert target to int
y = final['target'].astype(int)

#Split

X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.2,random_state=42)


# Handling imbalanced data (not sure if this is needed)
#sm = SMOTE(random_state=42)
#X_train, y_train = sm.fit_resample(X_train, y_train)

scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

#Model
model=RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)

#Predictions
y_pred=model.predict(X_test)
y_pred_prob=model.predict_proba(X_test)[:,1]

#Evaluate
accuracy=accuracy_score(y_test,y_pred)
roc_auc=roc_auc_score(y_test,y_pred_prob)

print("Accuracy", accuracy)
print("ROC-AUC ", roc_auc)
