from flask import Flask , render_template , request , url_for , redirect , flash , session
from surveys import satisfaction_survey
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Loki' 


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        session['responses'] = []
        return redirect(url_for('question_page', question_index=0))
    return render_template('start.html' , satisfaction_survey = satisfaction_survey)


@app.route('/questions/<int:question_index>', methods= ['GET', 'POST'])
def question_page(question_index):

    responses = session.get('responses', [])
    app.logger.debug(f'Current responses: {responses}')

    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you_page'))
    
    if question_index != len(responses):
        flash('Please answer the questions in order.')
        return redirect(url_for('question_page' , question_index = len(responses)))
    
    if request.method == 'POST':
        selected_choice = request.form.get('choice')
        if not selected_choice:
            flash('Please select an option before submitting.')
            return redirect(url_for('question_page', question_index=question_index))

        responses.append(selected_choice)
        session['responses'] = responses
        session.modified = True
        return redirect(url_for('question_page', question_index = question_index + 1))

    question = satisfaction_survey.questions[question_index]
    return render_template('questions.html' , question=question, question_index=question_index)
       

@app.route('/thank-you')
def thank_you_page():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
