import pytest

from src.bee_classes import BeeParameters,Word,SolutionList,Puzzle
from src.nytbee_classes import NytBee_Parameters,NytBee_Solution
import datetime

def test_nytbee_puzzle_input_construction():
    s = NytBee_Solution(date=datetime.date(2023,1,25))
    s.get_puzzle_from_input(puzzle=Puzzle(center_tile='m',petal_tiles=['n','w','e','d','l','i'],
                date_str='2023-01-25',solution=['mildew','mildewed','mine','mien','mild']))
    assert s.puzzle.datestr() == '2023-01-25'
    assert s.puzzle.solution.make_list() == ['MIEN', 'MILD', 'MILDEW', 'MILDEWED', 'MINE']

def test_nytbee_puzzle_date_wrong():
    with pytest.raises(ValueError) as e:
        NytBee_Solution(date=datetime.date(2001,1,25))
    assert str(e.value) == f"NytBee_Solution 2001-01-25 must be between 2018-07-29 and today"
