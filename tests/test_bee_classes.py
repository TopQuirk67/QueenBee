import pytest

from src.bee_classes import BeeParameters,Word,SolutionList,Puzzle
import string

def test_valid_alphagram_lengths():
    assert BeeParameters.max_tiles == 7 and BeeParameters.min_tiles == 4, "Test max and min lengths; tests will need to be refactored if these vary"

def test_word_construction():
    assert Word(word='abcd').word == 'ABCD'

def test_error_word_non_letters():
    word = 'ab:*dg'
    with pytest.raises(ValueError) as e:
        Word(word=word)
    assert str(e.value) == "Word ab:*dg can only contain letters: *:"   

def test_error_word_too_few_letters():
    word = string.ascii_letters[:BeeParameters.min_tiles-1]
    with pytest.raises(ValueError) as e:
        Word(word=word)
    assert str(e.value) == f"Word {word} contains too few letters"   

def test_error_word_too_many_letters():
    word = string.ascii_letters[:BeeParameters.max_tiles+1]
    with pytest.raises(ValueError) as e:
        Word(word=word)
    assert str(e.value) == f"Word {word} has too many letters"

def test_solution_list_contruction():
    assert SolutionList(['mildew','mildewed','mine','mien']).make_list() == ['MIEN', 'MILDEW', 'MILDEWED', 'MINE']

def test_solution_error_list_alphagram_too_long():
    with pytest.raises(ValueError) as e:
        sample_SolList = SolutionList(['mildew','mildewed','mine','mien','quoin'])
    assert str(e.value) == "SolutionList [Word(word='MILDEW'), Word(word='MILDEWED'), Word(word='MINE'), Word(word='MIEN'), Word(word='QUOIN')] has too many letters DEILMNOQUW, must have <= 7"

def test_puzz_contstruction_center_petal():
    test_puzz = Puzzle(center_tile='m',petal_tiles=['n','w','e','d','l','i'],
                date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])    
    assert test_puzz.solution.make_list()==['MIEN', 'MILDEW', 'MILDEWED', 'MINE'] and test_puzz.date_str=='2023-01-25' and \
                test_puzz.petal_tiles == ['D', 'E', 'I', 'L', 'N', 'W'] and test_puzz.center_tile == 'M'
    
def test_puzz_contstruction_tiles():
    test_puzz = Puzzle(tiles='mnwedli',
                    date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])
    assert test_puzz.solution.make_list()==['MIEN', 'MILDEW', 'MILDEWED', 'MINE'] and test_puzz.date_str=='2023-01-25' and \
                test_puzz.petal_tiles == ['D', 'E', 'I', 'L', 'N', 'W'] and test_puzz.center_tile == 'M' \
                and test_puzz.tiles == 'MDEILNW' 
    
def test_puzz_contstruction_center_petal_str():
    test_puzz = Puzzle(center_tile='m',petal_tiles=list('nwedli'),
                    date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])
    assert test_puzz.solution.make_list()==['MIEN', 'MILDEW', 'MILDEWED', 'MINE'] and test_puzz.date_str=='2023-01-25' and \
                test_puzz.petal_tiles == ['D', 'E', 'I', 'L', 'N', 'W'] and test_puzz.center_tile == 'M' \
                and test_puzz.tiles == 'MDEILNW' 

def test_puzz_error_center_petal_plus_tiles():
    with pytest.raises(ValueError) as e:
        test_puzz = Puzzle(center_tile='m',petal_tiles=list('nwedli'),tiles='mnwedli',
                        date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])
    assert str(e.value) == "Must contain tile specification through either tiles mnwedli or center+petal tiles m ['n', 'w', 'e', 'd', 'l', 'i'] "

def test_puzz_error_center_plus_tiles():
    with pytest.raises(ValueError) as e:
        test_puzz = Puzzle(center_tile='m',tiles='mnwedli',
                        date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])
    assert str(e.value) == "Must contain tile specification through either tiles mnwedli or center+petal tiles m None "

def test_puzz_error_petal_plus_tiles():
    with pytest.raises(ValueError) as e:
        test_puzz = Puzzle(petal_tiles=list('nwedli'),tiles='mnwedli',
                        date_str='2023-01-25',solution=['mildew','mildewed','mine','mien'])
    assert str(e.value) == "Must contain tile specification through either tiles mnwedli or center+petal tiles None ['n', 'w', 'e', 'd', 'l', 'i'] "

def test_puzz_error_date():
    with pytest.raises(ValueError) as e:
        Puzzle(center_tile='m',petal_tiles=['n','w','e','d','l','i'],
                date_str='2023-21-25',solution=['midew','midewed','mine','mien'])
    assert str(e.value) == "Date string 2023-21-25 does not match expected date format %Y-%m-%d "
    
def test_puzz_error_too_short():
    with pytest.raises(ValueError) as e:
        Puzzle(center_tile='m',petal_tiles=['n','w','e','d','i'],
                date_str='2023-01-25',solution=['midew','midewed','mine','mien'])
    assert str(e.value) == "Error in puzzle specification M length 1; ['D', 'E', 'I', 'N', 'W'] length 5"

def test_puzz_error_too_long():
    with pytest.raises(ValueError) as e:
        Puzzle(center_tile='m',petal_tiles=['n','w','e','d','l','i','h'],
                date_str='2023-01-25',solution=['mildew','mildewed','mine','mien','hind'])
    assert str(e.value) == "Error in puzzle specification M length 1; ['D', 'E', 'H', 'I', 'L', 'N', 'W'] length 7"

def test_puzz_error_solution_invalid():
    with pytest.raises(ValueError) as e:
        Puzzle(center_tile='m',petal_tiles=['n','w','e','d','l','i'],
                date_str='2023-01-25',solution=['mildew','mildewed','mine','mien','hind'])
    assert str(e.value) == "SolutionList [Word(word='MILDEW'), Word(word='MILDEWED'), Word(word='MINE'), Word(word='MIEN'), Word(word='HIND')] has too many letters DEHILMNW, must have <= 7"
