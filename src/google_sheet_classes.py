import pygsheets
import pandas as pd
import os
import time

class Google_Sheet:
    def __init__(self, google_sheet_name=None, google_sheet_id=None, sheet_name=None):
        # start_time = time.time()
        self.google_api_json = os.environ.get('GOOGLE_API_JSON')
        self.authorize()
        # print(f"⏱️  Authorization took {time.time() - start_time:.2f}s")
        if (google_sheet_name is None and google_sheet_id is None) or \
           (google_sheet_name is not None and google_sheet_id is not None):
            raise ValueError("Please give a value for google_sheet_name or google_sheet_id (but not both)")
        elif google_sheet_id is None:
            self.google_sheet_name = google_sheet_name
            self.find_id_from_name()
        else:
            self.google_sheet_id = google_sheet_id
            # name_start = time.time()
            self.find_name_from_id()
            # print(f"⏱️  find_name_from_id took {time.time() - name_start:.2f}s")
        self.spreadsheet = None
        self.sheet_name = sheet_name
        self.worksheet = None
        self.df = None
        
    def authorize(self):
        self.google_sheet_authorization = pygsheets.authorize(service_file=self.google_api_json)
    
    def open_by_name(self):
        self.spreadsheet = self.google_sheet_authorization.open(self.google_sheet_name)
        if not self.sheet_name:
            self.worksheet = self.spreadsheet[0] # first tab
        else:
            self.worksheet = self.spreadsheet.worksheet(self.sheet_name)

    def open_by_id(self):
        # start_time = time.time()
        # Reuse spreadsheet if already opened (e.g., from find_name_from_id)
        if self.spreadsheet is None:
            self.spreadsheet = self.google_sheet_authorization.open_by_key(self.google_sheet_id)
        if not self.sheet_name:
            self.worksheet = self.spreadsheet[0] # first tab
        else:
            self.worksheet = self.spreadsheet.worksheet(self.sheet_name)
        # print(f"⏱️  open_by_id took {time.time() - start_time:.2f}s")

    def find_id_from_name(self):
        self.google_sheet_id = list(filter(lambda x: x['name'] == self.google_sheet_name, self.google_sheet_authorization.drive.spreadsheet_metadata()))[0]['id']

    def find_name_from_id(self):
        # Open the sheet and cache it to avoid reopening later
        try:
            self.spreadsheet = self.google_sheet_authorization.open_by_key(self.google_sheet_id)
            self.google_sheet_name = self.spreadsheet.title
        except Exception as e:
            raise ValueError(f"Could not find sheet with ID: {self.google_sheet_id}") from e


    def read_to_df(self):
        # start_time = time.time()
        self.df = pd.DataFrame(self.worksheet.get_all_records())
        # print(f"⏱️  read_to_df took {time.time() - start_time:.2f}s (read {len(self.df)} rows)")

    def append_df(self,df):
        self.worksheet.append_table(values=df.values.tolist())

    def write_df(self,df):
        # wks = self.spreadsheet[0] # this sets to the first sheet
        # service.spreadsheets().values().clear(spreadsheetId='SHEET_ID', range='SHEET_NAME', body={}).execute()
        self.worksheet.clear()
        self.worksheet.set_dataframe(df,(0,0))

    def __str__(self):
        return f"GoogleSheet name {self.google_sheet_name} id: {self.google_sheet_id}"

if __name__ == '__main__':
    pass




