import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
import pickle

from prediciton import prediciton, dataPreporcessing, createCSV
from accessTOLog import logs2df, creat_xlsx, excelToCsv 
# import accessToLog2 

app = Flask(__name__)

#load the model 
model = pickle.load(open('savemodel.sav', 'rb'))

# @app.route('/')
# def home():
#     return render_template('index.html')

UPLOAD_FOLDER = 'C:\\Users\\user\\Documents\\LogfileJuypter\\regressionTree\\templates\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'log'}
fileName = ''
filePath = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/fig', methods=['GET', 'POST'])
def fig():
    import figure
    return render_template("fig.html")


@app.route('/prediction/<name>', methods=['GET', 'POST'])
def prediction(name):
    # fileName = request.args['fileName']
    # if request.method == 'GET':
    # fileName = request.args['fileName']
    # df = pd.read_csv(filePath)
     # excel_location = creat_xlsx()
    # df = excelToCsv(name)
    # dataPreporcessing(name)
    df = prediciton(name)
    df = df.drop(['referer', 'request'], axis=1)
    #--------------------------- to get csv file location use function createCSV(DF,name)----------------
    # csvFile = createCSV(df, name+"predicted")
    df_html = df.to_html()

    return render_template('prediction.html', data=df_html)  



@app.route('/CreatingDataset', methods=['POST', 'GET'])
def CreatingDataset():
    # X_test = float(request.form['X_test'])
    # result = model.predict(X_test)
    # return render_template('index.html', **locals) 
    # file = open(r'accessToLog2.py', 'r').read()
    # ./accessTOLog.py
    # return accessTOLog--------------**************
    
   
    fileName = request.args['fileName']
    filePath = request.args['filePath'] 
    # print("hgybui")
    excel_location = creat_xlsx()
    df = excelToCsv(fileName)

    # prediction(fileName, filePath)
    # templateData = template(text = water.get_last_watered())
    # templateData['redirect_url'] = url_for('new_page')
    # return render_template('main.html', **templateData)
    return render_template('loading.html'), {"Refresh": "3;url=prediction/{}".format(fileName)}
    # url=prediction, fileName=fileName, filePath=filePath

# @app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file =  request.form.get('file')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # f = request.form.get('file')
            # if f is not None:
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filePath)
            # message = json.dump("")
            print(filePath)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return redirect(url_for('CreatingDataset', filePath=filePath, fileName = secure_filename(file.filename)))
    return render_template('upload.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('CreatingDataset'))
    return render_template('index.html')






if __name__ == '__main__':
    
    app.run(debug=True)