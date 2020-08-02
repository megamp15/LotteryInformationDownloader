# Lottery Information Downloader
### Information on the lottery Information Downloader:

This script automates the retrieval of lottery data from the [Texas Retailer Lottery Website](https://tx-lsp.lotteryservices.com/lsptx/public/lotteryhome) using Selenium and Python.

The GUI interface is developed using Tkinter to keep the program compact and distributable.

Instructions to use the GUI Interface:

	How to use the Lottery Information Downloader:
  
		1. Select the excel file with all the client(s) information.
    		   Look at the 'SAMPLE.xlsx' excel file for more information on how to setup the excel file.
		   
		2. Select the download folder where you would like the lottery files.
    		   Note: A folder with the retailer name is created in the directory chosen with the downloaded lottery files inside.

		3. Enter Start and End date in the month/day/year or 00/00/0000 format.
    		   Note: If you click the entry fields for the dates the placeholder dates will be removed.

		4. Click the Start Button to begin the automatic download. 

		5. Once completed a pop up message will appear that will inform you that the program is   
		   complete. Click the Exit button to end the entire program.

	Information on each Button:

    		- Start Button = Start the Automatic Downloader. 
                     		 Clickable once all the appropriate fields are filled in.
                     
    		- End Button   = End the Automatic Downloader at anytime without closing the interface. 
                     		 Can view errors if there are any.
                     
    		- Help Button  = Recieve Information about the Program from the GUI interface. 
    
    		- Error Button = Clickable when there is an error. Otherwise no error was found.
    
    		- Exit Button  = Exit the downloader and interface. 
                     		 Cannot view errors if there are any.
