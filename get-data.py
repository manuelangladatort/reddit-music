import logging
import time
import json
from pathlib import Path
import praw
from datetime import datetime, timezone

# API details (replace with keys)
YOUR_CLIENT_ID = "key"
YOUR_CLIENT_SECRET = "key"
USERNAME = "username"

# Global parameters
SUBREDDIT = "LetsTalkMusic"
OUTPUT_DIR = "lets_talk_music_data"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reddit_download.log'),
        logging.StreamHandler()
    ]
)

def download_subreddit_posts(
    subreddit: str,
    output_dir: str = "reddit_data",
    sort_by: str = "new",
    download_type: str = "json",
    rate_limit_delay: int = 2,
    start_timestamp: int = None
) -> None:
    """
    Download posts from a specified subreddit with rate limiting and error handling.
    
    Args:
        subreddit (str): Name of the subreddit to download from
        output_dir (str): Directory to save the downloaded data
        sort_by (str): How to sort the posts ('new', 'top', 'hot', etc.)
        download_type (str): Type of data to download ('json', 'csv', etc.)
        rate_limit_delay (int): Delay between requests in seconds
        start_timestamp (int): Unix timestamp to start downloading from
    """
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logging.info(f"Starting download from r/{subreddit}")
        
        # Initialize Reddit API client
        reddit = praw.Reddit(
            client_id=YOUR_CLIENT_ID,
            client_secret=YOUR_CLIENT_SECRET,
            user_agent=f"python:reddit-post-downloader:v1.0 (by /u/{USERNAME})"
        )
        
        # Get subreddit instance
        subreddit_instance = reddit.subreddit(subreddit)
        
        # Get posts based on sort method
        if sort_by == "new":
            posts = subreddit_instance.new(limit=None)  # None means get all available posts
        elif sort_by == "top":
            posts = subreddit_instance.top(limit=None)
        elif sort_by == "hot":
            posts = subreddit_instance.hot(limit=None)
        else:
            raise ValueError(f"Invalid sort method: {sort_by}")
        
        # Download posts
        posts_data = []
        post_count = 0
        logging.info("Starting to process posts...")
        
        for post in posts:
            # Skip posts before start_timestamp if specified
            if start_timestamp and post.created_utc < start_timestamp:
                continue
                
            post_data = {
                "id": post.id,
                "title": post.title,
                "author": str(post.author),
                "created_utc": post.created_utc,
                "score": post.score,
                "url": post.url,
                "selftext": post.selftext,
                "num_comments": post.num_comments
            }
            posts_data.append(post_data)
            post_count += 1
            
            # Log progress every 100 posts
            if post_count % 100 == 0:
                logging.info(f"Processed {post_count} posts")
            
            time.sleep(rate_limit_delay)  # Rate limiting
        
        # Save data
        output_file = output_path / f"{subreddit}_{sort_by}.{download_type}"
        if download_type == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported download type: {download_type}")
        
        logging.info(f"Successfully downloaded {len(posts_data)} posts from r/{subreddit}")
        
    except Exception as e:
        logging.error(f"Error downloading from r/{subreddit}: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuration
    try:
        # Set start timestamp to January 1, 2011
        start_timestamp = int(datetime(2015, 1, 1, tzinfo=timezone.utc).timestamp())
        
        download_subreddit_posts(
            subreddit=SUBREDDIT,
            output_dir=OUTPUT_DIR,
            sort_by="new",  
            download_type="json",
            rate_limit_delay=2,
            start_timestamp=start_timestamp
        )
    except Exception as e:
        logging.error(f"Failed to download posts: {str(e)}")
        exit(1)