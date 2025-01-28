import PyPDF2
import io

async def process_pdf(file) -> str:
    try:
        # Verify file type
        if not file.filename.lower().endswith('.pdf'):
            raise Exception("Only PDF files are supported")

        # Read file content
        content = await file.read()
        if not content:
            raise Exception("Empty file uploaded")

        # Create PDF reader
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            raise Exception("Invalid or corrupted PDF file")

        # Extract text
        text = ""
        try:
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            raise Exception("Could not extract text from PDF")

        # Check if any text was extracted
        if not text.strip():
            raise Exception("No readable text found in PDF")

        return text.strip()

    except Exception as e:
        print(f"PDF Processing Error: {str(e)}")
        raise Exception(f"Error processing PDF: {str(e)}") 