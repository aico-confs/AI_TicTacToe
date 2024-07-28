#%%
import random
import numpy as np
import pickle

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)  # 0 represents empty cell, 1 represents X, -1 represents O
        self.current_player = 1  # 1 for X, -1 for O

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        return self.board

    def is_valid_action(self, action):
        row, col = action
        return self.board[row, col] == 0

    def step(self, action):
        if not self.is_valid_action(action):
            print("# Invalid move!")
            return self.board, -10, True  # Invalid move
        # -10是給人看的，訓練過程中，禁制事項應放在例外管理

        row, col = action
        self.board[row, col] = self.current_player

        if self.check_winner(self.current_player):
            return self.board, 1, True  # Current player wins
        elif np.all(self.board != 0):
            return self.board, 0, True  # Draw

        self.current_player *= -1
        return self.board, 0, False  # Game continues


    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                return True
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            return True
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            return True
        return False

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]


#%%
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, q_table = {}):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = q_table  # State-action values

    def get_q_value(self, state, action):
        return self.q_table.get((self.to_tuple(state), action), 0.0)

    def to_tuple(self, state):
        return tuple(map(tuple, state))

    def choose_action(self, state, available_actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_actions)
        q_values = [self.get_q_value(state, action) for action in available_actions]
        max_q_value = max(q_values)
        return random.choice([action for action, q_value in zip(available_actions, q_values) if q_value == max_q_value])

    def learn(self, state, action, reward, next_state, done):
        current_q = self.get_q_value(state, action)
        max_next_q = max([self.get_q_value(next_state, a) for a in env.available_actions()], default=0)
        if done: 
            target_q = reward  
        else :
            target_q = -1 * (reward + self.gamma * max_next_q)
        self.q_table[(self.to_tuple(state), action)] = current_q + self.alpha * (target_q - current_q)
    def save(self):
        print('進行學習更新......')
        with open('config.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)

# Initialize the environment
env = TicTacToe()
with open('config.pkl', 'rb') as f:
    loaded_q_table = pickle.load(f) 
agent = QLearningAgent()
agent.q_table = loaded_q_table






# def who_wins(target_list):


#     for mode in [0, 1]:
#         train_list = target_list[mode::2]
#         check_set = set(train_list)
#         finish = [['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['0', '4', '8'], ['2', '4', '6'], ['0', '3', '6'], ['1', '4', '7'], ['2', '5', '8']]
#         for fin in finish:
#             for f in fin:
#                 if f in check_set:
#                     continue
#                 else:
#                     break
#             else:
#                 return {'finish':True, 'mode':mode}
#     return {'finish':False}

# def answer(currData:str, mode):
    
#     available_actions = env.available_actions()
#     action = agent.choose_action(state, available_actions)
#     next_state, reward, done = env.step(action)
#     # modeJson = {
#     #     # 玩家先手、玩家後手
#     #     "先手":"defensive.json",
#     #     "後手":"offensive.json"
#     # }
#     # with open(modeJson[mode], 'r') as pre_f:
#     #     jsondata = json.load(pre_f)
#     # num_List = [str(i) for i in range(0, 9) if str(i) not in currData]
#     # max_flag = num_List[0]
#     # for i in num_List[1:]:
#     #     if jsondata.get(currData+i, 0) > jsondata.get(currData+max_flag, 0):
#     #         max_flag = i
#     # return {'message':'200', 'answer':max_flag, } 


# def Make_Output(s):
    
#     np.random.choice(values, p=probabilities)
#     pass

# def Count_Reward(s, a):
#     pass 



# #%%

# if __name__ == "__main__":
#     mode = 0
#     filename = {0:'offensive', 1:'defensive'}[mode]
    
#     # 指定範圍和機率
#     values = np.arange(0, 9)  # 0 到 8 的範圍
#     probabilities = [0.1, 0.05, 0.15, 0.2, 0.1, 0.1, 0.05, 0.15, 0.1]  # 每個數值的抽樣機率
#     # probabilities = np.random.rand(len(values))
#     # probabilities /= probabilities.sum()  # 確保機率和為 1
#     history = []
#     next_s = []
#     t = 1
#     Eposide = 5
    
#     while t <= Eposide:
        
#         # 看到最新的ENV (INPUT)
#         s = next_s

#         # 產生 OUTPUT        
#         a = Make_Output(s)
        
#         #  計算Reward
#         r = Count_Reward(s, a)

#         # 紀錄歷程
#         history += [((s, a), r)]

        
#         # OUTPUT 對 ENV 產生影響
#         next_s = s + [a]       
        
        
#         # 更新下一次eposide的環境
#         t += 1
#     else:
#         # 計算該次eposide的G
#         Eposide_Reward = []
#         for index in range(len(history)):
#             g = 0
#             rate = 1
#             for _, r in history[index:]:
#                 g+= r * rate
#                 rate = rate ** 0.9
#             else:
#                 Eposide_Reward += [((s, a), g)]

    
    
    
    
#%%
    # result = dict()
    # permutations = list(itertools.permutations(range(1, 10)))

    # while len(permutations):
    #     full_list = list(map(str, permutations.pop(0)))
    #     out = False
    #     N = 5
    #     mode = 1
    #     filename = {0:'offensive', 1:'defensive'}[mode]
    #     while N <10:
    #         target_list = full_list[:N]
    #         check_chunk = who_wins(target_list)
            
    #         train_list = target_list[mode:N:2]
    #         end_id = target_list.index(train_list[-1])+1
    #         for train_id in train_list:
    #             train_id = target_list.index(train_id)+1
    #             target_key = ''.join(target_list[:train_id])
    #             result[target_key] = result.get(target_key, 0)
    #             if check_chunk['finish'] and  check_chunk['mode'] == mode:    
    #                 result[target_key] += round(1/factorial(end_id - train_id), 2)
    #                 out = True
    #                 break

                
    #         if out:break
    #         N+=1

    # with open(f'{filename}.json', 'w') as f:
    #     json.dump(result, f, indent = 2)
    # # %%


