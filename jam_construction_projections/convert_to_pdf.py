#!/usr/bin/env python3
"""
Script to convert markdown and HTML files to PDF format.
Requires: pandoc to be installed on the system
"""

import subprocess
import os
import sys
from pathlib import Path

# Define the directory containing the files
WORKSPACE_DIR = Path(__file__).parent
OUTPUT_DIR = WORKSPACE_DIR / "pdfs"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)

def check_pandoc_installed():
    """Check if pandoc is installed."""
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pandoc():
    """Attempt to install pandoc."""
    print("Pandoc not found. Attempting to install...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "pandoc"], check=True)
        print("Pandoc installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install pandoc. Please install it manually:")
        print("  Ubuntu/Debian: sudo apt-get install pandoc")
        print("  macOS: brew install pandoc")
        print("  Or visit: https://pandoc.org/installing.html")
        return False

def convert_markdown_to_pdf(md_file):
    """Convert a markdown file to PDF."""
    pdf_file = OUTPUT_DIR / f"{md_file.stem}.pdf"
    try:
        subprocess.run(
            ["pandoc", str(md_file), "-o", str(pdf_file), "--from=markdown", "--to=pdf"],
            check=True,
            capture_output=True
        )
        print(f"✓ Converted: {md_file.name} → {pdf_file.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to convert {md_file.name}: {e.stderr.decode()}")
        return False

def convert_html_to_pdf(html_file):
    """Convert an HTML file to PDF."""
    pdf_file = OUTPUT_DIR / f"{html_file.stem}.pdf"
    try:
        subprocess.run(
            ["pandoc", str(html_file), "-o", str(pdf_file), "--from=html", "--to=pdf"],
            check=True,
            capture_output=True
        )
        print(f"✓ Converted: {html_file.name} → {pdf_file.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to convert {html_file.name}: {e.stderr.decode()}")
        return False

def main():
    """Main function to convert all files."""
    print("=" * 60)
    print("File to PDF Converter")
    print("=" * 60)
    
    # Check if pandoc is installed
    if not check_pandoc_installed():
        if not install_pandoc():
            sys.exit(1)
    
    print(f"\nOutput directory: {OUTPUT_DIR}\n")
    
    # Convert markdown files
    md_files = list(WORKSPACE_DIR.glob("*.md"))
    if md_files:
        print("Converting Markdown files:")
        for md_file in sorted(md_files):
            convert_markdown_to_pdf(md_file)
    else:
        print("No markdown files found in the workspace.")
    
    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
