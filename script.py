import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(workflow_name, repo_name, workflow_run_id):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    subject = f"Workflow {workflow_name} failed for repo {repo_name}"
    body = (
        f"Hi, the workflow '{workflow_name}' has failed for the repository '{repo_name}'. "
        f"Please check the details.\n\nMore Details:\nRun_ID: {workflow_run_id}"
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Call the function with all required arguments
send_email(
    os.getenv('WORKFLOW_NAME'),
    os.getenv('REPO_NAME'),
    os.getenv('WORKFLOW_RUN_ID')
)
