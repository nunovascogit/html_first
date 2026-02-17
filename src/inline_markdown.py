import re
from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        
        #unmatched delimiter
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' found.")

        split_nodes = []
        for i in range (len(parts)):
            if parts[i] == "":
                continue
            # even indices = surrounding text; odd indices = delimited content
            if i % 2 == 0:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(parts[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes        

def extract_markdown_images(text):
    #regex pattern
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # re.findall return list of tupels (Group1, Group 2)
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue 

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            parts = text.split(markdown, 1)
            before = parts[0]
            after = parts[1] if len (parts) > 1 else ""
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
           


            text = after
  
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))    

    return new_nodes    

def extract_markdown_links(text):
    pattern = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text) 
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue
 
        for link_text, url in links:
            markdown = f"[{link_text}]({url})"
            parts = text.split(markdown, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""
       
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))


            text = after
 
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes        
            

if __name__ == "__main__":
    node = TextNode(
        "Start ![one](url1)middle ![two](ulr2) end",
        TextType.TEXT,
    )
    print(split_nodes_image([node]))
