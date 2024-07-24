#%%
import json
import random
import numpy as np

def check(target_list):

    modeTurn = {
        0:"先手",
        1:"後手",
    }
    for mode in [0, 1]:
        train_list = target_list[mode::2]
        check_set = set(train_list)
        finish = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['1', '5', '9'], ['3', '5', '7'], ['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9']]
        for fin in finish:
            for f in fin:
                if f in check_set:
                    continue
                else:
                    break
            else:
                return {'finish':True, 'mode':modeTurn[mode]}
    return {'finish':False}

def answer(currData:str, mode):
    modeJson = {
        # 玩家先手、玩家後手
        "先手":"defenive.json",
        "後手":"offensive.json"
    }
    with open(modeJson[mode], 'r') as pre_f:
        jsondata = json.load(pre_f)
    num_List = [str(i) for i in range(1, 10) if str(i) not in currData]
    max_flag = num_List[0]
    for i in num_List[1:]:
        if jsondata.get(currData+i, 0) > jsondata.get(currData+max_flag, 0):
            max_flag = i
    return {'message':'200', 'answer':max_flag, }  
#%%

if __name__ == "__main__":
    Epochs = 1000000    
    epoch = 0
    result = dict()

    while epoch < Epochs:
        target_list = list(map(str, list((range(1, 10)))))
        random.shuffle(target_list)    
        N = 5
        mode = 1

        while N <10:
            train_list = target_list[mode:N:2]
            if check(target_list):
                for train_id in train_list:
                    target_key = ''.join(sorted(target_list[:target_list.index(train_id)+1]))
                    result[target_key] = result.get(target_key, 0)
                    result[target_key] +=1
            N+=1
            
        
        epoch +=1


    with open('defenive.json', 'w') as f:
        # jsondata[year][month][day] = {'info':money, 'final':sum(money + [0]), 'MinEarn':min(money + [0])}
        json.dump(result, f, indent = 2)
    # %%


