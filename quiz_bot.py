import streamlit as st
import pandas as pd

# Define the questions and answer options
questions = [
    "I found myself getting upset by quite trivial things",
    "I was aware of dryness of my mouth",
    "I couldn't seem to experience any positive feeling at all",
    "I experienced breathing difficulty (e.g., excessively rapid breathing, breathlessness in the absence of physical exertion)",
    "I just couldn't seem to get going",
    "I tended to over-react to situations",
    "I had a feeling of shakiness (eg, legs going to give way)",
    "I found it difficult to relax",
    "I found myself in situations that made me so anxious that I was most relieved when they ended",
    "I felt that I had nothing to look forward to",
    "I found myself getting upset rather easily",
    "I felt that I was using a lot of nervous energy",
    "I felt sad and depressed",
    "I found myself getting impatient when I was delayed in any way (e.g., lifts, traffic lights, being kept waiting)",
    "I had a feeling of faintness",
    "I had lost interest in just about everything",
    "I felt I wasn't worth much as a person",
    "I felt that I was rather touchy",
    "I perspired noticeably (e.g., hands sweaty) in the absence of high temperatures or physical exertion",
    "I felt scared without any good reason",
    "I felt that life wasn't worthwhile"
]

answer_options = [
    "Not at all applies to me",
    "Applies to me little",
    "Sometimes applies to me",
    "Completely applicable for me"
]

def main():
    st.set_page_config(page_title="Mental Health Quiz", page_icon="🧠", layout="centered")
    st.title("Mental Health Self-Assessment Quiz")
    st.write("Please answer the following questions based on how you've been feeling recently.")

    # Initialize session state for storing answers
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    # Create a form
    with st.form("quiz_form"):
        for i, question in enumerate(questions, 1):
            st.write(f"**Q{i}:** {question}")
            st.session_state.answers[i] = st.radio(
                f"Your answer for Q{i}:",
                options=answer_options,
                key=f"q{i}",
                index=None  # This ensures no option is selected by default
            )
            st.write("---")  # Separator between questions

        submitted = st.form_submit_button("Submit Answers")

    if submitted:
        if None in st.session_state.answers.values():
            st.error("Please answer all questions before submitting.")
        else:
            st.success("Thank you for completing the quiz!")
            results = calculate_results(st.session_state.answers)
            display_results(results)

def calculate_results(answers):
    # Convert answers to numerical values
    numeric_answers = {q: answer_options.index(a) for q, a in answers.items()}
    
    # Calculate scores (this is a simplified scoring method)
    total_score = sum(numeric_answers.values())
    max_possible_score = len(questions) * 3  # 3 is the max score per question
    percentage = (total_score / max_possible_score) * 100
    
    return {
        "total_score": total_score,
        "max_score": max_possible_score,
        "percentage": percentage
    }

def display_results(results):
    st.write("## Your Results")
    st.write(f"Total Score: {results['total_score']} out of {results['max_score']}")
    st.write(f"Percentage: {results['percentage']:.2f}%")
    
    # Create a simple gauge chart
    import plotly.graph_objects as go
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = results['percentage'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Mental Health Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 33], 'color': "lightgreen"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"}
            ],
        }
    ))
    
    st.plotly_chart(fig)
    
    # Provide a general interpretation
    if results['percentage'] < 33:
        st.write("Your responses suggest a low level of distress. However, if you have any concerns, please consult with a mental health professional.")
    elif results['percentage'] < 66:
        st.write("Your responses suggest a moderate level of distress. Consider talking to a mental health professional for further evaluation and support.")
    else:
        st.write("Your responses suggest a high level of distress. It's recommended to consult with a mental health professional for proper evaluation and support.")

    st.write("**Note:** This quiz is not a diagnostic tool. For accurate assessment and advice, please consult with a qualified mental health professional.")

if __name__ == "__main__":
    main()