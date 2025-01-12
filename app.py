# app.py
from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
from datetime import datetime
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MAX_POSTS = 100  # Prevent unlimited memory growth
    DEFAULT_LIKES_RANGE = (10, 500)
    DEFAULT_COMMENTS_RANGE = (1, 50)

# Initialize posts as a circular buffer
class PostBuffer:
    def __init__(self, max_size):
        self.max_size = max_size
        self.posts = []
    
    def add(self, post):
        if len(self.posts) >= self.max_size:
            self.posts.pop(0)  # Remove oldest post
        self.posts.append(post)
    
    def get_all(self):
        return self.posts
    
    def count(self):
        return len(self.posts)

posts_buffer = PostBuffer(Config.MAX_POSTS)

# Initialize Gemini if API key is available
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

CHARACTER_PROFILE = """
Name: Mei Zhang (dancing_rakoonnn)
Background: A quirky 20-year-old Chinese-Canadian student at UC Berkeley, combining Computer Science and Digital Arts.
She has a raccoon plushie named 'Binary' that she includes in her coding photos.

Personality Traits:
- Makes puns about programming and art
- Obsessed with bubble tea and names her git branches after different tea flavors
- Takes her raccoon plushie everywhere and poses it in photos
- Tends to anthropomorphize her code bugs
- Names all her tech devices after Studio Ghibli characters
- Has a collection of pixel art socks
- Known for her legendary 3 AM coding sessions fueled by bubble tea
"""

POST_SCENARIOS = [
    {
        "type": "coding_adventure",
        "prompts": [
            "Write a funny post about debugging at 3 AM where Mei personifies her bug as a mischievous character",
            "Create a post about Mei naming her git branches after bubble tea flavors and the chaos it caused in team code review",
            "Write about Binary (the raccoon plushie) helping with rubber duck debugging"
        ]
    },
     {
        "type": "food_quest",
        "prompts": [
            "Write about discovering a secret bubble tea menu item that changes the drink's color based on the temperature",
            "Create a post about rating different bubble tea shops based on their wifi speed for coding sessions",
            "Write about trying to teach Binary the raccoon to use chopsticks at a new fusion restaurant"
        ]
    },
     {
        "type": "art_tech_fusion",
        "prompts": [
            "Write about an AI art piece that accidentally gained sentience and started making memes",
            "Create a post about Mei's pixel art socks collection inspiring a new animation project",
            "Write about teaching her AI model to generate raccoon art but it keeps making possums instead"
        ]
    },
    {
        "type": "campus_life",
        "prompts": [
            "Write about DJing at a hackathon where the visualizations started responding to bugs in people's code",
            "Create a post about starting a club for people who name their devices after anime characters",
            "Write about Binary the raccoon becoming the unofficial mascot of the CS department"
        ]
    }
]

CREATIVE_FALLBACK_POSTS = [
    "Debug update: Named my latest bug 'Bob'. Bob likes to hide in nested loops and randomly change variable values...",
    # ... (previous fallback posts remain the same)
]

def generate_creative_post():
    """Generate a creative post using Gemini API or fallback to pre-written posts"""
    try:
        if not Config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
            
        scenario = random.choice(POST_SCENARIOS)
        prompt = random.choice(scenario["prompts"])
        
        full_prompt = f"""
        {CHARACTER_PROFILE}
        
        Task: {prompt}
        
        Rules:
        1. Be quirky and funny
        2. Include emojis
        3. Add relevant hashtags
        4. Reference character's interests and personality
        5. Keep it under 280 characters
        6. Make it sound natural and conversational
        """
        
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        app.logger.error(f"Error generating post: {e}")
        return random.choice(CREATIVE_FALLBACK_POSTS)

@app.route('/')
def home():
    """Render the main page with all posts"""
    return render_template(
        'index.html',
        posts_count=posts_buffer.count(),
        posts=posts_buffer.get_all()
    )

@app.route('/api/generate-post', methods=['POST'])
def generate_post():
    """Generate a new post and add it to the buffer"""
    try:
        content = generate_creative_post()
        
        post = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'likes': random.randint(*Config.DEFAULT_LIKES_RANGE),
            'comments': random.randint(*Config.DEFAULT_COMMENTS_RANGE)
        }


        
        posts_buffer.add(post)
        
        return jsonify({
            'status': 'success', 
            'post': post,
            'posts_count': posts_buffer.count()
        })
    except Exception as e:
        app.logger.error(f"Error in generate_post: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate post'
        }), 500

if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)