# Creative Social Post Generator

A Flask application that generates quirky and creative social media posts using the Gemini AI API and a fun character profile, Mei Zhang (aka dancing_rakoonnn). The app supports random post generation based on predefined scenarios and maintains a circular buffer for posts.

## Features

- **AI-Generated Posts:** Generates creative posts using the Gemini API (if configured).
- **Character Profile:** Customizes posts based on Mei Zhang's personality and interests.
- **Circular Buffer:** Limits the maximum number of stored posts to prevent memory issues.
- **Fallback Posts:** Uses predefined fallback posts if the API is unavailable.
- **API Integration:** Provides an endpoint for generating posts programmatically.
- **Interactive Web UI:** Displays all generated posts in a user-friendly interface.

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (optional, but recommended)
