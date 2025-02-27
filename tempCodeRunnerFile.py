app = Flask(__name__)


#   Landing page
@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method=='GET':
        return render_template('landing_page.html')