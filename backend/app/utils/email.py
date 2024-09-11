import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template  # Import Jinja2 Template
from config import SENDER_EMAIL, SENDER_PASSWORD

# Email sending function


def send_top_songs_email(user_email: str, top_songs: list, top_artists: list):
    # Define the SMTP email server (Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = SENDER_EMAIL  # Your Gmail address
    sender_password = SENDER_PASSWORD  # The App Password generated above

    # Email subject and recipient
    subject = "Your Top 5 Most Listened Tracks and Artists From Last Week"

    # HTML email template using Jinja2
    html_template = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; color: #333; }
            h1 { color: #4CAF50; }
            h2 { color: #333; }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            ol {
                padding-left: 20px;
            }
            li {
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Weekly Music Report</h1>
        
        <h2>Top 5 Most Listened-to Songs</h2>
        <table>
            <thead>
                <tr>
                    <th>Track Name</th>
                    <th>Artist</th>
                    <th>Album</th>
                    <th>Play Count</th>
                </tr>
            </thead>
            <tbody>
            {% for song in top_songs %}
                <tr>
                    <td>{{ song['track_name'] }}</td>
                    <td>{{ song['artist_name'] }}</td>
                    <td>{{ song['album_name'] }}</td>
                    <td>{{ song['play_count'] }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        
        <h2>Top 5 Most Listened-to Artists</h2>
        <table>
            <thead>
                <tr>
                    <th>Artist Name</th>
                    <th>Play Count</th>
                </tr>
            </thead>
            <tbody>
            {% for artist in top_artists %}
                <tr>
                    <td>{{ artist['artist_name'] }}</td>
                    <td>{{ artist['play_count'] }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        
        <p>Keep up the good vibes!</p>
        <p>Best, <br>Your Music App Team</p>
    </body>
    </html>
    """

    # Render the HTML template with Jinja2
    template = Template(html_template)
    rendered_html = template.render(
        top_songs=top_songs, top_artists=top_artists)

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    # Attach the rendered HTML content to the email
    msg.attach(MIMEText(rendered_html, "html"))

    # Send the email using Gmail's SMTP server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            # Login with email and App Password
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
        print(f"Email sent successfully to {user_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
