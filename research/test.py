# TEST CHUNKING
from src.helper import load_pdf_file, text_split

extracted_data = load_pdf_file(
    "data/Gale Encyclopedia of Medicine Vol. 1 (A-B).pdf"
)

text_chunks = text_split(extracted_data)

print("Pages:", len(extracted_data))
print("Chunks:", len(text_chunks))

print(text_chunks[0])

