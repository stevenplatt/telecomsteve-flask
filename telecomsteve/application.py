# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
# push updated deployment using 'eb deploy' from within the folder telecomsteve/

from flask import Flask, render_template

application = Flask(__name__)

@application.route("/")
def home():
    return render_template('index.html')




# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run (host= '0.0.0.0') # (host="localhost", port=8000)
