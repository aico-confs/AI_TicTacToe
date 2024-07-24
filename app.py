from flask import Flask, request, render_template
from model import check, answer
import os

app = Flask(__name__)
app.static_folder = 'templates/static'



@app.route("/")
def hello_world():

    return render_template('index.html', title='33')

@app.route("/calc", methods=[ "POST"])
def calc():
    if request.method == "POST":
        # 從前端拿數據
        currData = request.form.get("currData")
        mode = request.form.get("mode")

        print(currData)
        if check(currData)['finish']: 
            return  {'message':f'遊戲結束, {mode}獲勝'}  
        return answer(currData=currData, mode=mode)

    return render_template('index.html', title='33')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='127.0.0.1', port=port)
    
    
