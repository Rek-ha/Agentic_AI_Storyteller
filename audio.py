from agno.agent import Agent
from agno.tools.eleven_labs import ElevenLabsTools
from agno.models.groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set API keys in environment (needed by ElevenLabs tool internally)
os.environ["ELEVEN_LABS_API_KEY"] = ELEVEN_LABS_API_KEY

# Create an Agent with ElevenLabs tool and Groq model
agent = Agent(
    model=Groq(id="llama3-70b-8192", api_key=GROQ_API_KEY),
    tools=[
        ElevenLabsTools(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            target_directory="audio_generations"
        )
    ],
    name="ElevenLabs Agent"
)

# Generate audio on the story about rabbit and tortoise
#agent.print_response("Generate an audio on the story about rabbit and tortoise", markdown=True)


agent.print_response("Tell the story of Jack and the Beanstalk in one voice, as a single audio narration.", markdown=True)


