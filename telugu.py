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
os.environ["ELEVEN_LABS_API_KEY"] = ELEVEN_LABS_API_KEY

# Step 1: Generate Telugu story text
text_agent = Agent(
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY),
    tools=[],
    name="Telugu Story Generator"
)

telugu_story = text_agent.run(
    "Write a complete Telugu story about the rabbit and tortoise (తోడేలు మరియు తాబేలు). "
    "The story should be 9-10 sentences long with proper Telugu grammar. "
    "Return only the pure Telugu text without any English or special characters."
).content.strip()

# Step 2: Convert to audio with Telugu-optimized voice
audio_agent = Agent(
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY),
    tools=[
        ElevenLabsTools(
            voice_id="TX3LPaxmHKxFdv7VOQHJ",  # Best Telugu voice
            model_id="eleven_multilingual_v2",
            target_directory="telugu_stories",
        )
    ],
    name="Telugu Audio Generator"
)

audio_agent.print_response(
    f"Convert this Telugu text to clear speech: {telugu_story}",
    markdown=True
)

print(f"Generated Telugu Story:\n{telugu_story}")
print("Audio saved in 'telugu_stories' folder!")