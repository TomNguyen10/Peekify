import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from config import SENDER_EMAIL, SENDER_PASSWORD


def send_email(user_email: str, top_songs: list, top_artists: list, personalized_message: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD

    subject = "Your Weekly Music Report and Personalized Insights"

    html_template = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; color: #333; line-height: 1.6; }
            h1 { color: #4CAF50; }
            h2 { color: #333; margin-top: 20px; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .personalized-message {
                background-color: #f9f9f9;
                border-left: 5px solid #4CAF50;
                padding: 15px;
                margin-bottom: 20px;
            }
            .personalized-message p {
                margin-bottom: 15px;
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
        
        <div class="personalized-message">
            <h2>Your Personalized Insights</h2>
            {% for paragraph in personalized_message.split('\n\n') %}
                <p>{{ paragraph }}</p>
            {% endfor %}
        </div>
        
    </body>
    </html>
    """

    # Ensure personalized_message has double line breaks between paragraphs
    formatted_personalized_message = "\n\n".join(
        personalized_message.split('\n'))

    template = Template(html_template)
    rendered_html = template.render(
        top_songs=top_songs,
        top_artists=top_artists,
        personalized_message=formatted_personalized_message
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    msg.attach(MIMEText(rendered_html, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
        print(f"Email sent successfully to {user_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
