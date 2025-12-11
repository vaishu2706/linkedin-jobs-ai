import requests
from bs4 import BeautifulSoup
import time
import random
import string

class JobFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_jobs(self, keywords, location):
        jobs = []
        
        try:
            indeed_jobs = self.fetch_from_indeed(keywords, location)
            jobs.extend(indeed_jobs)
        except Exception as e:
            print(f'Indeed fetch failed: {e}')
        
        try:
            remote_jobs = self.fetch_from_remoteok(keywords)
            jobs.extend(remote_jobs)
        except Exception as e:
            print(f'RemoteOK fetch failed: {e}')
        
        return self.normalize_jobs(jobs)
    
    def fetch_from_indeed(self, keywords, location):
        url = f"https://www.indeed.com/jobs?q={keywords}&l={location}"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        for element in soup.find_all('div', class_='job_seen_beacon')[:10]:
            try:
                title_elem = element.find('h2').find('a').find('span')
                company_elem = element.find('[data-testid="company-name"]')
                location_elem = element.find('[data-testid="job-location"]')
                link_elem = element.find('h2').find('a')
                
                if title_elem and company_elem:
                    jobs.append({
                        'title': title_elem.get_text().strip(),
                        'company': company_elem.get_text().strip(),
                        'location': location_elem.get_text().strip() if location_elem else '',
                        'link': 'https://www.indeed.com' + link_elem.get('href'),
                        'source': 'Indeed'
                    })
            except:
                continue
        
        return jobs
    
    def fetch_from_remoteok(self, keywords):
        response = requests.get('https://remoteok.io/api', headers=self.headers)
        data = response.json()[1:11]  # Skip metadata, limit to 10
        
        jobs = []
        for job in data:
            if job.get('position') and any(kw.strip().lower() in job['position'].lower() 
                                         for kw in keywords.split(',')):
                salary = f"${job.get('salary_min', '')}-{job.get('salary_max', '')}" if job.get('salary_min') else None
                jobs.append({
                    'title': job['position'],
                    'company': job.get('company', ''),
                    'location': 'Remote',
                    'link': f"https://remoteok.io/remote-jobs/{job['id']}",
                    'source': 'RemoteOK',
                    'salary': salary
                })
        
        return jobs
    
    def normalize_jobs(self, jobs):
        normalized = []
        for job in jobs:
            job_id = f"{job['source']}-{int(time.time())}-{''.join(random.choices(string.ascii_lowercase, k=9))}"
            normalized.append({
                'id': job_id,
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'link': job['link'],
                'source': job['source'],
                'salary': job.get('salary'),
                'fetched_at': time.strftime('%Y-%m-%dT%H:%M:%S')
            })
        return normalized