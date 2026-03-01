from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_requirements_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Project: E-Commerce Checkout System")
    
    # Body Text
    c.setFont("Helvetica", 12)
    text = [
        "Business Requirement Document (BRD-2026)",
        "",
        "1. Functional Requirements:",
        "- The system shall allow users to add items to a cart.",
        "- The system shall calculate tax based on user location (10% for California).",
        "- Users must be able to pay using Credit Card or PayPal.",
        "",
        "2. User Stories:",
        "- As a user, I want to receive an email confirmation after purchase.",
        "- As an admin, I want to see daily sales reports.",
        "",
        "3. Security:",
        "- All passwords must be hashed using BCrypt.",
        "- Sessions must expire after 30 minutes of inactivity."
    ]

    y = 720
    for line in text:
        c.drawString(100, y, line)
        y -= 20

    c.save()
    print(f"Success! {filename} created.")

if __name__ == "__main__":
    create_requirements_pdf("requirements.pdf")