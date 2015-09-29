from flask import Flask, request, render_template
import cPickle as pickle
app = Flask(__name__)



# home page
@app.route('/')
def index():
    return render_template("index.html", data="")
    # return  '''
    # Welcome to Articles Classifier!
    # <a href='\submission'>Submission Page</a>
    # '''

@app.route('/hilary')
def hilary_page():
    return render_template("hilary.html", data="")
         
@app.route('/sanders')
def sanders_page():
    return render_template("sanders.html", data="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
