import requests, time,re,datetime,csv,traceback
from bs4 import BeautifulSoup,element
from googlesearch import search 

SearchPrefix = "https://www.zaubacorp.com/companysearchresults/"
Header = {
            "Host": "sitereview.bluecoat.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }


def ZaubaGetCompanyDetails(url):
    headers = Header
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return [
                # soup.find( "p" , text = "CIN").findNext("p").text.replace("\n",""),
                soup.find( "p" , text = "Company Name").findNext("p").text.replace("\n", ""),
                soup.find( "p" , text = "Company Status").findNext("p").text.replace("\n", ""),
                # soup.find( "p" , text = "RoC").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Registration Number").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Company Category").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Company Sub Category").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Class of Company").findNext("p").text.replace("\n",""),
                soup.find( "p" , text = "Date of Incorporation").findNext("p").text.replace("\n", ""),
                soup.find( "p" , text = "Age of Company").findNext("p").text.replace("\n", ""),
                # soup.find( "p" , text = "Activity").findNext("p").text.replace("\n", ""),
                # soup.find( "p" , text = "Number of Members").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Authorised Capital").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Paid up capital").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Listing status").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Date of Last Annual General Meeting").findNext("p").text.replace("\n",""),
                # soup.find( "p" , text = "Date of Latest Balance Sheet").findNext("p").text.replace("\n",""),
                soup.find( "b" , text = " Email ID: ").parent.find(text=True,recursive=False),
                soup.find( "b" , text = "Website:").parent.find(text=True,recursive=False),
                soup.find( "b" , text = "Address: ").parent.findNext("p").text.replace("\n","")
            ]
def GoogleTopThree(key):
    query = "http://www.google.co.in/search?q=" + key
    print(query)
    r = requests.get(query,headers=Header)  
    soup = BeautifulSoup(r.content, "html.parser")
    print(soup)
    cites = soup.findAll("div", class_="TbwUpd NJjxre")
    print(cites)
    for cite in cites:
        print(cite)

def GoogleTop3(key):
    temp =[]
    for value in  search(key, tld="co.in", num=10, start=0, stop=3, pause=2) :
        temp.append(value)
    return temp

def ZaubaGetCompanySearch(searchStr):
    search_url = SearchPrefix + searchStr
    headers = Header
    r = requests.get(search_url,headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    results = list
    # table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="results")
    # rows = table.findAll(lambda tag: tag.name=='tr')
    table = soup.find('table', id="results")
    rows = table.findAll('tr')
    result = []
    lenRows = len(rows)
    c = 0 
    for row in rows :
        # if c == 5 :
        #     break
        startTime = time.time()
        columns = row.findAll('td')
        temp = list()
        other = list()
        google = list()
        for column in columns:
            temp.append(column.text)
            a = column.find('a', href=True)
            if a :
                # temp = temp + ZaubaGetCompanyDetails(a.attrs['href'])
                other = ZaubaGetCompanyDetails(a.attrs['href'])
                time.sleep(10)
                google = GoogleTop3(a.text)
                
        c = c+1
        Elasped = time.time() - startTime
        # print(end='\r' )
        print("Proceesing ; Completed %.2f%% ; Last Elasped time : %f s ; ETC : %f s" %((c/lenRows * 100), Elasped, (lenRows-c)*Elasped), end='\r')
        temp = temp + google + other
        result.append(temp)
        
    return result

# GoogleTopThree("HIM ROBOTICS LLP")
if __name__ == "__main__":
    
    Keywords = ['robotics']
    result = []
    try :
        for keyword in Keywords:
            result = ZaubaGetCompanySearch(keyword)
    except Exception as  e :
        print("\n\n")
        print(str(e))
        traceback.print_exc()
    finally:
        print("\n\n")
        print("Completed")
        with open("Output_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") +".csv","w+") as file:
            csvWriter = csv.writer(file,delimiter=',')
            csvWriter.writerows(result)

# print(ZaubaGetCompanyDetails("https://www.zaubacorp.com/company/MAKEBOT-ROBOTIC-SOLUTIONS-PRIVATE-LIMITED/U74995MH2018PTC309071"))