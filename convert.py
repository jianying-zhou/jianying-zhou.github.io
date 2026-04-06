import sys, re

# Read index.html to steal the header and footer
with open('index.html', 'r') as f:
    idx = f.read()

header_match = re.search(r'(.*?<main class="content">\n)', idx, flags=re.DOTALL)
header_html = header_match.group(1)

footer_match = re.search(r'(  </main>\n</div>\n\n.*|  </main>\n\n</div>\n\n.*)', idx, flags=re.DOTALL)
if footer_match:
    footer_html = footer_match.group(1)
else:
    footer_html = "  </main>\n</div>\n</body>\n</html>"

def convert_file(filename, title):
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
    
    # Strip the old HTML outer tags
    start_idx = content.find('<hr>')
    if start_idx == -1:
        # Fallback
        body_start = content.find('<BODY>')
        if body_start != -1:
            start_idx = body_start + 6
        else:
            start_idx = 0
            
    end_idx = content.rfind('</font>')
    if end_idx == -1:
        end_idx = content.rfind('</BODY>')
    if end_idx == -1:
        end_idx = len(content)
        
    inner = content[start_idx:end_idx]
    
    # Clean up instances of relative jianying.space refs
    inner = inner.replace('http://jianying.space/', 'https://jianying-zhou.github.io/')
    
    # Some older files don't have titles in the same way, but let's wrap it in a section
    page_content = f'<section class="sec">\n  <h2 class="sec-title">{title}</h2>\n{inner}\n</section>\n'
    
    final_html = header_html.replace('<title>Jianying Zhou — Professor of Cybersecurity, SUTD</title>', f'<title>Jianying Zhou — {title}</title>') 
    
    # Special: make the sidebar highlight the active item? Not doing it for now to keep it simple, 
    # except maybe if we want to remove active class, we can leave as is.

    final_html += page_content + footer_html
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
convert_file('professional.html', 'Professional Activities')
convert_file('publications.html', 'Publications')
convert_file('conference-ranking.html', 'Conference Ranking')

print("Conversion completed successfully.")
