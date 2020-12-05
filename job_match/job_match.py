from resume_parser import resume_parser

def get_resume_text(file_path):
    """ Wrapper Function to get text from resume"""
    txt= resume_parser.get_text(file_path)
    return txt


get_resume_text("data/sample_input.pdf")