import numpy as np
import pandas as pd
from gym.utils import seeding
import gym
from gym import spaces
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle


HMAX_NORMALIZE = 100
# initial amount of money we have in our account
INITIAL_ACCOUNT_BALANCE=1000000
# total number of assets in our portfolio
CRYPTO_DIM = 1
TRANSACTION_FEE_PERCENT = 0.05
REWARD_SCALING = 1e-4

class CrpytoEnvTrain(gym.Env):
    """A crypto trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df,day = 0):
        self.day = day
        self.df = df

        # action_space normalization and shape is CRYPTO_DIM
        self.action_space = spaces.Box(low = -1, high = 1,shape = (CRYPTO_DIM,))
        self.observation_space = spaces.Box(low=0, high=np.inf, shape = (7,))
        # load data from a pandas dataframe
        self.data = self.df.loc[self.day,:]
        self.terminal = False
        # initalize state
        print(self.data)
        self.state = [INITIAL_ACCOUNT_BALANCE] + \
              [self.data.v.tolist()] + \
              [0]*CRYPTO_DIM + \
              [self.data.o.tolist()] + \
              [self.data.c.tolist()] + \
              [self.data.vw.tolist()] + \
              [self.data.n.tolist()]# initialize reward
        self.reward = 0
        self.cost = 0
        # memorize all the total balance change
        self.asset_memory = [INITIAL_ACCOUNT_BALANCE]
        self.rewards_memory = []
        self.trades = 0
        self._seed()


    def _sell_stock(self, index, action):
        # perform sell action based on the sign of the action
        if self.state[index+CRYPTO_DIM+1] > 0:
            #update balance
            self.state[0] += \
            self.state[index+1]*min(abs(action),self.state[index+CRYPTO_DIM+1]) * \
             (1- TRANSACTION_FEE_PERCENT)

            self.state[index+CRYPTO_DIM+1] -= min(abs(action), self.state[index+CRYPTO_DIM+1])
            self.cost +=self.state[index+1]*min(abs(action),self.state[index+CRYPTO_DIM+1]) * \
             TRANSACTION_FEE_PERCENT
            self.trades+=1
        else:
            pass


    def _buy_stock(self, index, action):
        # perform buy action based on the sign of the action
        available_amount = self.state[0] // self.state[index+1]

        #update balance
        self.state[0] -= self.state[index+1]*min(available_amount, action)* \
                          (1+ TRANSACTION_FEE_PERCENT)

        self.state[index+CRYPTO_DIM+1] += min(available_amount, action)

        self.cost+=self.state[index+1]*min(available_amount, action)* \
                          TRANSACTION_FEE_PERCENT
        self.trades+=1

    def step(self, actions):
        self.terminal = self.day >= len(self.df.index.unique())-1

        if self.terminal:
            plt.plot(self.asset_memory,'r')
            plt.close()
            end_total_asset = self.state[0]+ \
            sum(np.array(self.state[1:(CRYPTO_DIM+1)])*np.array(self.state[(CRYPTO_DIM+1):(CRYPTO_DIM*2+1)]))

            df_total_value = pd.DataFrame(self.asset_memory)
            df_total_value.to_csv('results/account_value_train.csv')
            df_total_value.columns = ['account_value']
            df_total_value['daily_return']=df_total_value.pct_change(1)

            if df_total_value['daily_return'].std() > 0:
              sharpe = (4 ** 0.5) * df_total_value['daily_return'].mean() / \
                      df_total_value['daily_return'].std()
            else:
              sharpe = (4 ** 0.5) * df_total_value['daily_return'].mean() / 1

            df_rewards = pd.DataFrame(self.rewards_memory)

            return self.state, self.reward, self.terminal,{}

        else:

            actions = actions * HMAX_NORMALIZE

            begin_total_asset = self.state[0]+ \
            sum(np.array(self.state[1:(CRYPTO_DIM+1)])*np.array(self.state[(CRYPTO_DIM+1):(CRYPTO_DIM*2+1)]))

            argsort_actions = np.argsort(actions)

            sell_index = argsort_actions[:np.where(actions < 0)[0].shape[0]]
            buy_index = argsort_actions[::-1][:np.where(actions > 0)[0].shape[0]]

            for index in sell_index:
                self._sell_stock(index, actions[index])

            for index in buy_index:
                self._buy_stock(index, actions[index])

            self.day += 1
            self.data = self.df.loc[self.day,:]
            #load next state
            self.state =  [self.state[0]] + \
                    [self.data.v] + \
                    list(self.state[(CRYPTO_DIM+1):(CRYPTO_DIM*2+1)]) + \
                    [self.data.o] + \
                    [self.data.c] + \
                    [self.data.vw] + \
                    [self.data.n]

            end_total_asset = self.state[0]+ \
            sum(np.array(self.state[1:(CRYPTO_DIM+1)])*np.array(self.state[(CRYPTO_DIM+1):(CRYPTO_DIM*2+1)]))
            self.asset_memory.append(end_total_asset)

            self.reward = end_total_asset - begin_total_asset
            self.rewards_memory.append(self.reward)

            self.reward = self.reward*REWARD_SCALING



        return self.state, self.reward, self.terminal, {}

    def reset(self):
        self.asset_memory = [INITIAL_ACCOUNT_BALANCE]
        self.day = 0
        self.data = self.df.loc[self.day,:]
        self.cost = 0
        self.trades = 0
        self.terminal = False
        self.rewards_memory = []
        #initiate state
        self.state = [INITIAL_ACCOUNT_BALANCE] + \
                      [self.data.v.tolist()] + \
                      [0]*CRYPTO_DIM + \
                      [self.data.o.tolist()] + \
                      [self.data.c.tolist()] + \
                      [self.data.vw.tolist()] + \
                      [self.data.n.tolist()]
        return self.state

    def render(self, mode='human'):
        return self.state

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
        
# adapted from previous project based off of https://towardsdatascience.com/finrl-for-quantitative-finance-tutorial-for-multiple-stock-trading-7b00763b7530