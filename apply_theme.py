import os
import re

target_dirs = ['acns', 'asiaccs', 'cpss', 'spt', 'WPES2025']
root_dir = os.path.dirname(os.path.abspath(__file__))
google_fonts = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'

updated_files = 0

for d in target_dirs:
    dir_path = os.path.join(root_dir, d)
    if not os.path.exists(dir_path):
        print(f"Directory not found, skipping: {dir_path}")
        continue
        
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html') or file.endswith('.htm'):
                file_path = os.path.join(root, file)
                rel_to_root = os.path.relpath(root_dir, root)
                style_path = os.path.join(rel_to_root, 'style.css').replace('\\', '/')
                style_link = f'<link rel="stylesheet" href="{style_path}">'
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='ISO-8859-1') as f:
                        content = f.read()
                
                injected = False
                
                # Check if already injected
                if 'Outfit' not in content or 'style.css' not in content:
                    injection = f'\n{google_fonts}\n{style_link}\n'
                    head_match = re.search(r'(<head[^>]*>)', content, flags=re.IGNORECASE)
                    
                    if head_match:
                        content = content[:head_match.end()] + injection + content[head_match.end():]
                        injected = True
                    else:
                        html_match = re.search(r'(<html[^>]*>)', content, flags=re.IGNORECASE)
                        if html_match:
                            content = content[:html_match.end()] + injection + content[html_match.end():]
                            injected = True
                        else:
                            content = injection + content
                            injected = True
                            
                if injected:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {file_path}")
                    updated_files += 1

print(f"Update complete! Modified {updated_files} files.")
