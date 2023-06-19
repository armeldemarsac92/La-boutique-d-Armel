from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

with open('../Assets/Data/mail_credentials.json') as f:
    data = json.load(f)
    email = data['email']
    password = data['password']

df = pd.read_csv('../Assets/Data/item_data_scrapped_from_vinted.csv')
todays_date = date.today().strftime("%d/%m/%Y")


filtered_df_added = df[(df['date_scrapped'] == todays_date) & (df['item_size'].notnull())]
filtered_df_sold = df[(df['item_date_sold'] == todays_date) & (df['item_size'].notnull())]

added_sizes_stats = {}
sold_sizes_stats = {}



sizes = [
    'XS\n',
    'S\n',
    'M\n',
    'L\n',
    'XL\n',
    'XXL\n'
]

for size in sizes:
    added_sizes_stats[size] = len(filtered_df_added[filtered_df_added['item_size'].str.contains(size)])
    sold_sizes_stats[size] = len(filtered_df_sold[filtered_df_sold['item_size'].str.contains(size)])

# Define the file path and name
output_file = '../Assets/Data/activity_log.pdf'

# Create a PDF document with A4 size
doc = SimpleDocTemplate(output_file, pagesize=A4)

# Set up the document styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Title'],
    fontName='Helvetica-Bold',
    fontSize=24,
    textColor=colors.darkblue,
    spaceAfter=30
)
section_title_style = ParagraphStyle(
    'SectionTitleStyle',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=16,
    textColor=colors.darkred,
    spaceAfter=10
)
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

# Create the content for the PDF document
story = []

# Add a title to the log
title = Paragraph("Boutique Activity Log", title_style)
story.append(title)
story.append(Spacer(1, 20))

# Add a custom greeting message
greeting_message = f"Hey! I hope you had a good night. Here are some stats about the boutique activity on {todays_date}. " \
                   "Have a good day, Armel."
greeting = Paragraph(greeting_message, styles["BodyText"])
story.append(greeting)
story.append(Spacer(1, 20))

# Add a section for each size
for size in sizes:
    section_title = Paragraph(f"For size {size}:", section_title_style)
    story.append(section_title)

    # Create a table to display the stats
    data = [
        ["Items sold yesterday", sold_sizes_stats[size]],
        ["Items scrapped", added_sizes_stats[size]]
    ]
    table = Table(data, colWidths=[200, 100], style=table_style)
    story.append(table)
    story.append(Spacer(1, 20))

# Calculate the total counts
total_added = sum(added_sizes_stats.values())
total_sold = sum(sold_sizes_stats.values())

# Add a section for total counts
total_section_title = Paragraph("Total Counts:", section_title_style)
story.append(total_section_title)

# Create a table for total counts
total_data = [
    ["Total items sold yesterday", total_sold],
    ["Total items scrapped to review", total_added]
]
total_table = Table(total_data, colWidths=[200, 100], style=table_style)
story.append(total_table)

# Build the PDF document
doc.build(story)

print(f"Log file has been generated: {output_file}")

# Send the log file via email
sender_email = "armeldemarsac@gmail.com"
receiver_email = "hrw4718cjat5n0@print.epsonconnect.com"
subject = "Boutique Activity Log"

# Create a multipart message and set the headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add the PDF log file as an attachment
with open(output_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename=activity_log.pdf",
)

message.attach(part)

# Connect to the SMTP server and send the email
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = email
smtp_password = password

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")

