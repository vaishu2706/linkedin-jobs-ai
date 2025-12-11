from openai import OpenAI

class AIMatcher:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def match_jobs(self, jobs, user_profile):
        job_list = '\n'.join([f"{i+1}. {job['title']} at {job['company']} - {job['location']}" 
                             for i, job in enumerate(jobs)])
        
        prompt = f"""
Analyze these jobs and match them to this profile:
{user_profile}

Jobs:
{job_list}

Return only job numbers (1,2,3...) that are good matches, separated by commas. No explanation needed."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            
            matches = [int(n.strip()) - 1 for n in response.choices[0].message.content.split(',') 
                      if n.strip().isdigit()]
            matches = [i for i in matches if 0 <= i < len(jobs)]
            
            return [jobs[i] for i in matches]
        except Exception as e:
            print(f'AI matching failed: {e}')
            return jobs[:3]  # Fallback
    
    def compose_email(self, matched_jobs, user_profile):
        job_list = '\n\n'.join([f"• {job['title']} at {job['company']} - {job['location']}\n  {job['link']}" 
                               for job in matched_jobs])
        
        prompt = f"""
Write a professional email about these job opportunities for someone with this profile:
{user_profile}

Jobs:
{job_list}

Keep it concise, professional, and highlight why these are good matches. Include the job links."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f'Email composition failed: {e}')
            return self.fallback_email(matched_jobs)
    
    def fallback_email(self, jobs):
        job_list = '\n\n'.join([f"• {job['title']} at {job['company']}\n  Location: {job['location']}\n  Link: {job['link']}" 
                               for job in jobs])
        
        return f"""Subject: New Job Opportunities Found

Hi,

I found {len(jobs)} job opportunities that might interest you:

{job_list}

Best regards,
Your Job Alert System"""