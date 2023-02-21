from dataclasses import dataclass
from typing import List, Dict, Union
import string
from datetime import datetime

class BeeParameters:
    max_tiles = 7
    min_tiles = 4
    
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    
@dataclass
class Word:
    word: str

    def __post_init__(self):
        non_alpha = set(self.word).difference(set(string.ascii_letters))
        if len(non_alpha)>0:
            raise ValueError(f'Word {self.word} can only contain letters: {"".join(sorted("".join(non_alpha)))}')
        elif len(self.word)<BeeParameters.min_tiles:
            raise ValueError(f'Word {self.word} contains too few letters')
        elif len(set(self.word))>BeeParameters.max_tiles:
            raise ValueError(f'Word {self.word} has too many letters')
        self.word = self.word.upper()

    def __str__(self):
        return(f'{self.word}')

    def string(self):
        return(f'{self.word}')
    
    def alphagram(self):
        return(''.join(sorted(list(set(self.word)))))
    
    def alphabet(self):
        return(''.join(sorted(self.word)))
    
    def count(self):
        return(len(self.word))
    
    def countdistinct(self):
        return(len(set(self.word)))
    
    def value(self):
        if len(self.word) < BeeParameters.min_tiles:
            return(0)
        elif len(self.word) == BeeParameters.min_tiles:
            return(1)
        else:
            return(len(self.word))
    
@dataclass
class SolutionList:
    solution: Union[List, List[Word]]
        
    def __post_init__(self):
        if isinstance(self.solution,List):
            new_solution = []
            for w in self.solution:
                if not isinstance(w,Word):
                    w1 = Word(w)
                    new_solution.append(Word(w))
                else:
                    new_solution.append(w)
            letter_set = set()
            for w in new_solution:
                letter_set=letter_set.union(set(w.string()))
            if len(letter_set)>BeeParameters.max_tiles:
                raise ValueError(f'SolutionList {new_solution} has too many letters {"".join(sorted("".join(letter_set)))}, must have <= {BeeParameters.max_tiles}')
            self.solution = new_solution
        else:
            raise ValueError(f'Must supply a list for the solution')
        # initialization always results in a sorted list. 
        self.solution = self.sort_SolutionList()
            
    def __str__(self):
        prt_str = '\n'.join([w.word for w in self.solution])
        return prt_str
    
    def sort_SolutionList(self):
        return [x for _, x in sorted(zip(self.make_list(), self.solution))]
    
    def make_list(self):
        made_list = []
        for word in self.solution:
            made_list.append(word.string())
        return made_list


@dataclass
class Puzzle:
    center_tile: float
    petal_tiles: list
    solution: SolutionList
    date_str: str
    date_format = '%Y-%m-%d'
        
    def __post_init__(self):
        self.center_tile = self.center_tile.upper()
        self.petal_tiles = sorted([l.upper() for l in list(set(self.petal_tiles))])
        if len(self.petal_tiles) != (BeeParameters.max_tiles-1) or len(self.center_tile) != 1 or len(set(self.petal_tiles).union(set(self.center_tile)))!=BeeParameters.max_tiles:
            raise ValueError(f'Error in puzzle specification {self.center_tile} length {len(self.center_tile)}; {self.petal_tiles} length {len(self.petal_tiles)}')
        if not isinstance(self.solution,SolutionList):
            self.solution = SolutionList(self.solution)
        # test that all words are valid
        for word in self.solution.solution:
            if (self.center_tile not in word.word) or (len(set(word.word).difference(set(self.petal_tiles).union(set(self.center_tile))))>0):
                raise ValueError(f'Input list contains invalid word {word} for tiles {self.center_tile} {self.petal_tiles} ')
        try:
            self.date = datetime.strptime(self.date_str, self.date_format)
        except:
            raise ValueError(f'Date string {self.date_str} does not match expected date format {self.date_format} ')

        
    def __str__(self):
        prt_str = (f"{color.UNDERLINE}{self.center_tile}{color.END}{''.join(self.petal_tiles)}\n"
                  f"{self.date_str}\n"
                  f"{self.solution}\n")
        return prt_str
    
    
    def alphagram_solutions(self):
        alph_dict = {}
        for word in self.solution.solution:
            key = word.alphagram()
            if key in alph_dict.keys():
                alph_dict[key].append(word)
            else:
                alph_dict[key]=[word]
        return alph_dict
    
    def datestr(self):
        return(self.date.strftime("%Y-%m-%d"))




