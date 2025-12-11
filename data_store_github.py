import json
import os
import requests
from datetime import datetime

class GitHubDataStore:
    def __init__(self):
        self.repo = os.getenv('GITHUB_REPOSITORY')
        self.token = os.getenv('GITHUB_TOKEN')
        self.branch = 'main'
        self.jobs_file = 'data/jobs.json'
        self.sent_jobs_file = 'data/sent_jobs.json'
    
    def get_file_content(self, file_path):
        url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}"
        headers = {'Authorization': f'token {self.token}'}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                import base64
                content = base64.b64decode(response.json()['content']).decode()
                return json.loads(content), response.json()['sha']
            return [], None
        except:
            return [], None
    
    def update_file(self, file_path, content, sha=None):
        url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}"
        headers = {'Authorization': f'token {self.token}'}
        
        import base64
        encoded_content = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
        
        data = {
            'message': f'Update {file_path}',
            'content': encoded_content,
            'branch': self.branch
        }
        
        if sha:
            data['sha'] = sha
        
        requests.put(url, json=data, headers=headers)
    
    def load_jobs(self):
        jobs, _ = self.get_file_content(self.jobs_file)
        return jobs
    
    def save_jobs(self, jobs):
        existing_jobs, sha = self.get_file_content(self.jobs_file)
        all_jobs = existing_jobs + jobs
        recent_jobs = all_jobs[-1000:]
        self.update_file(self.jobs_file, recent_jobs, sha)
        return recent_jobs
    
    def load_sent_jobs(self):
        sent_jobs, _ = self.get_file_content(self.sent_jobs_file)
        return sent_jobs
    
    def mark_jobs_as_sent(self, job_ids):
        sent_jobs, sha = self.get_file_content(self.sent_jobs_file)
        new_sent = [{'id': job_id, 'sent_at': datetime.now().isoformat()} for job_id in job_ids]
        sent_jobs.extend(new_sent)
        self.update_file(self.sent_jobs_file, sent_jobs, sha)
    
    def get_new_jobs(self, jobs):
        sent_jobs = self.load_sent_jobs()
        sent_job_ids = {job['id'] for job in sent_jobs}
        return [job for job in jobs if job['id'] not in sent_job_ids]