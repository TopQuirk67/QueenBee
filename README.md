# QueenBee

This package can create a google sheet to store the whole history of solutions to the [New York Times Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee).  I use this history along with a list of the words I have missed to study and to create commonly encounted words lists for study.

Happy scraping!

## Installs for the pipenv environment:

Clone this repo. 

This package has a Pipenv for the necessary installs.  Use:

`pipenv shell` 

in the package directory. 


## Running the program:

Environmental variables to define:
Put these lines in your .zshrc or whatever shell you are using, adjusting for your specifications.

```
export GOOGLE_API_JSON="/Users/YOURUSERNAME/YOUR_DIRECTORY/file_downloaded_from_google_API.json"
export GOOGLE_SHEET_QBDB="YOURGOOGLESHEETKEY_4wTpJGu6.L473g!vw!Gb_CnYF"
```

Set your `$PYTHONPATH` correctly:

`export PYTHONPATH=${PYTHONPATH}:${PWD}`

## Google API info:

Must set up the environmental variable `$GOOGLE_API_JSON` (see above)

Follow instructions at https://erikrood.com/Posts/py_gsheets.html to get setup with making your google sheets accessible.  You will need to share your sheet with the service account (this will look like your-project@your-project-892276.iam.gserviceaccount.com) and download a JSON (i.e. `$GOOGLE_API_JSON`) with credentials to your local machine.  I 

## NYTBee.com and sbsolver.com scraping info:

Typical scraping command is:

`python src/bee_scraper.py -i $GOOGLE_SHEET_QBDB -s 2018-01-08 -e 2023-03-09 -l`

Where I have date-limited the request and turned on the `--local` switch to write to a local `.csv`. If you choose invalid dates (prior to puzzle debut or after today), it will adjust your dates.  Leaving dates off defaults to all time (be careful... see notes for `Recursive Waiter`)

```
options:
  -h, --help            show this help message and exit
  -i ID, --id ID        Google sheet id string for the the solutions database (must be setup already and have permissions)
  -o, --overwrite       overwrite the entire sheet
  -e END_DATE, --end_date END_DATE
                        end_date; format=2022-01-25 (today if not specified)
  -s START_DATE, --start_date START_DATE
                        start_date; format=2018-07-29 (first puzzle if not specified)
  -l, --local           Write database versions to local files
```

The scraper goes to two different websites to scrape [New York Times Spelling Bee](https://www.nytimes.com/puzzles/spelling-bee) solutions: [NYTBee](https://nytbee.com/) and [sbsolver](https://www.sbsolver.com/).  These sites are updated daily and go back in history to 7/29/2018 and 5/9/2018, respectively.  The latter is the debut of the online version of the puzzle.  The scraper compares the Puzzles derived from the two websites to make sure they match, creates a data structure ready to write out to your google sheet.  

I have scraped up to at least 3/12/2023 and put the results in my own readable [google sheet](https://docs.google.com/spreadsheets/d/1WkAPgB0-7KrVoF8yTSaedRT1q7h83FewcHJyZ-wmJ_Q/edit?usp=sharing).  If you just want a reasonably updated data source, grab that.  I will likely keep updating it monthly or so.   You can also use this sheet as a baseline for yours and save some scraping time. 

### Recursive waiter:

Who ordered that in the immortal (words of I.I.Rabi)[https://newatlas.com/standard-model-particle-physics-unexpected-particle/23897/#:~:text=In%20the%20mid%2D1930s%2C%20physicists,when%20informed%20of%20the%20discovery.]?  This little routine is meant to randomize the cadence of access to the data websites so as to "look like" a human accessing the website, but when I initially scraped the websites with hundreds of http requests, I started to get denied.  So if you plan on scraping the whole database yourself, date limit your scraping commands so as to only make a reasonable number of requests.  


## Running Pytest:

`pytest` 

Runs the suite of tests in tests/test_bee_classes.py

## Shameless Plug:

I have a tiny website that tells you what the lengths of the words you are missing for today's puzzle, (the Pollinator)[http://www.nytbeepollinator.com/] check it out!

## References:

- https://erikrood.com/Posts/py_gsheets.html
- Must share that sheet with the service account
- see: https://stackoverflow.com/questions/38949318/google-sheets-api-returns-the-caller-does-not-have-permission-when-using-serve
- also useful:
- https://medium.com/geekculture/2-easy-ways-to-read-google-sheets-data-using-python-9e7ef366c775
- My [google spreadsheet](https://docs.google.com/spreadsheets/d/1WkAPgB0-7KrVoF8yTSaedRT1q7h83FewcHJyZ-wmJ_Q/edit?usp=sharing) with the occasionally updated database.


## TODO:
- improve the SolutionsList class to create dictionary of alphagrams and associated words in that solutions list; propagate to Puzzle class
- improved date tracking with datetimes / datetimestrings in Bee_DataBase class.
- improve the error handling around refused connections.  If you are running over a large data set, the program just crashes!  It would be better to write out the data you already have when this happens so that it can pick up where it left off later.

## Resources:

Check other websites for more data, which I considered for data sources.  These are really just notes, so buyer beware. 
- https://www.sbsolver.com/history https://www.sbsolver.com/s/1418 ... yes seems to go back to 1, which is May 19, which really is the very first date. 
- https://spellingbeetimes.com/ ... pangrams only not useful; oh I take that back 
- https://-spellingbeetimes.com/2023/03/05/new-york-times-nyt-spelling-bee-answers-and-solution-for-march-5-2023/ 
- has all the words listed but not readily accessible
- first date: https://spellingbeetimes.com/2020/10/18/new-york-times-nyt-spelling-bee-answers-and-solution-for-october-18-2020/
https://spellingbeeanswers.com/ ... 
- https://spellingbeeanswers.com/spelling-bee-january-10-2019-answers is first date
- seems similar: https://nytspellingbeeanswers.org/nyt-spelling-bee-answers-03-06-23/
- https://nytspellingbeeanswers.org/nyt-spelling-bee-answers-01-18-21/ (first day)
- https://spellbeeanswers.com/nyt-spelling-bee-answer-solution-march-05th-2023/   
- but first date seems to be https://spellbeeanswers.com/nyt-spelling-bee-answer-solution-november-25th-2022/
