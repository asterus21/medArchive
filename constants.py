"""The current file contains constants for the script."""

DRIVER = 'driver/chromedriver.exe' # note that the relative path to the driver is used
LINK = 'https://cr.minzdrav.gov.ru/archive'
START = '//*[@id="app"]/div/div/main/div/div/div[3]/div[2]/div[1]/div/div/div/div[3]/div'
END = '//*[@id="v-menu-21"]/div/div/div[7]/div[2]/div'
ANCHOR = '//*[@id="app"]/div/div/main/div/div/div[3]/div[1]/table/tbody[1]/tr[377]/td[1]/span' # note that the value can be changed eventually
INDICES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=(\d{1,4}_\d{1,4})'
URL = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}'
TITLES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}"\sclass="">(.*?)<\/a><\/td><td>'

class Constants:
    
    """The constants function (or functions) which are used in the script."""
    
    def __init__(self):
        pass

    def constants_to_store(self, number: int) -> str:

        """The function returns a constant value by a given number."""
        
        match number:

            case 0:
                return DRIVER
            case 1:
                return LINK
            case 2:
                return START
            case 3:
                return END
            case 4:
                return ANCHOR
            case 5:
                return INDICES
            case 6:
                return URL
            case 7:
                return TITLES
