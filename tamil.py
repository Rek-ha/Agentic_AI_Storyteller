from agno.agent import Agent
from agno.tools.eleven_labs import ElevenLabsTools
from agno.models.groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Step 1: Create agent just for text generation
text_agent = Agent(
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY),
    tools=[],
    name="Tamil Story Generator"
)

# Generate the Tamil story text
story_response = text_agent.run(
    "Write a complete Tamil story about the rabbit and tortoise (முயலும் ஆமையும்). "
    "The story should be 5-7 sentences long with proper Tamil grammar. "
    "Return only the Tamil text without any English or additional formatting."
)

# Extract the clean Tamil text
tamil_story = story_response.content.strip()

# Step 2: Create agent for audio generation
audio_agent = Agent(
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY),
    tools=[
        ElevenLabsTools(
            voice_id="MF3mGyEYCl7XYWbV9V6O",  # Tamil-optimized voice
            model_id="eleven_multilingual_v2",
            target_directory="tamil_stories"
        )
    ],
    name="Tamil Audio Generator"
)

# Generate audio from the clean Tamil text
audio_agent.print_response(
    f"Convert this Tamil text to speech: {tamil_story}",
    markdown=True
)

print(f"Success! Audio generated for Tamil story:\n{tamil_story}")