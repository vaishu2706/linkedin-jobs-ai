import os
from dotenv import load_dotenv
from job_fetcher import JobFetcher
from ai_matcher import AIMatcher
from email_sender import EmailSender
from data_store_github import GitHubDataStore

load_dotenv()

class JobAlertSystem:
    def __init__(self):
        self.job_fetcher = JobFetcher()
        self.ai_matcher = AIMatcher(os.getenv('OPENAI_API_KEY'))
        self.email_sender = EmailSender(os.getenv('RESEND_API_KEY'))
        self.data_store = GitHubDataStore()
        
        self.user_profile = """
Experienced software developer looking for:
- Full-stack or backend development roles
- Remote or hybrid positions
- Technologies: JavaScript, Python, Node.js, React
- Experience level: Mid to Senior (3-8 years)
- Salary range: $80k-150k
- Interested in: Startups, tech companies, fintech
"""
    
    def run(self):
        try:
            print('🚀 Starting job search...')
            
            keywords = os.getenv('JOB_KEYWORDS', 'software engineer,developer')
            location = os.getenv('LOCATION', 'remote')
            
            print(f'Searching for: {keywords} in {location}')
            all_jobs = self.job_fetcher.fetch_jobs(keywords, location)
            print(f'Found {len(all_jobs)} jobs')
            
            if not all_jobs:
                print('No jobs found, exiting...')
                return
            
            new_jobs = self.data_store.get_new_jobs(all_jobs)
            print(f'{len(new_jobs)} new jobs to process')
            
            if not new_jobs:
                print('No new jobs found, exiting...')
                return
            
            print('🤖 Matching jobs with AI...')
            matched_jobs = self.ai_matcher.match_jobs(new_jobs, self.user_profile)
            print(f'{len(matched_jobs)} jobs matched')
            
            if not matched_jobs:
                print('No matching jobs found')
                self.data_store.mark_jobs_as_sent([job['id'] for job in new_jobs])
                return
            
            print('✍️ Composing email...')
            email_content = self.ai_matcher.compose_email(matched_jobs, self.user_profile)
            
            print('📧 Sending email...')
            self.email_sender.send_email(
                os.getenv('FROM_EMAIL'),
                os.getenv('TO_EMAIL'),
                f'{len(matched_jobs)} New Job Matches Found',
                email_content
            )
            
            self.data_store.save_jobs(all_jobs)
            self.data_store.mark_jobs_as_sent([job['id'] for job in new_jobs])
            
            print('✅ Job alert completed successfully!')
            
        except Exception as e:
            print(f'❌ Error in job alert system: {e}')

if __name__ == '__main__':
    system = JobAlertSystem()
    system.run()