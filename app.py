import streamlit as st
from agno.agent import Agent
from agno.tools.eleven_labs import ElevenLabsTools
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up the Streamlit app
st.title("📖 Magic Ear Stories")
st.markdown("Enter a topic and select a language to generate a short story with audio")

# User inputs
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Enter story topic", "Jack and the Beanstalk")
with col2:
    language = st.selectbox("Select language", ["English", "Tamil", "Telugu", "Hindi", "Spanish"])

# Voice mapping for different languages
VOICE_IDS = {
    "English": "JBFqnCBsd6RMkjVDRZzb",
    "Tamil": "MF3mGyEYCl7XYWbV9V6O",
    "Telugu": "TX3LPaxmHKxFdv7VOQHJ",
    "Hindi": "XB0fDUnXU5powFXDhCwa",
    "Spanish": "D38z5RcWu1voky8WS1ja"
}

if st.button("Generate Story & Audio"):
    with st.spinner("Creating your story and audio..."):
        try:
            # Initialize the agent with selected language voice
            agent = Agent(
                model=Groq(id="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY")),
                tools=[
                    ElevenLabsTools(
                        voice_id=VOICE_IDS[language],
                        model_id="eleven_multilingual_v2",
                        target_directory="audio_outputs"
                    )
                ],
                name=f"{language} Story Agent"
            )

            # Generate the story
            prompt = (
                f"Write a 10-15 line short story about {topic} in {language}. "
                f"Use simple {language} language suitable for audio narration. "
                "Return only the story text without any titles or extra formatting."
            )
            
            response = agent.run(prompt)
            story_text = response.content.strip()

            # Generate audio
            audio_response = agent.run(f"Convert this {language} text to speech: {story_text}")
            
            audio_files = sorted(
                [f for f in os.listdir("audio_outputs") if f.endswith(".mp3")],
                key=lambda x: os.path.getmtime(os.path.join("audio_outputs", x)),
                reverse=True
            )
            
            if audio_files:
                audio_path = os.path.join("audio_outputs", audio_files[0])
                st.audio(audio_path, format="audio/mp3")
                
                # Download button
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="Download Audio",
                        data=f,
                        file_name=f"{topic[:20]}_{language}.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.warning("Audio generation failed - no output file found")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions
st.markdown("""
### How to use:
1. Enter your story topic (e.g., "Rabbit and Tortoise")
2. Select your preferred language
3. Click "Generate Story & Audio"
4. Listen to the audio or download it
""")