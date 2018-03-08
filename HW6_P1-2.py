import Working_Model as Classes

# run 1,000 simulated games
setOfGames = Classes.SetOfGames(prob_head=0.5, n_games=1000, id=1)
outcomes = setOfGames.simulation()

# Problem 1. 95%CI for expected reward and loss probability
print('Game rewards:')
print('The expected mean game reward is:', outcomes.get_ave_reward())
print('The 95%CI for the expected mean game reward is:', outcomes.get_CI_reward(alpha=0.05))

print('Losses:')
print('The expected probability of losing a game is:', outcomes.get_prob_loss())
print('The 95%CI for the expected probability of losing a game is:', outcomes.get_CI_probLoss(alpha=0.05))

# Problem 2. Interpret the 95%CI
print('Interpretation:')
print('Were we to run the simulation multiple times (or were we to observe such a set of games multiple times), '
      'on average, 95% of the calculated confidence intervals would cover the true unknown game reward mean.')

print('We interpret the 95%CI of the expected probability of a loss in much the same way. '
      'On average, we expect that 95% of the calculated confidence intervals will include the true unknown '
      'probability of a loss, "the loss mean."')