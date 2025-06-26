
import sys
import os
from datetime import datetime, timedelta
import re

comparison_format = "%Y%m%d_%H%M"


def identify_gaps(dir_to_scan: str, example_filename: str, step_in_mins: int = 30) -> list[str]:
   """
   Identifies whether there are gaps (missing files) in "dir_to_scan" by analyzing the datetimes shown by filenames and considering "step_in_mins" to identify sequence of files expected.
   
   Flow: 
   1) Identify all files that match "example_filename" format in "dir_to_scan"
   2) Obtain max and min datetimes 
   3) Verify if there is any missing file for datetime ranges considering expected files calculated using "step_in_mins"  

   Considerations:
   - Any "example_filename" can be used but it must always include datetime in following format %Y%m%d_%H%M%S
   - For initial version only 30 and 15 mins are supported for "step_in_mins" argument 
   - Delayed files are supported and they will counted for the o'clock or half closer.
      E.g. for 30 mins step, a filename containing 20250623_180700 is counted as belonging to o'clock 20250623_180000

   E.g.
   example_filename = upbcnv01_FO_EMAILREPORT_KPI_20250612_223000_last_30_minutes.csv
   step_in_mins = 30
   dir_to_scan = /home/matias
   files in /home/matias:  upbcnv01_FO_EMAILREPORT_KPI_20250623_180000_last_30_minutes.csv
                           upbcnv01_FO_EMAILREPORT_KPI_20250623_183000_last_30_minutes.csv
                           upbcnv01_FO_EMAILREPORT_KPI_20250623_193000_last_30_minutes.csv

   Returned missing filename -> upbcnv01_FO_EMAILREPORT_KPI_20250623_190000_last_30_minutes.csv

   """

   if step_in_mins not in (15, 30):
      raise ValueError("Only 15 and 30 minute steps are supported.")

   datetime_format_in_filename = "%Y%m%d_%H%M%S"   # Full datetime to extract

   # Create the regex based on input parameter  
   pattern = create_search_filename_regex(example_filename)
   regex = re.compile(pattern)

   # List all files in directory
   existing_files = os.listdir(dir_to_scan)

   # Obtain max and min dates
   # Build a set of observed prefixes
   observed_datetimes = set()
   for filename in existing_files:
      match = regex.match(filename)
      if not match:
         continue
      try:
         datetime_str = match.group(1) #Extract datetime from filename
         dt = datetime.strptime(datetime_str, datetime_format_in_filename)

         # Make adjustments for delayed files
         if step_in_mins == 30:
            minute = 0 if dt.minute < 30 else 30
         else:
            if dt.minute < 15:
               minute = 0
            elif dt.minute < 30:
               minute = 15
            elif dt.minute < 45:
               minute = 30
            else:
               minute = 45

         dt_bucket = dt.replace(minute=minute, second=0, microsecond=0)
         time_bucket = dt_bucket.strftime(comparison_format)

         observed_datetimes.add(time_bucket)

      except Exception:
         continue  # Skip malformed files

   if not observed_datetimes:
      raise ValueError("No files found matching example filename.")
   
   min_date = min(observed_datetimes)
   max_date = max(observed_datetimes)

   expected_datetimes = calculate_expected_datetimes(min_date, max_date, step_in_mins)

   # Check for missing prefixes
   missing_datetimes = sorted(expected_datetimes - observed_datetimes)

   return missing_datetimes


def create_search_filename_regex(example_filename: str) -> str:
   datetime_regex = r'(\d{8}_\d{6})' # Capturing group to use datetime later...

   # Find the datetime substring in the filename
   match = re.search(r'\d{8}_\d{6}', example_filename)
   if not match:
      raise ValueError("Datetime pattern not found in the input filename.")
    
   # Escape all other characters in the filename
   start = re.escape(example_filename[:match.start()])
   end = re.escape(example_filename[match.end():])

   # Construct final regex
   final_pattern = f'^{start}{datetime_regex}{end}$'
   return final_pattern

def calculate_expected_datetimes(min_date:str, max_date:str, step_in_mins: int) -> set:

   start_time = datetime.strptime(min_date, comparison_format)
   end_time = datetime.strptime(max_date, comparison_format)

   step = timedelta(minutes=step_in_mins)

   # Generate expected prefixes
   expected_datetimes = set()
   current = start_time
   while current <= end_time:
      datetime_str = current.strftime(comparison_format)
      expected_datetimes.add(datetime_str)
      current += step
   
   return expected_datetimes