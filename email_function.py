## email function 
def send_email_with_attachment(receiver_email, subject, body, attachment_path):
    sender_email = EMAIL  # email
    sender_password = PASSWORD       # password
    smtp_server = "smtp.gmail.com"         # SMTP server
    smtp_port = 587                          # Port for TLS
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    # Attach the file if it exists
    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            message.attach(part)
    else:
        print(f"Attachment file {attachment_path} not found.")
        return False
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")
        return False
        
        
        
        
        
#function call: (for better understanding)  
# SQL query to fetch invoice data
fetch_range_query = """
    SELECT invoices.invoice_id, customers.name, invoices.amount, customers.email, invoices.file
    FROM invoices
    JOIN customers ON invoices.customer_id = customers.id
    WHERE invoices.invoice_id BETWEEN %s AND %s;
"""

# Execute the SQL query with the given invoice number range
cursor.execute(fetch_range_query, (invoice_from, invoice_to))

# Fetch the invoices that haven't been sent yet
unsent_invoices = cursor.fetchall()

# Iterate through all unsent invoices
for invoice_id, name, amount, email, file_name in unsent_invoices:
    # Prepare the email
    subject = f"Invoice #{invoice_id}"
    body = f"Dear Sir/Madam,\n\nAttached is your invoice #{invoice_id} for the amount of {amount}€.\n\nBest regards,\nYour Service Team"
    
    # Set the path for the PDF attachment (using the file name)
    attachment_path = os.path.join("/home/...", file_name)  # Adjust the path where PDFs are stored
    
    # Attempt to send the email with the attachment
    email_sent = send_email_with_attachment(email, subject, body, attachment_path)
