# AI Quiz Generator

## 📌 Overview
The **AI Quiz Generator** is a Streamlit-based web application that creates multiple-choice quizzes from any given text. Using Google's Gemini AI, the app generates quiz questions, provides interactive answering options, and offers real-time feedback on responses.
## Try the App here: [link](https://avgreddy-ai-quiz2-quiz-g0ey4j.streamlit.app/)


## 🚀 Features
- ✅ AI-generated multiple-choice questions (MCQs)
- ✅ Adjustable difficulty levels (Easy, Medium, Hard)
- ✅ Selectable number of questions (1-20)
- ✅ Countdown timer for quizzes
- ✅ Answer review with explanations
- ✅ Score tracking and instant feedback

## 🛠 Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **AI Model:** [Google Gemini AI](https://ai.google.dev/)
- **Backend:** Python
- **Environment Management:** `dotenv` for API key handling

## 📂 Project Structure
```
📦 AI-Quiz-Generator
├── .env                  # API key configuration
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Ignore sensitive files
```

## 🔧 Setup & Installation
### 1️⃣ Prerequisites
- Python 3.8+
- Google API Key for Gemini AI

### 2️⃣ Installation Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/AI-Quiz-Generator.git
   cd AI-Quiz-Generator
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage Guide
1. Enter the text content for the quiz.
2. Select the difficulty level and number of questions.
3. Click **Generate Quiz** to create questions.
4. Answer the quiz within the given time.
5. Submit responses and view instant feedback!

## 📜 License
This project is licensed under the MIT License.

## 👨‍💻 Author
Developed by [avgreddy](https://github.com/avgreddy). Contributions welcome! 🚀

