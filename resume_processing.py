from langchain_community.document_loaders import PyMuPDFLoader

def extract_text_from_pdf(pdf_path):
    try:
        loader = PyMuPDFLoader(pdf_path)
        data = loader.load()
        return "\n\n".join([doc.page_content for doc in data])
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")