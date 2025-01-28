import asyncio
import aiofiles
from fastapi import UploadFile
import os

async def test_pdf_upload(file_path: str):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return

        # Create UploadFile object
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()
            upload_file = UploadFile(
                filename=os.path.basename(file_path),
                file=None,
                content_type="application/pdf"
            )
            upload_file.file = content

        # Import processor
        from app.api.services.pdf_processor import process_pdf
        
        # Process PDF
        print(f"Processing {file_path}...")
        result = await process_pdf(upload_file)
        
        print("✓ PDF processed successfully!")
        print(f"Extracted text length: {len(result)} characters")
        print("\nFirst 200 characters of extracted text:")
        print("-" * 50)
        print(result[:200] + "...")
        
    except Exception as e:
        print(f"✗ Error testing PDF: {str(e)}")

if __name__ == "__main__":
    # Test with a sample PDF
    pdf_path = "path/to/your/test.pdf"  # Update this path
    asyncio.run(test_pdf_upload(pdf_path)) 