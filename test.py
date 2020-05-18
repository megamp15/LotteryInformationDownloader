import os


def config_filePath():
    cur = os.getcwd()
    Lottery_dir = cur + "\\" + "Lottery"
    filelist = os.listdir(Lottery_dir)
    return cur, Lottery_dir, filelist


def create_folder(Lottery_dir, retailer_name, date_start):
    Month = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR", "05": "MAY", "06": "JUN",
             "07": "JUL", "08": "AUG", "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}
    path = Lottery_dir+"\\"+retailer_name+"\\" + \
        Month[date_start[:2]]+"-"+date_start[6:]
    os.mkdir(path)


data = config_filePath()
create_folder(data[1], "NB - Springtime", "05/01/2019")
