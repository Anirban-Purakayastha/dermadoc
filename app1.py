import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io
from dotenv import load_dotenv
# Configure Gemini API (Replace with your actual API key)
import os
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("API_KEY"))


# Create Gemini Pro Vision model
vision_model = genai.GenerativeModel('gemini-1.5-flash')

def create_theme_css(is_dark_mode):
    """
    Generate dynamic CSS based on selected theme
    """
    if is_dark_mode:
        return """
        <style>
        :root {
            /* Dark Mode Colors */
            --bg-primary: #121212;
            --bg-secondary: #1E1E1E;
            --text-primary: #E0E0E0;
            --text-secondary: #B0B0B0;
            --border-color: #333333;
            --input-bg: #2C2C2C;
            --button-bg: #4A4A4A;
            --hover-color: #555555;
            --send-button-bg: #4A90E2;
        }
        
        body, .stApp {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }
        
        
        .prompt-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 16px;
            background-color: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            z-index: 1000;
        }
        
        .prompt-input {
            width: 100%;
            background-color: var(--input-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            padding: 12px !important;
            resize: none !important;
        }
        
        .send-button {
            background-color: var(--send-button-bg) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 16px !important;
        }
        
        .file-upload-container {
            background-color: var(--input-bg) !important;
            border: 1px dashed var(--border-color) !important;
            border-radius: 8px !important;
            padding: 12px !important;
            margin-bottom: 12px !important;
        }
        </style>
        """
    else:
        return """
        <style>
        :root {
            /* Light Mode Colors */
            --bg-primary: #FFFFFF;
            --bg-secondary: #F5F5F5;
            --text-primary: #333333;
            --text-secondary: #666666;
            --border-color: #E0E0E0;
            --input-bg: #FFFFFF;
            --button-bg: #F0F0F0;
            --send-button-bg: #4A90E2;
        }
        
        body, .stApp {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }
        
        /* ChatGPT-like Prompt Box */
        .prompt-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 16px;
            background-color: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            z-index: 1000;
        }
        
        .prompt-input {
            width: 100%;
            background-color: var(--input-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            padding: 12px !important;
            resize: none !important;
        }
        
        .send-button {
            background-color: var(--send-button-bg) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 16px !important;
        }
        
        .file-upload-container {
            background-color: var(--input-bg) !important;
            border: 1px dashed var(--border-color) !important;
            border-radius: 8px !important;
            padding: 12px !important;
            margin-bottom: 12px !important;
        }
        </style>
        """

def analyze_skin_condition(uploaded_file, problem_description):
    """
    Analyze skin condition using Gemini API
    """
    try:
        # Convert uploaded image to PIL Image
        image = Image.open(uploaded_file)
        
        # Prompt for medical analysis
        prompt = f"""
        Perform a comprehensive medical analysis of this skin/hair condition.
        Provide:
        1. Potential diagnosis
        2. Recommended treatments
        3. Prescription medicines
        4. Potential side effects of prescribed medicines
        5. Additional care recommendations

        Context from user: {problem_description}
        """
        
        # Generate response
        response = vision_model.generate_content([prompt, image])
        
        return response.text
    except Exception as e:
        st.error(f"Error in analysis: {e}")
        return None

def main():
    # Initialize session state
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    # Page configuration
    st.set_page_config(
        page_title="Dermat AI Doctor",
        page_icon="🩺",
        layout="wide"
    )

    # Custom CSS for additional styling
    st.markdown("""
    <style>
    /* Chat History Styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        padding: 20px;
        margin-bottom: 100px;
    }
    .user-message {
        align-self: flex-end;
        max-width: 80%;
        margin-bottom: 15px;
    }
    .ai-message {
        align-self: flex-start;
        max-width: 80%;
        margin-bottom: 15px;
    }
    .message-box {
        border-radius: 12px;
        padding: 12px;
        max-width: 100%;
    }
    .preview-image {
        max-width: 200px;
        max-height: 200px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Theme toggle
    st.markdown("""
    <div style='position: absolute; top: 20px; right: 20px;'>
        <label class="switch">
            <input type="checkbox" id="theme-switch">
            <span>🌓</span>
        </label>
    </div>
    """, unsafe_allow_html=True)

    # Apply dynamic theme CSS
    st.markdown(create_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

    # Theme switch JavaScript
    st.markdown("""
    <script>
    const themeSwitch = document.getElementById('theme-switch');
    themeSwitch.checked = sessionStorage.getItem('darkMode') === 'true';
    
    themeSwitch.addEventListener('change', function() {
        sessionStorage.setItem('darkMode', this.checked);
        window.location.reload();
    });
    </script>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 style='text-align: center;'>🩺 Dermat AI Doctor</h1>", unsafe_allow_html=True)

    # Chat History Container
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    
    # Render chat history
    for item in st.session_state.chat_history:
        if item['type'] == 'user':
            st.markdown(f"""
            <div class='user-message' style='display: flex; justify-content: flex-end; width: 100%;'>
                <div class='message-box' style='background-color: #4A90E2; color: white;'>
                    {item['message']}
                    {'<img src="data:image/png;base64,' + item['image'] + '" class="preview-image">' if item.get('image') else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='ai-message' style='display: flex; justify-content: flex-start; width: 100%;'>
                <div class='message-box' style='background-color: #E0E0E0; color: black;'>
                    {item['message']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Prompt Container
    st.markdown('<div class="prompt-container">', unsafe_allow_html=True)
    
    # Columns for file upload and text input
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # File Uploader
        uploaded_file = st.file_uploader(
            "Upload Image", 
            type=['png', 'jpg', 'jpeg'], 
            label_visibility="collapsed"
        )
    
    with col2:
        # Problem Description Input
        problem_description = st.text_area(
            "Describe Your Medical Concern", 
            placeholder="Describe your skin or hair condition in detail...",
            key="prompt_input",
            label_visibility="collapsed",
            className="prompt-input"
        )

    # Send Button
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        send_button = st.button("Send", key="send_button", use_container_width=True, className="send-button")

    st.markdown('</div>', unsafe_allow_html=True)

    # Analysis Logic
    if send_button and (uploaded_file or problem_description):
        # Add user message to chat history
        if uploaded_file:
            # Convert image to base64
            img_byte_arr = io.BytesIO()
            Image.open(uploaded_file).save(img_byte_arr, format='PNG')
            img_str = base64.b64encode(img_byte_arr.getvalue()).decode()
            
            # Add user message with image
            st.session_state.chat_history.append({
                'type': 'user',
                'message': problem_description,
                'image': img_str
            })
        else:
            # Add user message without image
            st.session_state.chat_history.append({
                'type': 'user',
                'message': problem_description
            })

        # Perform analysis
        with st.spinner('Analyzing your condition...'):
            analysis_result = analyze_skin_condition(uploaded_file, problem_description) if uploaded_file else None
            
            # Add AI response to chat history
            if analysis_result:
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'message': analysis_result
                })
            else:
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'message': "I apologize, but I need an image to provide a comprehensive analysis. Could you please upload an image of the skin or hair condition?"
                })

        # Clear input
        st.experimental_rerun()

    # Disclaimer
    st.markdown("""
    <div style='
        text-align: center; 
        position: fixed; 
        bottom: 70px; 
        left: 0; 
        right: 0;
        font-size: 0.8em;
        opacity: 0.7;
    '>
    🚨 Disclaimer: This AI tool is for informational purposes only and does not replace professional medical advice.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()