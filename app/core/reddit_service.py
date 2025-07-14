import asyncpraw
import asyncio
import os
from typing import Tuple, List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "persona-script")

async def get_reddit_data(username: str) -> Tuple[List[str], List[str]]:
    """
    Retrieve Reddit comments and posts for a given username
    
    Args:
        username: Reddit username to analyze
        
    Returns:
        Tuple containing lists of comments and posts
    """
    reddit = asyncpraw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    try:
        user = await reddit.redditor(username)
        
        # Fetch up to 100 comments and posts
        comments = []
        posts = []
        
        async for comment in user.comments.new(limit=100):
            comments.append(comment.body)
            
        async for post in user.submissions.new(limit=100):
            posts.append(post.title + "\n" + post.selftext)
        
        return comments, posts
    except Exception as e:
        print(f"Error retrieving Reddit data for user {username}: {e}")
        return [], []

def prepare_documents(comments: List[str], posts: List[str]) -> List[Document]:
    """
    Convert raw comments and posts into LangChain Document objects
    
    Args:
        comments: List of user comments
        posts: List of user posts
        
    Returns:
        List of Document objects
    """
    documents = []
    
    # Process comments
    for i, comment in enumerate(comments):
        documents.append(
            Document(
                page_content=comment,
                metadata={"source": "comment", "index": i}
            )
        )
    
    # Process posts
    for i, post in enumerate(posts):
        documents.append(
            Document(
                page_content=post,
                metadata={"source": "post", "index": i}
            )
        )
    
    # Split long documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    return text_splitter.split_documents(documents)