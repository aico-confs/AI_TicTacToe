#%%
import numpy as np
import pickle
import random

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

# Initialize the environment
env = TicTacToe()
#%%
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}  # State-action values

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
# Initialize the agent
"""
alpha : 每次看到新棋局的學習速度，積分的加減是簡易的線性，因此越小、學的越慢，可以越謹慎
gamma: : 未來的走勢影響當下有多少，模型已設計成越遠影響越低，降低的程度由gamma決定
epsilon: AI不思考亂亂選的機率

"""
agent = QLearningAgent(alpha=0.01, gamma=0.9, epsilon=0.1)

# Load the Q-table from a file
with open('config.pkl', 'rb') as f:
    loaded_q_table = pickle.load(f)

# Create a new agent and assign the loaded Q-table
agent = QLearningAgent()
agent.q_table = loaded_q_table

# Training the agent
num_episodes = 42000000

for episode in range(num_episodes):

    state = env.reset().copy()
    done = False
    env.current_player = 1
    while not done:
        available_actions = env.available_actions()
        action = agent.choose_action(state, available_actions)
        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state, done)
        state = next_state.copy()
    if episode % 1000000 == 0:
        print(f'累積{episode}')
        agent.save()
    # if len(agent.q_table) >  23299:
    #     agent.save()
        

# TODO  如果效果不好，鎖定只有切換到特定玩家才learn

print("Training completed.")

# Save the Q-table to a file
with open('config.pkl', 'wb') as f:
    pickle.dump(agent.q_table, f)


#%%


def play_game(agent, human_first=True):
    state = env.reset().copy()
    done = False
    env.current_player = 1 if human_first else -1  # Decide who goes first

    while not done:
        print(env.board)
        if env.current_player == 1:  # Human's turn
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            action = (row, col)
            if not env.is_valid_action(action):
                print("Invalid move. Try again.")
                continue
        else:  # AI's turn
            available_actions = env.available_actions()
            action = agent.choose_action(state, available_actions)
            print(f"AI chooses action: {action}")

        next_state, reward, done = env.step(action)
        state = next_state.copy()
        if done:
            print(env.board)
            if reward == 1:
                winner = "Human" if env.current_player == 1 else "AI"
                print(f"{winner} wins!")
            elif reward == 0:
                print("It's a draw!")
            break
        
        
# Play a game where human goes first
play_game(agent, human_first=True)


#%%


# Load the Q-table from a file
with open('config.pkl', 'rb') as f:
    loaded_q_table = pickle.load(f)

# Create a new agent and assign the loaded Q-table
agent = QLearningAgent()
agent.q_table = loaded_q_table

# %%
