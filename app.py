from flask import Flask, render_template, jsonify, request, session
import config
import openai
import aiapi
import notebook


def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])

app.register_error_handler(404, page_not_found)


@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        prompt = request.form['prompt']
        res = {}
        #### change here ####
        # new_conversation = request.form.get('new_conversation', False)
        if 'new_conversation' not in session:
            session['new_conversation'] = True

        if session['new_conversation']:
            session['new_conversation'] = False
            answer = "I am Wallace, Sabin's AI chatbot. How can I assist you today?"
        else:
            answer = notebook.customChatGPTAnswer(prompt)
        
        res = {'answer': answer}
        ### till here #### 
        # res['answer'] = notebook.customChatGPTAnswer(prompt)
        return jsonify(res), 200

    return render_template('index3.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
