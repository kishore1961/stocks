import os
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
import io
import camelot
import pdfplumber
from pathlib import Path

class PDFExtractor:
    def __init__(self, pdf_path, output_dir="extracted_content"):
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.images_dir = self.output_dir / "images"
        self.text_dir = self.output_dir / "text"
        self.tables_dir = self.output_dir / "tables"
        
        for dir_path in [self.images_dir, self.text_dir, self.tables_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def extract_images(self):
        """Extract all images from PDF using PyMuPDF"""
        print("Extracting images...")
        doc = fitz.open(self.pdf_path)
        image_count = 0
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_data = pix.tobytes("png")
                    img_name = f"page_{page_num + 1}_img_{img_index + 1}.png"
                    img_path = self.images_dir / img_name
                    
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_data)
                    
                    image_count += 1
                    print(f"Saved: {img_name}")
                
                pix = None
        
        doc.close()
        print(f"Total images extracted: {image_count}")
        return image_count
    
    def extract_text(self):
        """Extract text from PDF using multiple methods"""
        print("Extracting text...")
        
        # Method 1: PyMuPDF - Good for general text extraction
        self._extract_text_pymupdf()
        
        # Method 2: pdfplumber - Better for structured text
        self._extract_text_pdfplumber()
        
        print("Text extraction completed")
    
    def _extract_text_pymupdf(self):
        """Extract text using PyMuPDF"""
        doc = fitz.open(self.pdf_path)
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            full_text += f"\n--- Page {page_num + 1} ---\n"
            full_text += text
            
            # Save individual page text
            page_text_path = self.text_dir / f"page_{page_num + 1}_pymupdf.txt"
            with open(page_text_path, "w", encoding="utf-8") as f:
                f.write(text)
        
        # Save complete text
        complete_text_path = self.text_dir / "complete_text_pymupdf.txt"
        with open(complete_text_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        doc.close()
    
    def _extract_text_pdfplumber(self):
        """Extract text using pdfplumber - better for structured content"""
        with pdfplumber.open(self.pdf_path) as pdf:
            full_text = ""
            
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {page_num + 1} ---\n"
                    full_text += text
                    
                    # Save individual page text
                    page_text_path = self.text_dir / f"page_{page_num + 1}_pdfplumber.txt"
                    with open(page_text_path, "w", encoding="utf-8") as f:
                        f.write(text)
            
            # Save complete text
            complete_text_path = self.text_dir / "complete_text_pdfplumber.txt"
            with open(complete_text_path, "w", encoding="utf-8") as f:
                f.write(full_text)
    
    def extract_tables(self):
        """Extract tables using both camelot and pdfplumber"""
        print("Extracting tables...")
        
        # Method 1: Camelot - Good for well-defined tables
        self._extract_tables_camelot()
        
        # Method 2: pdfplumber - Good for various table formats
        self._extract_tables_pdfplumber()
        
        print("Table extraction completed")
    
    def _extract_tables_camelot(self):
        """Extract tables using camelot"""
        try:
            # Try lattice method first (for tables with lines)
            tables = camelot.read_pdf(self.pdf_path, pages='all', flavor='lattice')
            
            if len(tables) == 0:
                # Try stream method (for tables without lines)
                tables = camelot.read_pdf(self.pdf_path, pages='all', flavor='stream')
            
            for i, table in enumerate(tables):
                # Save as CSV
                csv_path = self.tables_dir / f"table_{i + 1}_camelot.csv"
                table.to_csv(str(csv_path))
                
                # Save as Excel
                excel_path = self.tables_dir / f"table_{i + 1}_camelot.xlsx"
                table.df.to_excel(str(excel_path), index=False)
                
                print(f"Saved table {i + 1} from page {table.parsing_report['page']}")
        
        except Exception as e:
            print(f"Camelot extraction failed: {e}")
    
    def _extract_tables_pdfplumber(self):
        """Extract tables using pdfplumber"""
        with pdfplumber.open(self.pdf_path) as pdf:
            table_count = 0
            
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table_idx, table in enumerate(tables):
                    if table:  # Check if table is not empty
                        df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                        
                        table_count += 1
                        
                        # Save as CSV
                        csv_path = self.tables_dir / f"page_{page_num + 1}_table_{table_idx + 1}_pdfplumber.csv"
                        df.to_csv(csv_path, index=False)
                        
                        # Save as Excel
                        excel_path = self.tables_dir / f"page_{page_num + 1}_table_{table_idx + 1}_pdfplumber.xlsx"
                        df.to_excel(excel_path, index=False)
                        
                        print(f"Saved table from page {page_num + 1}")
            
            print(f"Total tables extracted with pdfplumber: {table_count}")
    
    def extract_all(self):
        """Extract all content types"""
        print(f"Starting extraction from: {self.pdf_path}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 50)
        
        # Extract images
        self.extract_images()
        print("-" * 50)
        
        # Extract text
        self.extract_text()
        print("-" * 50)
        
        # Extract tables
        self.extract_tables()
        print("-" * 50)
        
        print("Extraction completed!")
        print(f"Check the '{self.output_dir}' directory for extracted content.")
    
    def get_summary(self):
        """Get summary of extracted content"""
        summary = {
            'images': len(list(self.images_dir.glob('*.png'))),
            'text_files': len(list(self.text_dir.glob('*.txt'))),
            'tables_csv': len(list(self.tables_dir.glob('*.csv'))),
            'tables_excel': len(list(self.tables_dir.glob('*.xlsx')))
        }
        
        print("\n=== EXTRACTION SUMMARY ===")
        print(f"Images extracted: {summary['images']}")
        print(f"Text files created: {summary['text_files']}")
        print(f"Tables (CSV): {summary['tables_csv']}")
        print(f"Tables (Excel): {summary['tables_excel']}")
        
        return summary


# Example usage
if __name__ == "__main__":
    # Replace with your PDF path
    pdf_path = "gensol.pdf"
    
    # Create extractor instance
    extractor = PDFExtractor(pdf_path, output_dir="extracted_pdf_content")
    
    # Extract all content
    extractor.extract_all()
    
    # Get summary
    extractor.get_summary()
    
    # Or extract specific content types:
    # extractor.extract_images()
    # extractor.extract_text()
    # extractor.extract_tables()