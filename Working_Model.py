import numpy as np
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head                  # probability of flipping a head
        self._countWins = 0                         # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0                             # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:                # if the series is ..., T, T, H
                    self._countWins += 1            # increase the number of wins by 1
                count_tails = 0                     # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1                    # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games, id):
        self._id = id                               # identification of the game
        self._prob_head = prob_head                 # probability heads

        self._gameRewards = []                      # create an empty list where rewards will be stored
        self._gameLosses = []                       # create an empty list where losses will be stored

        self._n_losses = 0                          # number of losses
        self._n_games = n_games                     # number of total games
        self._prob_loss = 0                         # loss probability

    def simulation(self):
        """runs the simulated set of games"""
        for n in range(self._n_games):
            # create a new game
            game = Game(id=self._id*self._n_games+n, prob_head=self._prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

        # store and count losses
        for reward in self._gameRewards:
            if reward < 0:
                self._n_losses += 1
                self._gameLosses.append(1)
            else:
                self._gameLosses.append(0)

        return SetOfGamesOutcomes(self)              # call for outcomes

    def get_reward_list(self):
        """returns the list of game rewards"""
        return self._gameRewards

    def get_loss_list(self):
        """returns the list of losses"""
        return self._gameLosses


class SetOfGamesOutcomes:
    def __init__(self, simulated_games):

        self._simulatedGames = simulated_games

        # Summary statistics: game rewards
        self._sumStat_gameRewards = \
            Stat.SummaryStat('Game rewards', self._simulatedGames.get_reward_list())

        # Summary statistics: losses
        self._sumStat_gameProbLoss = \
            Stat.SummaryStat('Losses', self._simulatedGames.get_loss_list())

    def get_ave_reward(self):
        """returns the average reward across all games"""
        return self._sumStat_gameRewards.get_mean()

    def get_CI_reward(self, alpha):
        """returns the 95%CI for the average game reward"""
        return self._sumStat_gameRewards.get_t_CI(alpha)

    def get_prob_loss(self):
        """returns the probability of a loss (mean of losses)"""
        return self._sumStat_gameProbLoss.get_mean()

    def get_CI_probLoss(self, alpha):
        """returns the 95%CI of a loss (mean of losses)"""
        return self._sumStat_gameProbLoss.get_t_CI(alpha)


class MultipleGameSets:
    """runs multiple sets of games"""
    def __init__(self, prob_head, games_in_set, set_ids):
        self._set_id = set_ids                              # set ids
        self._prob_head = prob_head                         # probability heads
        self._gamesInSet = games_in_set                     # number of games in a set

        self._gameRewards = []                              # create an empty list where rewards will be stored
        self._gameRewardsMean = []                          # create an empty list where mean rewards will be stored

        # Summary statistics: game rewards (declaring placeholder)
        self._sumStat_gameRewardsMean = None

    def simulation(self):
        for n in self._set_id:
            # create a new set of games
            games = SetOfGames(id=n, prob_head=self._prob_head, n_games=self._gamesInSet)
            # simulate the set of games using 20 flips
            games.simulation()
            # store the rewards
            self._gameRewards.append(games.get_reward_list())
            # store average of the reward
            self._gameRewardsMean.append(games.simulation().get_ave_reward())

        # Update summary statistics: game rewards
        self._sumStat_gameRewardsMean = Stat.SummaryStat("Mean rewards", self._gameRewardsMean)

    def get_mean_reward(self):
        """returns overall mean game reward"""
        return self._sumStat_gameRewardsMean.get_mean()

    def get_PI_mean_reward(self, alpha):
        """returns prediction interval for overall mean reward"""
        return self._sumStat_gameRewardsMean.get_PI(alpha)
