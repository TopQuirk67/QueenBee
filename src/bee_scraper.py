from src.bee_classes import Puzzle,NytBee_Parameters,Sbsolver_Parameters,NytBee_Solution,Sbsolver_Solution,Bee_DataBase
import pandas as pd
import argparse
from datetime import datetime, timedelta

# TODO: add some error checking to the requests 
# TODO: write out good data in the case of failure
# TODO: remove excess code from the __main__ of al these routines, especially class definitions
# TODO: remove TODOs
# TODO: write tiny class for missed solutions in its own file

def date_list(start_date,end_date):
    delta = timedelta(days=1)
    d_list = []
    if start_date<min(NytBee_Parameters.start_date,Sbsolver_Parameters.start_date):
        print(f'Warning {start_date} precedes data availability')
        start_date=min(NytBee_Parameters.start_date,Sbsolver_Parameters.start_date)
    if start_date>datetime.today():
        print(f'Warning {start_date} must be today {datetime.today()} or earlier')
        start_date=datetime.today()
    d = start_date
    while d <= end_date:
        d_list.append(d)
        d+=delta
    return d_list

def newly_scraped_dates_prior_to_last_db_date(db_df, new_df):
    if db_df is None or new_df is None:
        return False
    elif len(db_df) == 0 or len(new_df) == 0:
        return False
    else:
        return (len(set(new_df['date']).intersection(set(pd.to_datetime(db_df['date'])))))>0 or \
            (min(new_df['date'].values))<=(max(pd.to_datetime(db_df['date'].values)))

if __name__ == '__main__':
    ''' Default behavior: grab the specified solutions database
    do the quality checks on it (implemented in Bee_DataBase)
    provide warnings about data quality
    if there are any holes in the dates in the current database between the start and end date, try to get that data
    if the only updates are at the end of the database, just update the page
    if the updates include dates that are in between prior solutions, warn that you will need to overwrite but just append.
    '''
    parser = argparse.ArgumentParser(
        prog="bee_scraper",
        description="Scrape nytbee website solutions to the google sheet you input by sheet id",
    )
    parser.add_argument("-i", "--id", type=str, required=True, help="Google sheet id string for the the solutions database (must be setup already and have permissions)")
    parser.add_argument("-o", "--overwrite",action="store_true",default=False,help="overwrite the entire sheet")
    parser.add_argument("-e", "--end_date",type=str,required=False,default=datetime.today().strftime(Puzzle.date_format),help="end_date; format=2022-01-25 (today if not specified)")
    parser.add_argument("-s", "--start_date",type=str,required=False,default=Sbsolver_Parameters.start_date.strftime(Puzzle.date_format),help="start_date; format=2018-07-29 (first puzzle if not specified)")
    parser.add_argument("-l", "--local",required=False,action="store_true",default=False,help="Write database versions to local files")
    args = parser.parse_args()
    start_date_datetime = datetime.strptime(args.start_date,Puzzle.date_format)
    earliest_possible_date = min(Sbsolver_Parameters.start_date,NytBee_Parameters.start_date)
    if start_date_datetime < earliest_possible_date:
        print(f'Resetting date to {earliest_possible_date} (earliest possible)')
        start_date_datetime = earliest_possible_date 
    end_date_datetime = datetime.strptime(args.end_date,Puzzle.date_format)
    db_google_sheet = Bee_DataBase(google_sheet_id=args.id,local=args.local)
    db_dates = db_google_sheet.make_datetime_list()

    df = pd.DataFrame()
    for d in date_list(start_date=start_date_datetime,end_date=end_date_datetime):
        if d not in db_dates:
            print(f'fetching data for date {d}')
            nyt = NytBee_Solution(date=d)
            nyt.get_puzzle_from_url()
            sbs = Sbsolver_Solution(date=d)
            sbs.get_puzzle_from_url()
            if sbs.puzzle is None and nyt.puzzle is None:
                print(f'No solution data available for date {d}')
            elif sbs.puzzle is None:
                puzzle = nyt.puzzle
            elif nyt.puzzle is None:
                puzzle = sbs.puzzle
            elif nyt.puzzle == sbs.puzzle:
                puzzle = nyt.puzzle
            else:
                print(f'Mismatched solutions for date {d} \n NYTBee \n {nyt}\n Sbsolver \n {sbs}')
            d = {'date': [d], 'tiles':[puzzle.tiles], 'solution':[puzzle.solution.make_list_to_string()]}
            df = pd.concat([df, pd.DataFrame.from_dict(d, orient='columns')],  ignore_index=False, axis=0)
    if args.overwrite or newly_scraped_dates_prior_to_last_db_date(db_df = db_google_sheet.df, new_df = df):
        df = pd.concat([df, db_google_sheet.df],  ignore_index=False, axis=0) # .sort_values(by='date',ascending=True)
        db_google_sheet.update_df(df)
        db_google_sheet.overwrite()
    elif len(df)==0:
        print('Nothing to append')
    else:
        db_google_sheet.append(df)


