from fpdf import FPDF
import os

CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)

def generate_cert(name, identity, course):
    pdf = FPDF(orientation='L')
    pdf.add_page()
    
    # Background
    pdf.set_fill_color(10, 25, 50)
    pdf.rect(0, 0, 297, 210, 'F')
    
    # Border
    pdf.set_draw_color(0, 168, 255)
    pdf.set_line_width(3)
    pdf.rect(10, 10, 277, 190)
    
    # Title
    pdf.set_font('Arial', 'B', 36)
    pdf.set_text_color(0, 168, 255)
    pdf.cell(0, 40, "CYBERSECURITY SCAN CERTIFICATE", 0, 1, 'C')
    
    # Content
    pdf.set_font('Arial', '', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 25, "This is to certify that", 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(74, 207, 250)
    pdf.cell(0, 30, name, 0, 1, 'C')
    
    pdf.set_font('Arial', '', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 25, f"of {identity}", 0, 1, 'C')
    pdf.cell(0, 25, f"has successfully completed the {course} security assessment", 0, 1, 'C')
    
    # Footer
    pdf.set_font('Arial', 'I', 16)
    pdf.set_text_color(150, 150, 150)
    pdf.set_y(160)
    pdf.cell(0, 10, "This certifies a scan was ethically performed under student project", 0, 1, 'C')
    
    # Save file
    filename = f"{CERT_DIR}/{name.replace(' ', '_')}_certificate.pdf"
    pdf.output(filename)
    return filename