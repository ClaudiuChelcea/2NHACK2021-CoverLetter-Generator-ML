from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

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

# To repeat for each page: https://www.ejobs.ro/locuri-de-munca/c++/pagina2
URL = 'https://www.ejobs.ro/locuri-de-munca/c++'
html_text = requests.get(URL).text
# print(html_text)

# Get all jobs from url
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_="JobCard")

COUNT = 0
hashtable = {}
filter = 1 # apply filter
filter_job_text = 'C++'

for job in jobs:
    company_name = job.find('h3', class_="JCContentMiddle__Info JCContentMiddle__Info--Darker").text
    job_name = job.find('h2', class_="JCContentMiddle__Title").text
    for word in job_name.split(" "):
        hashtable[word] = 1;
    job_link = job.find('a', class_="JCContent__Logo")
    job_date = job.find('span', class_="JCContentTop__Date").text
    job_link = "https://www.ejobs.ro/user/" + str(job_link)[58:str(job_link).find(">")-1]
    job_skills = job.find()
    if filter == 1:
        if filter_job_text in job_name:
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

# print(jobs)
# print(hashtable)

