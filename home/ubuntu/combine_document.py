#!/usr/bin/env python3

import os
import markdown
import re
from bs4 import BeautifulSoup

def combine_markdown_files(output_file):
    """
    Combines all markdown files into a single comprehensive document
    """
    # Order of files to include
    files = [
        "/home/ubuntu/introduction.md",
        "/home/ubuntu/system_architecture.md",
        "/home/ubuntu/database_schema.md",
        "/home/ubuntu/component_implementation.md",
        "/home/ubuntu/technical_considerations.md",
        "/home/ubuntu/implementation_roadmap.md",
        "/home/ubuntu/step_by_step_guide.md",
        "/home/ubuntu/visual_diagrams.md",
        "/home/ubuntu/appendices.md"
    ]
    
    combined_content = ""
    
    # Add title
    combined_content += "# Luxury Watch Price Optimization System - Technical Implementation Document\n\n"
    
    # Add table of contents
    with open("/home/ubuntu/document_structure.md", 'r') as f:
        toc = f.read()
        # Remove the title as we've already added it
        toc = re.sub(r'^#.*\n', '', toc)
        combined_content += toc + "\n\n"
    
    # Combine all content files
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                # Remove the title from each file to avoid duplication
                content = re.sub(r'^#.*\n', '', content)
                combined_content += content + "\n\n"
    
    # Write the combined content to the output file
    with open(output_file, 'w') as f:
        f.write(combined_content)
    
    print(f"Combined document created at {output_file}")
    
    # Convert to HTML for better formatting
    html_output = output_file.replace('.md', '.html')
    html_content = markdown.markdown(combined_content, extensions=['tables', 'fenced_code'])
    
    # Add some basic styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Luxury Watch Price Optimization System - Technical Implementation Document</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #2c3e50;
                margin-top: 24px;
                margin-bottom: 16px;
            }}
            h1 {{
                font-size: 2.5em;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
            }}
            h2 {{
                font-size: 2em;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
            }}
            code, pre {{
                font-family: Consolas, Monaco, 'Andale Mono', monospace;
                background-color: #f6f8fa;
                border-radius: 3px;
            }}
            pre {{
                padding: 16px;
                overflow: auto;
                line-height: 1.45;
            }}
            code {{
                padding: 0.2em 0.4em;
            }}
            pre code {{
                padding: 0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 16px;
            }}
            table, th, td {{
                border: 1px solid #dfe2e5;
            }}
            th, td {{
                padding: 8px 16px;
                text-align: left;
            }}
            th {{
                background-color: #f6f8fa;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            blockquote {{
                padding: 0 1em;
                color: #6a737d;
                border-left: 0.25em solid #dfe2e5;
                margin: 0 0 16px 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    with open(html_output, 'w') as f:
        f.write(styled_html)
    
    print(f"HTML version created at {html_output}")
    
    return output_file, html_output

if __name__ == "__main__":
    output_file = "/home/ubuntu/luxury_watch_price_optimization_system.md"
    combine_markdown_files(output_file)
