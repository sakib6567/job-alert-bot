import requests
from bs4 import BeautifulSoup
import urllib3
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_bdjobs():
    url = "https://www.bdjobs.com/jobsearch.asp?fcatId=8&icatId="
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    for div in soup.find_all("div", class_="norm_jv"):
        title_tag = div.find("a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag["href"]
            deadline = "N/A"
            jobs.append({
                "title": f"BDJobs - {title}",
                "link": link,
                "deadline": deadline,
                "category": "Private"
            })
    return jobs

def scrape_bpsc():
    url = "https://bpsc.gov.bd/site/view/notices"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    table = soup.find("table", class_="table")
    if table:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                title = cols[1].get_text(strip=True)
                deadline = "N/A"
                link_tag = cols[1].find("a")
                link = "https://bpsc.gov.bd" + link_tag["href"] if link_tag and link_tag.has_attr("href") else ""
                jobs.append({
                    "title": f"BPSC - {title}",
                    "link": link,
                    "deadline": deadline,
                    "category": "Government"
                })
    return jobs

def scrape_bangladesh_bank():
    url = "https://erecruitment.bb.org.bd/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    jobs = []
    table = soup.find("table")
    if table:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 4:
                title = cols[0].get_text(strip=True)
                deadline = cols[3].get_text(strip=True)
                link = "https://erecruitment.bb.org.bd/" + cols[0].find("a")["href"]
                jobs.append({
                    "title": f"Bangladesh Bank - {title}",
                    "link": link,
                    "deadline": deadline,
                    "category": "Banking"
                })
    return jobs

def main():
    jobs = scrape_bdjobs() + scrape_bpsc() + scrape_bangladesh_bank()
    with open("jobs_data.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"Scraped {len(jobs)} jobs on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
