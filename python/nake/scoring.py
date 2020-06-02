from run_stats import RunStats

class ScoreRun:
    """ Scores a run"""

    def __init__(self, max_length, max_num_moves, max_moves_per_food, max_value=1000000):
        self.max_length = max_length
        self.max_num_moves = max_num_moves
        self.max_moves_per_food = max_moves_per_food

        # # length, moves per food, moves made
        # self.multiplier_length = max_value / float(self.max_length)
        # self.multiplier_moves_per_food = self.multiplier_length / float(self.max_moves_per_food + 1)
        # self.multiplier_moves_made = self.multiplier_moves_per_food / float(self.max_num_moves + 1)

        # length, moves made, moves per food
        self.multiplier_length = max_value / float(self.max_length)
        self.multiplier_moves_made = self.multiplier_length / float(self.max_num_moves + 1)
        self.multiplier_moves_per_food = self.multiplier_moves_made / float(self.max_moves_per_food + 1)


    @staticmethod
    def compute_inputs(snake, food_generator):
        """ Computes __init__ class inputs """
        board = food_generator.board
        max_length = board.size
        max_num_moves = (board.size - snake.length) * snake.moves_increase_by + snake.length
        max_moves_per_food = max_num_moves / board.size
        return max_length, max_num_moves, max_moves_per_food

    @classmethod
    def from_scenario(cls, scenario, **kwargs):
        return cls(*cls.compute_inputs(scenario.snake, scenario.food_generator))

    def score_stats(self,**run_stats):
        """ Computing sore on run_stats... returning a single float value"""
        # Moves per food can been None is no food has been hit
        moves_per_food = run_stats[RunStats.MOVES_PER_FOOD] or self.max_moves_per_food
        r_moves_per_food = self.max_moves_per_food - float(moves_per_food)

        score = run_stats[RunStats.LENGTH] * self.multiplier_length
        score += r_moves_per_food * self.multiplier_moves_per_food
        score += run_stats[RunStats.MOVES_MADE] * self.multiplier_moves_made

        return score
