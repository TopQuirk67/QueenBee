from dataclasses import dataclass, field
from src.google_sheet_classes import Google_Sheet
from src.utils import recursive_waiter
from typing import List, Dict, Union
import string
from datetime import datetime, timedelta
from src.utils import Color
import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd

# Classes related to the spelling bee puzzle
# https://www.nytimes.com/puzzles/spelling-bee
class BeeParameters:
    max_tiles = 7
    min_tiles = 4


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
            if len(set(self.word))==BeeParameters.max_tiles:
                return(len(self.word))+BeeParameters.max_tiles
            else:    
                return(len(self.word))
            
    def validinpuzzle(self,puzzle_tiles):
        p = puzzle_tiles.upper()
        if len(set(self.alphagram()).intersection(set(p)))==self.countdistinct() and p[0] in self.alphagram():
            return True
        else:
            return False
    
    
@dataclass
class SolutionList:
    solution: Union[List, List[Word]]
    alphagram_dictionary: dict = None
        
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
        self.alphagram_dictionary = self.compile_alphagram_dictionary()
        self.nwords = self.nwords()
        self.points = self.points()
            
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

    def make_list_to_string(self):
        return ' '.join(self.make_list())
    
    def compile_alphagram_dictionary(self):
        alphagram_dictionary={}
        for word in self.solution:
            if word.alphagram() in alphagram_dictionary.keys():
                alphagram_dictionary[word.alphagram()].append(word)
            else:
                alphagram_dictionary[word.alphagram()] = [word]
        return alphagram_dictionary

    def nwords(self):
        return len(self.make_list())
    
    def points(self):
        return sum([w.value() for w in self.solution])
        



@dataclass
class Puzzle:
    solution: SolutionList
    date_str: str
    center_tile: str = None
    petal_tiles: list = None
    tiles: str = None
    date_format = '%Y-%m-%d'
        
    def __post_init__(self):
        if (self.tiles is None) and (self.center_tile is None or self.petal_tiles is None):
            raise ValueError(f'Must contain tile specification through either tiles {self.tiles} or center+petal tiles {self.center_tile} {self.petal_tiles} ')
        elif (self.tiles is not None) and ((self.center_tile is not None) or (self.petal_tiles is not None)):
            raise ValueError(f'Must contain tile specification through either tiles {self.tiles} or center+petal tiles {self.center_tile} {self.petal_tiles} ')
        elif (self.tiles is None):
            if (self.petal_tiles is None) or (self.petal_tiles is None):
                raise ValueError(f'Must contain tile specification center+petal tiles {self.center_tile} {self.petal_tiles} ')
            else:            
                self.center_tile = self.center_tile.upper()
                self.petal_tiles = sorted([l.upper() for l in list(set(self.petal_tiles))])
                self.tiles = self.center_tile+''.join(self.petal_tiles)
        else:
            self.center_tile = self.tiles[0].upper()
            self.petal_tiles = sorted(list(self.tiles[1:].upper()))
            self.tiles = self.center_tile+''.join(self.petal_tiles)
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
        prt_str = (f"{Color.UNDERLINE}{self.center_tile}{Color.END}{''.join(self.petal_tiles)}\n"
                  f"{self.tiles}\n"
                  f"{self.date_str}\n"
                  f"{self.solution}\n")
        return prt_str    
    
    def alphagram_solutions(self):
        return self.solution.alphagram_dictionary
    
    def datestr(self):
        return(self.date.strftime(self.date_format))

# Classes related to the solutions website
# nytbee.com

class NytBee_Parameters:
    start_date = datetime(2018, 7, 29)

@dataclass
class NytBee_Solution:
    date: datetime
    date_str: str = None
    waiter_settings: Dict = field(default_factory=lambda: {'maxdepth': 3, 'scaler':1, 'phighbin':0.2,'precursion':0.5})

    def __post_init__(self):
        if not isinstance(self.date,datetime):
            raise ValueError(f'NytBee_Solution {self.date} must be a datetime')
        elif self.date < NytBee_Parameters.start_date or self.date > datetime.today():
            print(f'NytBee_Solution {self.date} must be between {NytBee_Parameters.start_date} and today')
        self.puzzle = None

    def __str__(self):
        return f'NytBee_Solution for {self.datestring()}\n {self.urlstring()}\n {self.puzzle}'
    
    def datestring(self):
        (year, month, day) = (self.date.year, self.date.month, self.date.day)
        return f'{year:02d}{month:02d}{day:02d}'
    
    def urlstring(self):
        return f'https://nytbee.com/Bee_{self.datestring()}.html'
    
    def get_puzzle_from_url(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        if self.waiter_settings is not None:
            recursive_waiter(**self.waiter_settings)
        page = requests.get(self.urlstring(), headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        if page.status_code != 200:
            f'Error fetching page {self.urlstring()}'
            self.puzzle = None
            return None
        
        x = soup.find('script', type='text/javascript')
        if (x):
            regex = 'var docs_json = \'(.+?)\';'
            y = json.loads(re.findall(regex,str(x))[0])
            keys = [k for k in y.keys()]
            key = keys[0]

            for item in y[key]['roots']['references']:
                if ('data' in item['attributes'].keys()):
                    if ('words' in item['attributes']['data'].keys()):
                        todays_lists = item['attributes']['data']['words']
                    elif ('tips' in item['attributes']['data'].keys()):
                        todays_lists = item['attributes']['data']['tips']
                    else:
                        print(f'Error can\'t find word list from nytbee')
                        self.puzzle = None
            nytbee = {}
            all_words = []
            for list_nletters in todays_lists:
                if len(list_nletters)>0:
                    nletters = len(list_nletters[0])
                    nwords   = len(list_nletters)
                    for word in list_nletters:
                        all_words.append(word)
                    nytbee[nletters]=nwords
                    
            x1 = soup.find_all('script', type='text/javascript')
            if len(x1)>=5:
                x1 = x1[5]
                regex = 'var docs_json = \'(.+?)\';'
                y1 = json.loads(re.findall(regex,str(x1))[0])
                key = [k for k in y1.keys()][0]
                for item in y1[key]['roots']['references']:
                    if 'data' in item['attributes'].keys():
                        center_tile = (chr(item['attributes']['data']['color'].index('firebrick')+ord('a')))

                x2 = soup.find_all('script', type='text/javascript')[6]
                y2 = json.loads(re.findall(regex,str(x2))[0])
                key = [k for k in y2.keys()][0]
                for item in y2[key]['roots']['references']:
                    if 'data' in item['attributes'].keys():
                        colors = item['attributes']['data']['color']
                        puzz_tiles = [chr(idx+ord('a')) for idx,color in enumerate(colors) if color=='firebrick']
                        # center_tile = (chr(item['attributes']['data']['color'].index('firebrick')+ord('a')))
            else:
                center_tile = set(all_words[0])
                for word in all_words:
                    center_tile = center_tile.intersection(set(word))
                center_tile = ''.join(list(center_tile))
                
            puzz_tiles = list(set(''.join(all_words))-set(center_tile))
            puzz_tiles.sort()
            puzz_tiles.insert(0,center_tile)
            if len(puzz_tiles)!=BeeParameters.max_tiles or len(center_tile)!=1:
                print(f'Error scraping puzzle tiles {puzz_tiles} {center_tile}')

            puzz_tiles.remove(center_tile)
            puzz_tiles.sort()
            puzz_tiles.insert(0,center_tile)
            puzz_tiles=''.join(puzz_tiles)
            date_str=self.date.strftime(Puzzle.date_format)
            self.puzzle = Puzzle(tiles=puzz_tiles,solution=all_words,date_str=date_str)
        else:
            self.puzzle = None

    def get_puzzle_from_input(self,puzzle):
        self.puzzle = puzzle

class Sbsolver_Parameters:
    start_date = datetime(2018, 5, 9)

@dataclass
class Sbsolver_Solution:
    date: datetime
    date_str: str = None
    waiter_settings: Dict = field(default_factory=lambda: {'t1':1.0,'t2':8.0,'t3':8.0,'t4':17.0, 'maxdepth': 3, 'scaler':1, 'phighbin':0.2,'precursion':0.5})
    def __post_init__(self):
        if not isinstance(self.date,datetime):
            raise ValueError(f'Sbsolver_Solution {self.date} must be a datetime')
        elif self.date < Sbsolver_Parameters.start_date or self.date > datetime.today():
            print(f'Sbsolver_Solution {self.date} must be between {Sbsolver_Parameters.start_date} and today')
        self.puzzle = None

    def __str__(self):
        return f'Sbsolver_Solution for {self.date}\n url: {self.urlstring()}\n {self.urlstring()}\n {self.puzzle}'
    
    def translate_date_to_index(self):
        return 1+(self.date-Sbsolver_Parameters.start_date).days
    
    def urlstring(self):
        return f"https://www.sbsolver.com/s/{self.translate_date_to_index()}"
    
    def get_puzzle_from_url(self):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        if self.waiter_settings is not None:
            recursive_waiter(**self.waiter_settings)
        page = requests.get(self.urlstring(), headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        if page.status_code != 200:
            print(f'Error fetching page {self.urlstring()}')
            self.puzzle = None
            return None

        puzz_tiles = soup.find('input')['value']    
        all_words = [item.a['href'].split('/')[-1] for item in soup.find_all('td', {"class": "bee-hover"})]
        self.extracted_date = datetime.strptime(soup.find("meta", property="og:title")['content'].split(':')[0] ,'%B %d, %Y')
        if self.extracted_date!=self.date:
            print(f'Error scraping Sbsolver date mismatch {self.extracted_date} {self.date}')
        if len(puzz_tiles)!=BeeParameters.max_tiles :
            print(f'Error scraping puzzle tiles {puzz_tiles}')

        date_str=self.date.strftime(Puzzle.date_format)
        self.puzzle = Puzzle(tiles=puzz_tiles,solution=all_words,date_str=date_str)

    def get_puzzle_from_input(self,puzzle):
        self.puzzle = puzzle

@dataclass
class Bee_DataBase:
    google_sheet_id: str = None
    google_sheet_name: str = None
    google_sheet: Google_Sheet = None
    start_date: str = None 
    end_date: str = None
    missing_datetimes_list = None
    local: bool = False
    timestampstr = None
    df = None

    def __post_init__(self):
        self.google_sheet = Google_Sheet(google_sheet_name=self.google_sheet_name,google_sheet_id=self.google_sheet_id)
        self.google_sheet.open_by_id()
        self.google_sheet.read_to_df()
        self.google_sheet_name = self.google_sheet.google_sheet_name
        self.google_sheet_id = self.google_sheet.google_sheet_id
        self.df = self.google_sheet.df
        if len(self.df)==0:
            print('Current bee database sheet is empty')
        else:
            if self.local:
                self.timestampstr = self.timestamp()
                self.write_db_to_local(final=False)
            self.validate()

    def __str__(self):
        return f'Bee_Database for "{self.google_sheet_name}" "{self.google_sheet_id}"\n start:end date {self.start_date}:{self.end_date}\n{self.df}'

    def validate(self):
        df = pd.DataFrame({'date': pd.Series(dtype='str'),
                        'tiles': pd.Series(dtype='str'),
                        'solution': pd.Series(dtype='str'),})

        for _,row in self.df.iterrows():
            try:
                date = pd.to_datetime(row['date'])
                date_str = date.strftime(Puzzle.date_format)
                solution = row['solution'].split(' ')
                tiles = row['tiles']
                puzzle = Puzzle(tiles=tiles,date_str=date_str,solution=solution)
                # Note that rather than writing out the whole class, we only write out the datestr, tiles, and solution string because
                # when we use the google_sheet_class to update, we must go through a serializer that 
                # cannot accomodate unusual classes like the Puzzle Class
                d = {'date': [puzzle.date_str], 'tiles':[puzzle.tiles], 'solution':[puzzle.solution.make_list_to_string()]}
                df = pd.concat([df, pd.DataFrame.from_dict(d, orient='columns')],  ignore_index=False, axis=0)
            except:
                print(f'Error validating Bee_Database {row["date"]} {row["tiles"]}')
        self.df = df.sort_values(by='date',ascending=True)
        self.start_date=self.df['date'].values[0]
        self.end_date=self.df['date'].values[-1]
        self.missing_datetimes_list = self.missing_datetimes()
        if len(self.missing_datetimes_list)>0:
            print(f'DataBase Validation WARNING: missing dates\n')
            for d in self.missing_datetimes_list:
                print(d)

    def append(self,df):
        # have to translate datetime to string so that it is JSON serializable
        df['date']=df['date'].apply(lambda x: x.strftime(Puzzle.date_format))
        self.google_sheet.append_df(df)
        self.df = pd.concat([self.df, df],  ignore_index=False, axis=0)
        self.validate()
        if self.local:
            self.write_db_to_local(final=True)

    def overwrite(self):
        self.google_sheet.write_df(df=self.df)
        if self.local:
            self.write_db_to_local(final=True)

    def write_db_to_local(self,final):        
        if final:
            local_file = f'data/{self.google_sheet_name}-{self.timestampstr}.csv'
        else:
            local_file = f'data/{self.google_sheet_name}-{self.timestampstr}-BCK.csv'
        self.df.to_csv(local_file,index=False)

    def timestamp(self):
        return datetime.now().strftime("%Y-%m-%d-%H%M%S")

    def make_datestr_list(self):
        if len(self.df)>0:
            return list(self.df['date'])

    def make_datetime_list(self):
        if len(self.df)>0:
            return list(pd.to_datetime(self.df['date']))
        else:
            return []
        
    def update_df(self,df):
        self.df = df
        self.validate()

    def missing_datetimes(self):
        delta = timedelta(days=1)
        d_list = []
        d = datetime.strptime(self.start_date, Puzzle.date_format)
        while d <= datetime.strptime(self.end_date, Puzzle.date_format):
            d_list.append(d)
            d+=delta
        d_list = [d.strftime(Puzzle.date_format) for d in d_list]
        d_list = sorted(list(set(d_list)-set(self.df['date'])))
        return d_list

if __name__ == '__main__':
    pass
