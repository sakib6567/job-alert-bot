
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bdjobs():
    url = "https://www.bdjobs.com/jobsearch.asp"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    for div in soup.select(".row.jobcontent"):
        title = div.select_one(".job-title-text").text.strip() if div.select_one(".job-title-text") else ""
        company = div.select_one(".comp-name-text").text.strip() if div.select_one(".comp-name-text") else ""
        category = div.select_one(".catagories").text.strip() if div.select_one(".catagories") else "General"
        deadline = div.select_one(".deadlines").text.strip() if div.select_one(".deadlines") else "Not specified"
        jobs.append({"Source": "BDJobs", "Title": title, "Company": company, "Category": category, "Deadline": deadline})
    return jobs

def scrape_bpsc():
    url = "http://bpsc.gov.bd/site/view/notices"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    for row in soup.select(".table.table-bordered tbody tr"):
        cols = row.find_all("td")
        if cols:
            title = cols[1].text.strip()
            deadline = cols[2].text.strip() if len(cols) > 2 else "Not specified"
            jobs.append({"Source": "BPSC", "Title": title, "Company": "BPSC", "Category": "Govt", "Deadline": deadline})
    return jobs

def scrape_bangladesh_bank():
    url = "https://erecruitment.bb.org.bd/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    for link in soup.find_all("a", href=True):
        if "jobdetail" in link["href"]:
            jobs.append({"Source": "BD Bank", "Title": link.text.strip(), "Company": "Bangladesh Bank", "Category": "Bank", "Deadline": "Not specified"})
    return jobs

def main():
    jobs = scrape_bdjobs() + scrape_bpsc() + scrape_bangladesh_bank()
    df = pd.DataFrame(jobs)
    df.to_csv("daily_jobs.csv", index=False)

if __name__ == "__main__":
    main()
