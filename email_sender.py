import requests

class EmailSender:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.resend.com'
    
    def send_email(self, from_email, to_email, subject, content):
        try:
            response = requests.post(f'{self.base_url}/emails', 
                json={
                    'from': from_email,
                    'to': [to_email],
                    'subject': subject,
                    'html': content.replace('\n', '<br>')
                },
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
            )
            
            response.raise_for_status()
            print(f'Email sent successfully: {response.json().get("id")}')
            return response.json()
        except Exception as e:
            print(f'Email sending failed: {e}')
            raise