import Working_Model as Working_Model

# Problem 3. Owners & Players
print('We view the casino owner playing multiple games as a system in a steady-state.')
print('He/She cares about the average winnings of an individual player and the precision of that claim.')
print('Assuming that the Law of Large Numbers holds, we report the mean and 95%CI '
      'looking for negative values (times when the house wins).')

casino_owner = Working_Model.SetOfGames(prob_head=0.5, n_games=10000, id=1)
casino_ownerOutcomes = casino_owner.simulation()            # assumming 10,000 games

print('Values:')
print('The expected loss per player is:', casino_ownerOutcomes.get_ave_reward())
print('The 95%CI of the expected loss per player is:', casino_ownerOutcomes.get_CI_reward(alpha=0.05))

print('Interpretation:')
print('Per game, the anticipated average earnings for the owner are +$24.1x. '
      'Were mulitple games to occur, we expect that the true average house winnings per player '
      'would be within the range +$26.00 to +$22.20 95% of the time.')

print('We view the gambler as a system in a transient-state.')
print('Based on the limited number of times that the gambler plays the game, we report the sample mean '
      'and 95% projection interval.')

MultipleGameSets = Working_Model.MultipleGameSets(prob_head=0.5, games_in_set=10, set_ids=range(1000))
MultipleGameSets.simulation()       # running the simulation 1,000 times

print('Values:')
print('The projected mean game reward is:', MultipleGameSets.get_mean_reward())
print('The 95% projection interval is:', MultipleGameSets.get_PI_mean_reward(alpha=0.05))

print('Interpretation:')
print('On average, the gambler can expect to lose -$24.14. His/Her earnings'
      ' are anticipated to fall within the range of -$80.00 to +$40.00 with 95% certainty.')



