import random
import math
from itertools import permutations, product
import copy
from colorama import Fore, Back, Style, init

from CamelUpPlayer import CamelUpPlayer

class CamelUpBoard:
    def __init__(self, camel_styles: list[str]):
        self.TRACK_POSITIONS = 16
        self.DICE_VALUES = [1,2,3]
        self.BETTING_TICKET_VALUES = [5, 3, 2, 2]
        
        self.camel_styles = camel_styles
        self.camel_colors = camel_styles.keys()
        self.track = self.starting_camel_positions()
        self.pyramid = set(self.camel_colors)
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = [] #preserves order

    def starting_camel_positions(self)->list[list[str]]:
        '''Places camels on the board at the beginning of the game
            TODO: randomize these positions

            Return
               list[list[str]] - a 2D list model of the Camel Up race track
        '''
        track = [[] for i in range(self.TRACK_POSITIONS)]
        track[0] = list(self.camel_colors)
        random.shuffle(track[0])
        return track
    
    def print(self, players: list[CamelUpPlayer]):
        '''Prints the current state of the Camel Up board, including:
            - Race track with current camel positions
            - Betting Tents displaying available betting tickets
            - Dice Tents displaying an ordered collection of rolled dice
            - Player information for both players
                - name
                - coins
                - betting tickets for the current leg of the race
        '''
        board_string = "\n"
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.camel_styles[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.camel_styles[die[0]]+str(die[1])+Style.RESET_ALL+" "

        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "
        
        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.camel_styles[camel]+ camel +  Style.RESET_ALL 
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])+"\n"

        #Player Info
        player_string=""
        for player in players:
            player_string+=f"{player.name} has {player.money} coins."
            if len(player.bets)>0:
                bets_string = " ".join([self.camel_styles[bet[0]]+str(bet[1])+Style.RESET_ALL for bet in player.bets])
                player_string += f" Bets: {bets_string}"  
            player_string+="\t\t" 
        
        board_string+=player_string
        print(board_string+"\n")

    def reset_tents(self):
        '''Rests dice tents and ticket tents at the end of a leg
        '''
        self.ticket_tents = {color:self.BETTING_TICKET_VALUES.copy() for color in self.camel_colors}
        self.dice_tents = []

    def place_bet(self, color:str)->tuple[str, int]:
        '''Manages the board perspective when a player places a bet:
            - removes the top betting ticket (with highest value) from the appropriate Ticket Tent
            - returns the ticket

            Args
               color (str) - the color of the ticket on which a player would like to bet: 'r'
           
            Return
                tuple(str, int) - a tuple representation of a betting ticket: ('r', 5)
        '''
        tickets_left = self.ticket_tents[color]
        ticket = ()
        if len(tickets_left)>0:
            ticket =(color, tickets_left[0])
            self.ticket_tents[color] = tickets_left[1:]
        return ticket

    def move_camel(self, die:tuple[str, int], verbose=False):
        '''Updates the track according to the die color and value
           The camel of the appropriate color moves the apporpriate number of spaces, 
           along with all camels riding on top of that camel.

           Args
             die (tuple[str, int]) - A tuple represntation of the die: ('g', 2)

           Return
             list[list[str]] - a 2D list model of the Camel Up race track
        '''
        if verbose: print("Current track state:", self.track)
        ### BEGIN SOLUTION

        camel_to_move = die[0]
        num_steps = die[1]
        camel_pos = None
        camel_height = None
        for position_index, track_position in enumerate(self.track):
            if camel_to_move in track_position:
                camel_pos = position_index
                camel_height = track_position.index(camel_to_move)
                break
        new_position = camel_pos + num_steps
        if new_position >= len(self.track):
            new_position = len(self.track) - 1
        camels_to_move = self.track[camel_pos][camel_height:]
        self.track[camel_pos] = self.track[camel_pos][:camel_height]
        self.track[new_position].extend(camels_to_move)


        ### END SOLUTION
        if verbose: print("Updated track state:", self.track)
        return self.track
    
    def shake_pyramid(self)->tuple[str, int]:
        '''Manages all the steps (from the board persepctive) involved with shaking the pyramid, 
           which includes:
                - selecting a random color and dice value from the dice colors in the pyramid
                - removing the rolled dice from the pyramid
                - placing the rolled dice in the dice tents

            Return
                tuple[str, int] - A tuple representation of the rolled die
        '''
        rolled_die=("", 0)
        ### BEGIN SOLUTION

        if not self.pyramid:
            return rolled_die
        choose_color = random.choice(list(self.pyramid))
        self.pyramid.remove(choose_color)
        die_value = random.choice(self.DICE_VALUES)
        self.dice_tents.append((choose_color, die_value))
        rolled_die = (choose_color, die_value)

        ### END SOLUTION
        return rolled_die

    def is_leg_finished(self)->bool:
        '''Determines whether the leg of a race is finished

           Return
             bool - True if all dice have been rolled, False otherwise
        '''
        ### BEGIN SOLUTION

        return len(self.pyramid) == 0

        ### END SOLUTION

    def get_rankings(self):
        '''Determines first and second place camels on the track
           
           Returns:
            tuple: a tuple of strings of (1st, 2nd) place camels: ('b', 'y') 
        '''
        rankings = ("", "")
        ### BEGIN SOLUTION
        
        camel_order = []
        for position in reversed(self.track):
            if position:
                camel_order.extend(reversed(position))
        if len(camel_order) > 1:
            rankings = (camel_order[0], camel_order[1])
        elif len(camel_order) == 1:
            rankings = (camel_order[0], "")
        

        ### END SOLUTION
        return rankings

    def get_all_dice_roll_sequences(self)-> set:
        '''
            Constructs a set of all possible roll sequences for the dice currently in the pyramid
            Note: Use itertools product function

            Return
               set[tuple[tuple[str, int]]] - A set of tuples representing all the ordered dice seqences 
                                             that could result from shaking all dice from the pyramid
        ''' 
        roll_space = set()
        ### BEGIN SOLUTION
        
        remaining_dice = list(self.pyramid)
        dice_combinations = []
        for color in remaining_dice:
            for value in self.DICE_VALUES:
                dice_combinations.append((color, value))
        all_sequences = product(dice_combinations, repeat=len(remaining_dice))
        for sequence in all_sequences:
            roll_space.add(tuple(sequence))
    
        
        ### END SOLUTION
        
        return roll_space
    
    def run_enumerative_leg_analysis(self)->dict[str, tuple[float, float]]:
        '''Conducts an enumerative analysis of the probability that each camel will win either 1st or 
           2nd place in this leg of the race. The enumerative analysis counts 1st/2nd place finishes 
           via calculating the entire state space tree

           General Steps:
                1) Precalculate all possible dice sequences for the dice currently in the pyramid
                2) Move through each sequence of possible dice rolls to count the number of 1st/2nd places 
                   finishes for each camel
                3) Calculates the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of dice sequences

                TODO: Add notes about using deepcopy to preserve state
           
           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents = {color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION

        all_sequences = self.get_all_dice_roll_sequences()
        total_sequences = len(all_sequences)
        counts = {color: [0, 0] for color in self.camel_colors}
        for sequence in all_sequences:
            track_copy = copy.deepcopy(self.track)
            for die in sequence:
                self.move_camel(die)
                rankings = self.get_rankings()
            if rankings[0]:
                counts[rankings[0]][0] += 1
            if rankings[1]:
                counts[rankings[1]][1] += 1
        for color in self.camel_colors:
            first_count, second_count = counts[color]
            win_percents[color] = (first_count / total_sequences, second_count / total_sequences)
            
        ### END SOLUTION

        return win_percents


    def run_experimental_leg_analysis(self, trials:int)->dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimenta analysis counts 
            1st/2nd place finishes bycounting outcomes from randomly shaking the pyramid over a given 
            number of trials.
           
           General Steps:
                1) Shake the pyramid enough times to randomly generate a dice sequence to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total 
                   number of 1st/2nd finishes out of the total number of trials

                TODO: Add notes about using deepcopy to preserve state

           Args
              trials (int): The number of random simulations to conduct

           Returns: 
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will 
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        win_percents={color:(0, 0) for color in self.camel_colors}
        ### BEGIN SOLUTION
        pract = copy.deepcopy(self.track)
        keep = copy.deepcopy(self.dice_tents)
        pyr = self.pyramid
        winlist = []
        finaldictwin = {}
        finaldicttwo = {}
        win_percents = {}
        for i in range(trials):
            pract = copy.deepcopy(self.track)
            keep = copy.deepcopy(self.dice_tents)
            while len(self.pyramid) > 0:
                shake = self.shake_pyramid()
                self.move_camel(shake)
            winlist.append(self.get_rankings())
            self.pyramid = pyr
            self.track = pract
            self.dice_tents = keep
        for x in winlist:
            if x[0] not in finaldictwin:
                finaldictwin[x[0]] = 1
            else:
                finaldictwin[x[0]] += 1
            if x[1] not in finaldicttwo:
                finaldicttwo[x[1]] = 1
            else:
                finaldicttwo[x[1]] += 1
        for a in self.camel_colors:
            if a in finaldictwin.keys() and a in finaldicttwo.keys():
                win_percents[a] = ((((finaldictwin.get(a))/trials)), ((finaldicttwo.get(a))/trials))
            elif a in finaldictwin.keys():
                win_percents[a] = (((finaldictwin.get(a))/trials), 0.0)
            elif a in finaldicttwo.keys():
                win_percents[a] = (0.0, ((finaldicttwo.get(a))/trials))
            else: 
                win_percents[a] = (0.0, 0.0)

        self.pyramid = pyr
        self.track = pract
        self.dice_tents = keep
        ### END SOLUTION
        return win_percents
   
   
if __name__ == "__main__":
    camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = CamelUpBoard(camel_styles)
    p1 = CamelUpPlayer("p1")
    p2 = CamelUpPlayer("p2")
    board.print([p1, p2])
    die = ('b', 1)
    board.move_camel(die)
    #Roll 3 random dice
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    rolled_die = board.shake_pyramid()
    board.move_camel(rolled_die)
    board.print([p1, p2])
    #Probabilites
    all_possible_dice_sequences= board.get_all_dice_roll_sequences()
    print(f"{len(all_possible_dice_sequences)} possible dice sequences for {len(board.pyramid)} dice in the pyramid:") 
    print("Enumerative Probabilities:", board.run_enumerative_leg_analysis())
    print("Experimental Probabilities:", board.run_experimental_leg_analysis(5000))
