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
@app.route('/<candidate>')
def candidate_page(candidate):
  html_page = candidate + '.html'
  return render_template(html_page, data="")

@app.route('/about')
def about_page():
  html_page = 'about.html'
  return render_template(html_page, data="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
