import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found")

# Added basepath to the signature
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(from_path):
            # Pass basepath down the recursive call
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        elif entry.endswith(".md"):
            base_name, _ = os.path.splitext(dest_path)
            html_dest_path = f"{base_name}.html"
            # Pass basepath to the page generator
            generate_page(from_path, template_path, html_dest_path, basepath)

# Added basepath to the signature
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r', encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, 'r', encoding="utf-8") as f:
        template = f.read()

    title = extract_title(markdown_content)
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # 1. Replace standard placeholders
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # 2. Replace relative links/sources with the basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w', encoding="utf-8") as f:
        f.write(full_html)