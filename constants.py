"""The current file contains constants"""

class CONST:
    
    """The constants are given in a class."""
    
    def __init__(self):
        pass

    # 0 DRIVER = 'D:/py/med/driver/chromedriver.exe'
    # 1 LINK = 'https://cr.minzdrav.gov.ru/archive'
    # 2 START = '//*[@id="app"]/div/div/main/div/div/div[3]/div[2]/div[1]/div/div/div/div[3]/div'
    # 3 END = '//*[@id="v-menu-21"]/div/div/div[7]/div[2]/div'
    # 4 ANCHOR = '//*[@id="app"]/div/div/main/div/div/div[3]/div[1]/table/tbody[1]/tr[377]/td[1]/span'
    # 5 INDICES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=(\d{1,4}_\d{1,4})'
    # 6 URL = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}',
    # 7 TITLES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}"\sclass="">(.*?)</a></td><td>'

    # the common regex to use is:
    # r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}"\sclass="">.*?</a></td><td>(\d{1,2}\/\d{1,2}\/\d{1,4})</td><td>.*?</td>'

    def cons(self, number: int) -> str:

        """The function returns a constant value by a given number."""
        
        DRIVER = 'D:/py/med/driver/chromedriver.exe'
        
        LINK = 'https://cr.minzdrav.gov.ru/archive'        
        
        START = '//*[@id="app"]/div/div/main/div/div/div[3]/div[2]/div[1]/div/div/div/div[3]/div'
        
        END = '//*[@id="v-menu-21"]/div/div/div[7]/div[2]/div'
        
        '''note that the anchor is not a constant value'''
        ANCHOR = '//*[@id="app"]/div/div/main/div/div/div[3]/div[1]/table/tbody[1]/tr[377]/td[1]/span'
        
        INDICES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=(\d{1,4}_\d{1,4})'
        
        URL = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}'
        
        TITLES = r'https:\/\/apicr.minzdrav.gov.ru\/api.ashx\?op=GetClinrecPdf&amp;id=\d{1,4}_\d{1,4}"\sclass="">(.*?)<\/a><\/td><td>'

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
