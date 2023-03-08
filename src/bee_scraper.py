from src.bee_classes import BeeParameters,Word,SolutionList,Puzzle,NytBee_Parameters,Sbsolver_Parameters,NytBee_Solution,Bee_DataBase
# from src.google_sheet_classes import Google_Sheet
import pandas as pd
import argparse
from datetime import datetime, date, timedelta

# TODO:
# remove excess code from the __main__ of al these routines, especially class definitions
# 

def dates_iterable(start_date,end_date):
    delta = timedelta(days=1)
    return [d for d in ]

if __name__ == '__main__':
    ''' Default behavior: grab the specified solutions database
    do the quality checks on it (implemented in Bee_DataBase)
    provide warnings about data quality
    if there are any holes in the dates in the current database between the start and end date, try to get that data
    if the only updates are at the end of the database, just update the page
    if the updates include dates that are in between prior solutions, warn that you will need to overwrite but just append.
    '''
# TODO:
# Functionalities we want:
# - check the current db, and then scrape all missing solutions from nytbee, update append the db
# - have argparse to take in the sheet
    parser = argparse.ArgumentParser(
        prog="bee_scraper",
        description="Scrape nytbee website solutions to the google sheet you input by sheet id",
    )
    parser.add_argument("-i", "--id", type=str, required=True, help="Google sheet id string for the the solutions database (must be setup already and have permissions)")
    parser.add_argument("-o", "--overwrite",action="store_true",default=False,help="overwrite the entire sheet")
    parser.add_argument("-e", "--end_date",type=str,required=False,default=date.today().strftime(Puzzle.date_format),help="end_date; format=2022-01-25 (today if not specified)")
    parser.add_argument("-s", "--start_date",type=str,required=False,default=Sbsolver_Parameters.start_date.strftime(Puzzle.date_format),help="start_date; format=2018-07-29 (first puzzle if not specified)")
    parser.add_argument("-v", "--verbose",required=False,action="store_true",default=False,help="Not implemented")
    parser.add_argument("-l", "--local",required=False,action="store_true",default=False,help="Write database versions to local files")
    args = parser.parse_args()
    db_google_sheet = Bee_DataBase(google_sheet_id=args.id,local=args.local)
    print(db_google_sheet)
    print(15*'dates-','\n',db_google_sheet.make_date_list())
    # TODO: vet against start and end dates, set up method to get only the dates you need
    # TODO: create method to compare data between the two websites and pick one; write out any mismatches
    # TODO: eventually get the update method working for new data only. 
    # TODO: start with a small date range and an empty sheet
    # TODO: then disorder the sheet, try skipped fill-in dates, etc. 
    # TODO: eventually empty out the sheet and just run a full overwrite.
    # TODO: am I using all the argparses?
    # TODO: maybe more pytests
    # TODO: can I pytest google_sheet_class (currently empty test) or delete test file

    # test_sheet.append_df(df=tiny_df)
    db_google_sheet.overwrite()

    # end_date = datetime.date.today()
    # delta = timedelta(days=1)




    # put together and then randomize the list of dates we need to fetch
    # this_date = start_date
    # while this_date <= end_date:
    #     (year, month, day) = (this_date.year, this_date.month, this_date.day)
    #     datestring = f'{year:02d}{month:02d}{day:02d}'
    #     url = f'https://nytbee.com/Bee_{datestring}.html'
    #     # check if file already exists
    #     filename = f'data/NYTbee__{datestring}.txt'
    #     file_exists = os.path.exists(filename)
    #     if file_exists:
    #         pass
    #     else:
    #         recursive_waiter(phighbin=0.2,maxdepth=5,precursion=0.5,scaler=1)
    #         print(f'Fetching data for {url}')
    #         todays_lists,puzz_tiles = get_todays_lists(url)
    #         if todays_lists:
    #             write_file(puzz_tiles,todays_lists,filename)
    #         else:
    #             print(f"{bcolors.WARNING}Warning: Cannot find data for url {url}.{bcolors.ENDC}")
    #     this_date += delta