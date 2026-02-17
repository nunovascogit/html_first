import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # 1. Use os.listdir() to see what is in the current directory
    for entry in os.listdir(dir_path_content):
        # Construct source and destination paths
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        # 2. Check if directory
        if os.path.isdir(from_path):
            # RECURSION: Call the function again for the subdirectory
            generate_pages_recursive(from_path, template_path, dest_path)
        
        # 3. If markdown file, call generate_page
        elif entry.endswith(".md"):
            # splitext separates the file root from the LAST extension ONLY
            base_path, _ = os.path.splitext(dest_path)
            html_dest_path = f"{base_path}.html"
            
            generate_page(from_path, template_path, html_dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read the markdown file
    with open(from_path, 'r', encoding="utf-8") as f:
        markdown_content = f.read()

    # 2. Read the template file
    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()

    # 3. Use markdown_to_html_node and extract_title
    # Note: .to_html() is called on the resulting ParentNode
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)

    # 4. Replace placeholders using .replace()
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # 5. Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    # 6. Write the result to the destination
    with open(dest_path, 'w', encoding="utf-8") as f:
        f.write(full_html)