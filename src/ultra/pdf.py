from fpdf import FPDF  

def text_to_pdf(title: str):
    input_path = f"transcript/{title}-sentences.txt"
    output_path = f"transcript/{title}-final.pdf"
    
    with open(input_path, "r") as input_file:
        text = input_file.read()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_path)