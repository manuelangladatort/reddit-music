import logging
import time
import json
from pathlib import Path
import praw

# API details
YOUR_CLIENT_ID = "Iny6ZNxNXNFXuvS0OAtL3Q"
YOUR_CLIENT_SECRET = "N5qmBqY3Syln6qIoE9efDsyL6X34EA"
USERNAME = "One-Author7372 "


NUMBER_OF_POSTS = 100 # use None to download all posts

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
    rate_limit_delay: int = 2
) -> None:
    """
    Download posts from a specified subreddit with rate limiting and error handling.
    
    Args:
        subreddit (str): Name of the subreddit to download from
        output_dir (str): Directory to save the downloaded data
        sort_by (str): How to sort the posts ('new', 'top', 'hot', etc.)
        download_type (str): Type of data to download ('json', 'csv', etc.)
        rate_limit_delay (int): Delay between requests in seconds
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
            posts = subreddit_instance.new(limit=NUMBER_OF_POSTS)
        elif sort_by == "top":
            posts = subreddit_instance.top(limit=NUMBER_OF_POSTS)
        elif sort_by == "hot":
            posts = subreddit_instance.hot(limit=NUMBER_OF_POSTS)
        else:
            raise ValueError(f"Invalid sort method: {sort_by}")
        
        # Download posts
        posts_data = []
        for post in posts:
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
    SUBREDDIT = "LetsTalkMusic"
    OUTPUT_DIR = "lets_talk_music_data"
    
    try:
        download_subreddit_posts(
            subreddit=SUBREDDIT,
            output_dir=OUTPUT_DIR,
            sort_by="new",
            download_type="json",
            rate_limit_delay=2
        )
    except Exception as e:
        logging.error(f"Failed to download posts: {str(e)}")
        exit(1)