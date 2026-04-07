import os
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'link', 'img', 'script'):
            for attr, value in attrs:
                if attr in ('href', 'src'):
                    if value:
                        self.links.append(value)

def check_links():
    root_dir = '/Users/naga-itrust/Downloads/jianying-zhou.github.io-main'
    broken_links = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
                
            filepath = os.path.join(dirpath, filename)
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            parser = LinkParser()
            parser.feed(content)
            
            for href in parser.links:
                # Ignore mailto, javascript, external links, anchor links
                if href.startswith(('mailto:', 'javascript:', 'http://', 'https://', 'tel:', '#')):
                    continue
                    
                parsed_url = urlparse(href)
                target_path = unquote(parsed_url.path)
                
                if not target_path:
                    continue
                    
                if target_path.startswith('/'):
                    # relative to root_dir
                    target_full_path = os.path.join(root_dir, target_path.lstrip('/'))
                else:
                    # relative to current file
                    target_full_path = os.path.normpath(os.path.join(dirpath, target_path))
                    
                if not os.path.exists(target_full_path):
                    broken_links.append({
                        'file': os.path.relpath(filepath, root_dir),
                        'broken_link': href,
                        'expected_path': os.path.relpath(target_full_path, root_dir) if target_full_path.startswith(root_dir) else target_full_path
                    })
                    
    if broken_links:
        print("Broken links found:")
        for link in broken_links:
            print(f"File: {link['file']} -> Missing: {link['broken_link']} (Expected path: {link['expected_path']})")
    else:
        print("No broken local links found!")

if __name__ == '__main__':
    check_links()
