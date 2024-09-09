from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import time

# Load the CSV file into a DataFrame with specified encoding
df = pd.read_csv('tax.csv', encoding='utf-8')

# Shuffle the DataFrame to randomize the order of questions
df = df.sample(frac=1).reset_index(drop=True)

# Initialize the Flask app
app = Flask(__name__)

# Global variables
question_index = 0
start_time = None

# Index route to start the quiz
@app.route('/')
def index():
    global question_index, df, start_time
    question_index = 0  # Reset the question index
    start_time = time.time()  # Set the start time of the quiz
    question = df.iloc[question_index]['question']
    total_questions = len(df)
    return render_template('index.html', question=question, show_yes_no_buttons=True, feedback="", show_retry_button=False, total_questions=total_questions, current_question=question_index+1, elapsed_time=format_time(time.time() - start_time))

# Quiz route to display questions and check answers, or retry the quiz
@app.route('/quiz_or_retry', methods=['POST'])
def quiz_or_retry():
    global question_index, df, start_time
    user_answer = request.form.get('answer')

    if user_answer is not None:
        correct_answer = df.iloc[question_index]['answer']
        feedback = 'Incorrect!' if user_answer.lower() != correct_answer.lower() else 'Correct!'
        show_yes_no_buttons = False
        show_retry_button = True

        if feedback == 'Correct!':
            time.sleep(1)  # Wait for 1 second before moving to the next question
            question_index += 1
            if question_index < len(df):
                show_yes_no_buttons = True
                show_retry_button = False
                question = df.iloc[question_index]['question']
                return render_template('index.html', question=question, show_yes_no_buttons=show_yes_no_buttons, feedback="Good! Next question!", show_retry_button=show_retry_button, total_questions=len(df), current_question=question_index+1, elapsed_time=format_time(time.time() - start_time))
            else:
                # End of the quiz
                return render_template('index.html', question='Quiz complete!', show_yes_no_buttons=False, feedback="Well done! Congratulations!", show_retry_button=True, total_questions=len(df), current_question=question_index+1, elapsed_time=format_time(time.time() - start_time))

        else:
            # Incorrect answer, stay on the same question
            explanation = df.iloc[question_index]['explanation']
            if pd.isnull(explanation):
                explanation = ""
            return render_template('index.html', question=df.iloc[question_index]['question'], show_yes_no_buttons=show_yes_no_buttons, feedback=feedback, show_retry_button=show_retry_button, explanation=explanation, total_questions=len(df), current_question=question_index+1, elapsed_time=format_time(time.time() - start_time))

    else:
        return redirect(url_for('index'))  # Reload the page without processing the answer

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# 2024-02-12 implemented
    # simply yes or no question
    # flask app and index html to be interactive
    # make the program accessible via local network to any device and not only on the local device server

# 2024-02-13 implemented  
    # show empty string when no answer is clicked
    # always show the "Yes" and "No" buttons
    # if incorrect answer is clicked, stay on the question, show incorrect feedback message, remove yes or no answer buttons, show only retry button
    # retry button needs to be as big as no button
    # if retry button is clicked, then restart the quiz again, with the questions shuffled in a random manner again
    # on quiz complete, don't show yes or no answer options, show retry

# 2024-02-14 implemented
    # if correct answer is selected, stay on the same question for 1 second, show positive feedback and say next (since I cannot figure out how to show the correct message on the same question for 1 second before the next question comes up), and then automatically move onto the next question
    # if incorrect answer, show explanation under the feedback message
    # if there is no explanation, don't show explanation in the feedback message
    # add a column in the data base for explanation
    # show progress
    # show timer to calculate the time spent on each quiz

# [Future implements]
    # check copy right
    # monetization strategy: appstore, google ad, in app purchase, 
    # marketing strategy: instagram, naver cafe, etc.
    # make it publicly accessible

    