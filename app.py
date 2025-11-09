import streamlit as st
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Script to Image Prompt Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎬 Script to Image Prompt Generator (Gemini + Streamlit)")
st.markdown("---")

# --- SIDEBAR: API KEY INPUT ---
with st.sidebar:
    st.header("1. Gemini API Key")
    # API key input field
    gemini_api_key = st.text_input(
        "Enter your Gemini API Key:", 
        type="password", 
        help="Get your key from Google AI Studio. This key is not stored."
    )
    
    # Information/Help
    st.markdown("---")
    st.caption("Key Features:")
    st.caption("- Analyzes full script/screenplay.")
    st.caption("- Generates detailed, high-quality image prompts.")
    st.caption("- Pairs each prompt with the original script line.")

# --- MODEL SELECTION ---
MODEL_NAME = "gemini-2.5-flash" 
# This model is excellent for structured text generation and is cost-effective.

# --- MAIN APP INTERFACE ---

st.header("2. Paste Your Full Script")

script_input = st.text_area(
    "Full Screenplay or Story Script:", 
    height=300, 
    placeholder="SCENE 1: A lone explorer stands on a Martian ridge. Dust swirls around his boots. He raises a hand to shield his eyes from the twin moons.",
    key="script_input_box"
)

# --- The Magic Prompt (Instructions for Gemini) ---
def create_gemini_prompt(script_text):
    prompt = f"""
    You are an expert Creative Director and Visual Storyteller. Your task is to analyze the provided script and generate a **highly detailed, artistic Image Generation Prompt** (like for Midjourney, Stable Diffusion, or DALL-E) for every significant action or dialogue line in the script.

    Your output MUST be a **Markdown List** where each item contains two parts, separated by '->':
    1.  **The Original Script Line (bold):** The exact line from the script.
    2.  **The Image Prompt:** A detailed, descriptive prompt (including style, lighting, camera angle, and mood) that visually captures the essence of that line.

    **Strict Output Format (ONLY use this format):**
    * **[Original Script Line]** -> [Detailed Image Prompt, including artistic style, lighting, and mood]

    **Example:**
    * **The two friends stand silently on a desolate hill.** -> A cinematic wide shot of two silhouette figures standing on a barren mountain peak at twilight, dramatic lens flare, deep purples and oranges, ultra-realistic, 8k.
    * **The child laughs loudly and embraces a dog.** -> A heartwarming, close-up portrait of a child laughing joyfully while hugging a Golden Retriever puppy, soft morning light, shallow depth of field, photorealistic, Canon EOS R5.

    ---
    **Original Script to Analyze:**
    {script_text}
    """
    return prompt

# --- Generate Button Logic ---
st.header("3. Generate Prompts")

if st.button("🖼️ Generate Image Prompts", use_container_width=True):
    # 1. Validation Checks
    if not gemini_api_key:
        st.error("❌ Error: Baraye meherbani sidebar mein apna Gemini API Key daalain.")
        st.stop()
        
    if not script_input:
        st.warning("⚠️ Warning: Baraye meherbani script paste karein.")
        st.stop()
        
    # 2. Process
    with st.spinner("Gemini is analyzing your script and crafting visual prompts..."):
        try:
            # Initialize Client with the user-provided key
            client = genai.Client(api_key=gemini_api_key)
            
            # Prompt creation
            full_prompt = create_gemini_prompt(script_input)
            
            # Call Gemini API
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt
            )
            
            # Display Results
            st.subheader("✅ Generated Image Prompts")
            # Streamlit will automatically render the Markdown response from Gemini
            st.markdown(response.text)

        except Exception as e:
            # Catch API errors (e.g., invalid key, rate limit)
            st.error(f"❌ An error occurred. Check your API Key or script content: {e}")

st.markdown("---")
st.caption("Powered by Google Gemini API and Streamlit")

# --- End of app.py ---
