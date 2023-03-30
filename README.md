# Updating_Call_Number_in_Holdings

Some colleagues asked a question on whether there was a way to edit/replace the call numbers in existing holdings records using a spreadsheet.

The answer is yes. The prerequisite is that you export the MMS id and call numbers data from the spreadsheet to a text file with a special format like below.



Then you use the code to process this file line by line and replace the call numbers in the corresponding holding records in ALMA.

The first, please edit the Main13.py file (downloaded from GitHub) and add your library cataloging records API key there.



The second, run the python in windows command prompt and input “python Main13.py”, then press enter key. After that, click the “Locate the MMS ID file” button and open the text file (MMS_ID_and_Data.txt) we mentioned previously. After waiting for a moment, everything is done.



The code is in GitHub https://github.com/andytang2008/Updating_Call_Number_in_Holdings

The code was tested successfully in the environment of Windows 10 + Python 3.8.6. Please use this code by a small set of data first.

BTW: If Python pops up a warning “ImportError: No module named requests”, please use “python -m pip install requests” to install requests module, or contact your library application developer to solve it. 

I hope it helps.
