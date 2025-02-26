import streamlit as st
import json
import os
import re
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="AI Quiz Generator", page_icon="🎓", layout="wide")

# Custom CSS for hover effects
st.markdown("""
    <style>
        .stButton>button {
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            background-color: #4CAF50 !important; /* Green color on hover */
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("### 📖 About")
st.sidebar.write(
    "This AI-powered quiz generator creates MCQs based on the text you provide. "
    "You can select difficulty levels, specify the number of questions, and take the quiz with a timer."
)

st.sidebar.markdown("### 🎨 Customize")
st.sidebar.write(
    """
    - Adjust difficulty levels.  
    - Choose the number of questions.  
    - Set a timer for answering.  
    - Get instant feedback on your answers.  
    """
)

st.sidebar.markdown("### 🔥 Interactive")
st.sidebar.write(
    """
    ✅ AI-generated MCQs  
    ✅ Countdown timer  
    ✅ Answer review with explanations  
    ✅ Score tracking and feedback  
    """
)

# Function to determine countdown timer duration
def get_timer_duration(difficulty, num_questions):
    base_time_per_question = {"Easy": 30, "Medium": 45, "Hard": 60}  # Time in seconds
    return base_time_per_question[difficulty] * num_questions

# Function to extract valid JSON from AI response
def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None

# Function to generate questions
@st.cache_data
def fetch_questions(text_content, quiz_level, num_questions):
    if not text_content.strip():
        return [], "❌ Error: No text provided!"

    PROMPT_TEMPLATE = f"""
    You are an AI quiz generator. Based on the provided text, generate exactly {num_questions} multiple-choice questions at the '{quiz_level}' difficulty level.

    TEXT:
    {text_content}

    Return the output strictly in this JSON format:

    {{
        "mcqs": [
            {{
                "mcq": "Question 1?",
                "options": {{
                    "a": "Option A",
                    "b": "Option B",
                    "c": "Option C",
                    "d": "Option D"
                }},
                "correct": "a",
                "explanation": "A detailed explanation for the correct answer."
            }},
            ...
        ]
    }}

    Ensure that exactly {num_questions} questions are included.
    """

    try:
        response = model.generate_content(PROMPT_TEMPLATE)
        if not response or not response.text:
            return [], "❌ Error: Empty response from AI!"

        extracted_response = extract_json(response.text)
        if extracted_response and "mcqs" in extracted_response and len(extracted_response["mcqs"]) == num_questions:
            return extracted_response["mcqs"], None
        else:
            return [], "❌ Error: Incorrect number of questions generated!"
    except Exception as e:
        return [], f"❌ AI Request Error: {str(e)}"

def main():
    st.title("✨ AI-Powered Quiz Generator 🎓")
    st.write("Generate multiple-choice quizzes from any text instantly!")

    st.markdown("### 📄 **Enter Your Text Below**")
    text_content = st.text_area(
        "Paste your text here:",
        height=180,
        placeholder="Enter the content for quiz generation...",
        help="AI will generate MCQs based on the text you enter.",
    )

    col1, col2 = st.columns(2)
    with col1:
        quiz_level = st.selectbox("🎚 Select difficulty:", ["Easy", "Medium", "Hard"])

    with col2:
        num_questions = st.number_input("🔢 Number of questions:", min_value=1, max_value=20, value=5, step=1)

    # Initialize session state variables
    if "time_left" not in st.session_state:
        st.session_state.time_left = 0
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "selected_options" not in st.session_state:
        st.session_state.selected_options = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if st.button("🚀 Generate Quiz"):
        with st.spinner("Generating your quiz..."):
            questions, error_message = fetch_questions(text_content, quiz_level, num_questions)

        if questions:
            st.session_state.questions = questions
            st.session_state.quiz_generated = True
            st.session_state.selected_options = {}
            st.session_state.time_left = get_timer_duration(quiz_level, num_questions)
            st.session_state.submitted = False
            st.success("✅ Quiz Generated Successfully!")
            st.rerun()
        else:
            st.error(error_message or "❌ Failed to generate quiz. Try again with different text.")

    if st.session_state.quiz_generated and not st.session_state.submitted:
        st.divider()
        st.write("## 🎯 Your Quiz")

        timer_placeholder = st.empty()

        with st.form(key="quiz_form"):
            for i, question in enumerate(st.session_state.questions):
                with st.expander(f"❓ Question {i+1}"):
                    st.markdown(f"**{question['mcq']}**")
                    options = [f"{key}: {value}" for key, value in question["options"].items()]
                    option_key = f"question_{i}"

                    selected_option = st.radio("Select an answer:", options, key=option_key, index=None)

                    if selected_option:
                        st.session_state.selected_options[i] = selected_option.split(":")[0]

            submitted = st.form_submit_button("✅ Submit Answers")

        if submitted:
            st.session_state.submitted = True
            st.rerun()

        while st.session_state.time_left > 0:
            mins, secs = divmod(st.session_state.time_left, 60)
            timer_placeholder.markdown(f"### ⏳ Time Left: {mins:02d}:{secs:02d}")
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()

        if st.session_state.time_left == 0:
            st.session_state.submitted = True
            st.rerun()

    if st.session_state.submitted:
        st.success("✅ Quiz Submitted!")
        st.write("### 📊 Quiz Results")

        marks = 0
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}. {question['mcq']}**")

            selected_letter = st.session_state.selected_options.get(i)
            correct_letter = question["correct"]
            explanation = question.get("explanation", "No explanation available.")

            st.write(f"✅ Correct answer: **{correct_letter.upper()} - {question['options'][correct_letter]}**")
            with st.expander("📝 Show Complete Explanation"):
                st.info(explanation)

            if selected_letter == correct_letter:
                marks += 1

        st.markdown(f"### 🎉 Score: **{marks} / {len(st.session_state.questions)}**")

        if st.button("🔄 Reset Quiz"):
            st.session_state.quiz_generated = False
            st.session_state.submitted = False
            st.session_state.selected_options = {}
            st.session_state.questions = []
            st.session_state.time_left = 0
            st.rerun()

if __name__ == "__main__":
    main()
