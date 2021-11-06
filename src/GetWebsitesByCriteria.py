import requests
import collections
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Get url
# url = str(input("Insert URL: "));

# Get html
# def get_soup(url):
#    html_file = urlopen(url).read()
#    return BeautifulSoup(html_file, 'lxml')

# soup = get_soup(url)
# print(soup.prettify())

# Get specific tags

# tags = soup.find_all('p')
# for tag in tags:
#     print(tag)

# tags = soup.find_all('div',class_="w3-content")
# for tag in tags:
#     print(tag.p)

# Get website to search on

def get_code_from_page(URL):
    html_text = requests.get(URL).text
    # print(html_text)

    # Get all jobs from url
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('div', class_="JobCard")
    return jobs

def display_jobs(jobs = [], FILTER_ACTIVE = 0, filter = ""):
    count = 0
    #print(jobs)
    for job in jobs:
        print("da")
        count = count + 1
        company_name = job.find('h3', class_="JCContentMiddle__Info JCContentMiddle__Info--Darker").text
        job_name = job.find('h2', class_="JCContentMiddle__Title").text
        job_link = job.find('a', class_="JCContent__Logo")
        job_date = job.find('span', class_="JCContentTop__Date").text
        job_link = "https://www.ejobs.ro/user/" + str(job_link)[58:str(job_link).find(">")-1] # next time use job.header.h2.a['href']
        job_skills = job.find()
        if FILTER_ACTIVE == 1:
            if filter in job_name:
                print(f'''
                Company Name: {company_name.strip()} 
                Job Title: {job_name}
                Job link: {job_link}
                Date posted: {str(job_date).strip()}
                ''')
        else:
            print(f'''
            Company Name: {company_name.strip()} 
            Job Title: {job_name}
            Job link: {job_link}
            Date posted: {str(job_date).strip()}
            ''')

        return count
            
def increase_page(URL):
    x = int(URL[-1:])
    x = x + 1
    URL = URL[:-1] + str(x)
    return URL

Words=str(input("What to search for: "))
URL = 'https://www.ejobs.ro/locuri-de-munca/' + Words + '/pagina1'
Filter = str(input("Filter by: "))
FILTER_ACTIVE = 1
if Filter != "":
    FILTER_ACTIVE = 1

starting_page = get_code_from_page(URL)
print(URL)
URL = increase_page(URL)
pages = [starting_page]

# Get all pages
for i in range(1,20):
    jobs = get_code_from_page(URL)
    pages.append(jobs)
    if jobs == starting_page:
        print("Finished looping through pages")
        break;
    print(URL)
    URL = increase_page(URL)

# Display all pages
COUNT_JOBS_AFTER_FILTER = 0
COUNT_JOBS_BEFORE_FILTER = 0
hashtable = {}
break_all = 0
url_list = []
for page in pages:
    if break_all == 1:
        break;
    for job in page:
        company_name = job.find('h3', class_="JCContentMiddle__Info JCContentMiddle__Info--Darker").text
        if company_name == "" :
            break_all = 1
            break;
        job_name = job.find('h2', class_="JCContentMiddle__Title").text
        for word in job_name.split(" "):
            if(word not in hashtable):
                hashtable[word] = 1
            else:
                hashtable[word] = hashtable[word] + 1

        job_link = job.find('a', class_="JCContent__Logo")
        job_date = job.find('span', class_="JCContentTop__Date").text
        job_link = "https://www.ejobs.ro/user/" + str(job_link)[58:str(job_link).find(
            ">") - 1]  # next time use job.header.h2.a['href']
        job_skills = job.find()
        COUNT_JOBS_BEFORE_FILTER = COUNT_JOBS_BEFORE_FILTER + 1
        if FILTER_ACTIVE == 1:
            if Filter in job_name:
                print(f'''
                Company Name: {company_name.strip()} 
                Job Title: {job_name}
                Job link: {job_link}
                Date posted: {str(job_date).strip()}
                ''')
                url_list.append(job_link);
                COUNT_JOBS_AFTER_FILTER = COUNT_JOBS_AFTER_FILTER + 1
        else:
            print(f'''
            Company Name: {company_name.strip()} 
            Job Title: {job_name}
            Job link: {job_link}
            Date posted: {str(job_date).strip()}
            ''')


# Output
print(str(COUNT_JOBS_BEFORE_FILTER) + " jobs found in this section!")
print(str(COUNT_JOBS_AFTER_FILTER) + " jobs titles match your search criteria!")

# Get category
category = ""

if all (k in hashtable for k in ("Software","Engineer")):
    print()
    print("Software Enginner");
# other categories to come

