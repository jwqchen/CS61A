"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Helper Functions #
######################

def get_digit(n, *argv):
    """Retruns a list of digits of N, in the order specified by *arg

    n:      the number of interest
    *arg:   position of the digit(s) wanted, digit position counts right to left. So the right-most digit has position 1.

    >>> get_digit(21, 1, 2)
    [1, 2]
    >>> get_digit(21, 2, 1)
    [2, 1]
    >>> get_digit(124, 3, 1)
    [1, 4]
    >>> get_digit(236, 2, 5 ,2)
    [3, 0, 3]
    >>> get_digit(253654364, 6)
    [6]
    >>> get_digit(12782975, 5)
    [8]
    >>> get_digit(0, 1)
    [0]
    >>> get_digit(0, 2)
    [0]
    >>> get_digit(134, 7)
    [0]
    >>> get_digit(56, 3)
    [0]
    """
    def get_digit(digit_position):
        assert digit_position > 0, "position needs to be an integer greater than 0"
        return n % (10**digit_position) // (10**(digit_position-1))

    lst = [get_digit(digit_position) for digit_position in argv]
    return lst


def roll_once(strategy, score, score_opponent, dice):
    """
    returns SCORE0 and SCORE1 after a player has played in a turn
    """
    # print("roll_once")
    num_dice = strategy(score, score_opponent)
    # print("strategy returns", num_dice)
    turn_score = take_turn(num_dice, score_opponent, dice)
    # print("turn_score", turn_score)
    score += turn_score
    # print("score", score)
    if turn_score == 0:
        score_opponent += num_dice
        # print("score_opponent", score_opponent)
    return score, score_opponent


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    n = 1
    sum_rolls = 0
    has_one = False
    while n <= num_rolls:
        num = dice()
        if num == 1:
            has_one = True
        sum_rolls += num
        n += 1
    if has_one == True:
        return 0
    else:
        return sum_rolls
    # END Question 1


def is_prime(n):
    '''returns True if N is a prime number, False otherwise
    >>> is_prime(1)
    False
    >>> is_prime(0)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(10)
    False
    >>> is_prime(101)
    True
    '''
    assert type(n) == int, 'n must be an integer.'
    assert n >= 0, 'n must be equal to or greater than 0.'    
    if n == 1 or n == 0:
        return False
    i = 2
    while i < n:
        if n%i == 0:
            return False
        i += 1
    return True


def next_prime(n):
    '''return the next prime number greater than n
    >>> next_prime(2)
    3
    >>> next_prime(101)
    103
    >>> next_prime(13)
    17
    >>> next_prime(19)
    23
    >>> next_prime(97)
    101
    >>> next_prime(31)
    37
    '''
    assert type(n) == int, 'n must be an integer.'
    assert is_prime(n), "n must be a prime number"
    test_num = n + 1
    while True:
        if is_prime(test_num):
            return test_num
        test_num += 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # print("***from take_turn, num_rolls", num_rolls)
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        (first_digit, second_digit) = get_digit(opponent_score, 1, 2)
        # first_digit = opponent_score % 10
        # second_digit = opponent_score // 10
        score = max(first_digit, second_digit) + 1
        # print("in take_turn, score is", score)

    else:
        score = roll_dice(num_rolls, dice)
    if is_prime(score):
        score = next_prime(score)
    return score
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    sum = score + opponent_score
    if sum % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3



def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    (score0_first, score0_second) = get_digit(score0, 1, 2)
    (score1_first, score1_second) = get_digit(score1, 1, 2)
    if score0_first == score1_second and score1_first == score0_second:
        return True
    else:
        return False 
    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    while True:
        dice_choice = select_dice(score0, score1)
        # print("player", who)
        if who == 0:
            score0, score1 = roll_once(strategy0, score0, score1, dice_choice)
        else:
            score1, score0 = roll_once(strategy1, score1, score0, dice_choice)

        if is_swap(score0, score1):
            temp_value = score0
            score0 = score1
            score1 = temp_value
            # print("final score0", score0)

            # print("final score1", score1)

        # print("score0: ", score0)
        # print("score1: ", score1)
        if score0 >= goal or score1 >= goal:
            break        
        who = other(who)
        # print("here")
        # print("player for next round", who)
    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def inner(*arg):
        i = 0
        sum_results = 0
        while i < num_samples:
            sum_results += fn(*arg)
            i += 1
        return sum_results/num_samples
    return inner
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=10000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    averaged_roll_dice = make_averaged(roll_dice, num_samples)
    i = 1
    temp_max = 0
    num_dice = 1
    while i <=10:
        average = averaged_roll_dice(i, dice)
        if average > temp_max:
            num_dice = i
            temp_max = average
        i += 1
    #delete print!!!!!
    # print("final_max", temp_max)
    return num_dice
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if 0:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if 0:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if 0:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if 0:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))
    
    if 0:  # Change to True to test final_strategy
        # print("final_strategy return", final_strategy(1, 2))
        print('final_strategy_original win rate:', average_win_rate(final_strategy_original))

    if 1:  # Change to True to test final_strategy
        # print("final_strategy return", final_strategy(1, 2))
        print('final_strategy win rate:', average_win_rate(final_strategy))

    # optimization code for meta_final: I ran this and chose the highest params for meta_final to generate my final_strategy
    for four_sided_cutoff in range(2,5):
        for four_sided_count in range(2,4):
            for six_sided_cutoff in range(3,6):
                for six_sided_count in range(3,6):
                    print("%d, %d, %d, %d " % (four_sided_cutoff, four_sided_count, six_sided_cutoff, six_sided_count), 'toshiro_strategy win rate:', average_win_rate(meta_final(four_sided_cutoff, four_sided_count, six_sided_cutoff, six_sided_count)))


    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    zero_roll = take_turn(0, opponent_score)
    if zero_roll >= margin:
        return 0
    else:
        return num_rolls
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    zero_roll_score = take_turn(0, opponent_score)
    zero_roll_total_score = score + zero_roll_score
    if is_swap(zero_roll_total_score, opponent_score):
        if opponent_score > zero_roll_total_score:
            return 0
        else:
            return num_rolls
    else:
        return num_rolls
    # END Question 9

#this is wenqin's original strategy, gets to about .75
def final_strategy_original(score, opponent_score, goal=GOAL_SCORE):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN Question 10
    num_rolls = 4
    margin = 3
    zero_roll_score = take_turn(0, opponent_score)
    zero_roll_total_score = score + zero_roll_score

    if (goal - score) <= zero_roll_score:
        return 0


    roll_dice_strategy_delta = 0
    bacon_strategy_delta = zero_roll_score - margin
    swap_strategy_delta = opponent_score - zero_roll_total_score


    max_delta = max(roll_dice_strategy_delta, bacon_strategy_delta, swap_strategy_delta)

    if max_delta == bacon_strategy_delta:
        return 0
    elif max_delta == roll_dice_strategy_delta:
        return num_rolls
    else:
        return 0

def meta_final(four_sided_cutoff, four_sided_count, six_sided_cutoff, six_sided_count):
    def final_strategy(score, opponent_score, goal=GOAL_SCORE):
        # calculate zero roll
        (first_digit, second_digit) = get_digit(opponent_score, 1, 2)
        
        base_zero_roll_score = max(first_digit, second_digit) + 1

        if is_prime(base_zero_roll_score):
            base_zero_roll_score = next_prime(base_zero_roll_score)

        if (goal - score) <= base_zero_roll_score:
            return 0

        effective_zero_score = base_zero_roll_score

        if base_zero_roll_score + score + opponent_score % 7 == 0:
            effective_zero_score += 4

        if is_swap(base_zero_roll_score + score, opponent_score): 
            effective_zero_score += opponent_score - (base_zero_roll_score + score)
        
        if (score + opponent_score) % 7 == 0:
            if effective_zero_score > four_sided_cutoff:
                return 0
            else:
                return four_sided_count
        else:
            if effective_zero_score > six_sided_cutoff:
                return 0
            else:
                return six_sided_count
    return final_strategy

final_strategy = meta_final(2,3,4,4)
 #final_strategy = meta_final(4,3,5,4)


#why didn't the following code work?
    # if zero_roll_score >= margin:
    #     return 0
    # elif is_swap(zero_roll_total_score, opponent_score):
    #     if opponent_score > zero_roll_total_score:
    #         return 0
    # else:
    #    return num_rolls


    # bacon_strategy(score, opponent_score, 7, 6)

    # swap_strategy(score, opponent_score, 6)

    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
