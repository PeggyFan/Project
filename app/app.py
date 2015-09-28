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
    return '''
          !DOCTYPE html>
          <html>
              <head>
                  <meta charset="utf-8">
                  <title>Page Title</title>
              </head>
              <body>
              <!-- page content -->
                  <h1>My Page</h1>
                  <p>
                  Topic 1: 'win election democratic nomination party general vote democrats think clinton'
                  Topic 2: 'email server private state information classified government emails use secretary'
                  Topic 3: 'president hillary woman america rodham united states qualified ms clinton'
                  Topic 4: 'mrs mr clinton republican good party obama position wehner republicans'
                  Topic 5: 'biden joe run president clinton better race presidency vp man'
                  Topic 6: 'times story coverage nyt news ny reporting page clinton readers'
                  Topic 7: 'trump republican bush donald gop clinton hillary candidates like fiorina'
                  Topic 8: 'hilary bernie win joe hiding like run left wow better'
                  Topic 9: 'sanders bernie hillary support clinton media candidate campaign socialist need'
                  Topic 10: 'change people just black don like blm lives want know'
                  </p>
                  <p style="color: purple; text-align: right;">
                      My right-aligned purple text.
                  </p>
              </body>
          </html>
    '''
         

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
