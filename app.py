from flask import Flask, request, render_template, url_for, redirect
from model import env, agent
import os, pickle

app = Flask(__name__)
app.static_folder = 'templates/static'




@app.route("/")
def hello_world():

    return render_template('index.html', title='井字遊戲')

@app.route("/reset_board", methods=[ "POST"])
def reset_board():
    if request.method == "POST":
        env.reset()
        env.current_player = 1 if request.form.get("mode") == '先手' else -1

        return  {'message':'200'}  
    return  {'message':'reset_board error'}  

@app.route("/save", methods=[ "POST"])
def save():
    if request.method == "POST":
        agent.save()
        return  {'message':'200'}  
    return  {'message':'save error'} 

@app.route("/calc", methods=[ "POST"])
def calc():
    if request.method == "POST":
        state = env.board.copy()

        # 從前端拿數據
        if env.current_player == 1:  # Human's turn
            value = int(request.form.get("value"))
            row = value // 3
            col = value % 3
            action = (row, col)
            if not env.is_valid_action(action):
                return  {'message':"Invalid move. Try again."}  
        else:  # AI's turn
            available_actions = env.available_actions()
            action = agent.choose_action(state, available_actions)
            print(f"AI chooses action: {action}")
            
        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state, done)
        
        # print(agent.get_q_value([[ 0,0,1], [0, 1 , 0], [ 0 , 0 ,-1]], (1, 0)))
        # for i in agent.q_table:
        #     if agent.q_table[i] > 0:
        #         print(agent.q_table[i])
        #         print(i)
        
        answer = action[0]*3+action[1] 
        if done:
            print(env.board)
            if env.current_player == 1 :answer = ''
            if reward == 1:
                if env.current_player == 1 :agent.save()
                winner = "玩家"  if env.current_player == 1 else  "AI"
                return {'message': f"{winner} 贏了!", "answer":answer} 
             
            elif reward == 0:
                return {'message': "平手!", "answer":answer}  
        # 輪到人類玩家
        if env.current_player == 1:
            return  {'message':"200", "answer":answer}
        else:
            return   redirect(url_for('calc'),  code=307)
        

        # print(currData)
        # if who_wins(currData)['finish']: 
        #     mode =  { 0:"先手", 1:"後手", }[who_wins(currData)['mode']]
        #     return  {'message':f'遊戲結束, {mode}獲勝'}  
        # else:
        #     answer_chunk = answer(currData=currData, mode=mode)
        #     check_chunk = who_wins(currData + answer_chunk['answer'])
        #     if check_chunk['finish']:
        #         mode =  { 0:"先手", 1:"後手", }[check_chunk['mode']]
        #         return  {'message':f'遊戲結束, {mode}獲勝', 'answer':answer_chunk['answer']} 
        # return answer_chunk



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='127.0.0.1', port=port)
    
    
