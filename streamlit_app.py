# Import required libraries
import praw
import pandas as pd
import os
import warnings
from datetime import datetime, timedelta

# Suppress PRAW async warning
warnings.filterwarnings("ignore", category=UserWarning)

# Store credentials securely (REPLACE with your actual values)
os.environ["REDDIT_CLIENT_ID"] = "3fXfFslCainOY6xM4Zm0Ng"
os.environ["REDDIT_CLIENT_SECRET"] = "1Zxte6SguEhBrtYAJirOBI7kbwV3yQ"
os.environ["REDDIT_USER_AGENT"] = "name"

# Retrieve credentials from environment variables
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

# Initialize Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Ask the user for the subreddit to scrape
subreddit_name = input("Enter the subreddit name (without 'r/'): ").strip()

# Define subreddit to scrape
subreddit = reddit.subreddit(subreddit_name)

# List to store scraped data
data = []
count = 0  # Counter for valid posts

# Get the timestamp for 6 months ago
six_months_ago = datetime.utcnow() - timedelta(days=180)
six_months_ago_timestamp = six_months_ago.timestamp()

print(f"Fetching up to 100 posts from r/{subreddit_name} in the last 6 months...")

# Scrape top posts, filtering only those from the last 6 months
for post in subreddit.top(limit=300):  # Fetch more to ensure 100 valid ones
    if post.created_utc >= six_months_ago_timestamp:  # Check if post is within the last 6 months
        data.append({
            'Post_id': post.id,
            'Title': post.title,
            'Author': post.author.name if post.author else 'Unknown',
            'Timestamp': pd.to_datetime(post.created_utc, unit='s'),
            'Text': post.selftext,
            'Score': post.score,
            'Total_comments': post.num_comments,
            'Post_URL': post.url
        })
        count += 1

    if count >= 100:  # Stop once we have 100 posts
        break

# Convert data to a Pandas DataFrame
reddit_data = pd.DataFrame(data)

# Define output CSV file name
csv_filename = f"{subreddit_name}_top_100_last_6_months.csv"

# Save as CSV file
reddit_data.to_csv(csv_filename, index=False)

print(f"✅ Successfully saved top 100 posts from r/{subreddit_name} (last 6 months) to {csv_filename}!")
