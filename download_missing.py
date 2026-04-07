import os
import urllib.request
import re
import ssl

# Ignore SSL verification just in case
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    root_dir = '/Users/naga-itrust/Downloads/jianying-zhou.github.io-main'
    broken_links_file = os.path.join(root_dir, 'broken_links.txt')
    
    if not os.path.exists(broken_links_file):
        print("broken_links.txt not found!")
        return

    with open(broken_links_file, 'r') as f:
        content = f.read()

    expected_paths = set(re.findall(r'\(Expected path: (.*?)\)', content))
    base_url = "http://jianying.space/"

    for path in expected_paths:
        rel_path = path
        
        # Handle the stray search path out of directory bounds
        if "search" in path and path.startswith('/Users/'):
            rel_path = "search/"
            
        # Clean leading slashes
        rel_path = rel_path.lstrip('/')
        
        # If it's a directory (like search/), make it an index or ignore, or we hit it and see what it is
        # Actually search is probably not a static file, but let's try
        
        url = base_url + rel_path
        
        # Determine local path relative to root
        # if rel_path is search/ we might download it as search/index.html
        local_target = os.path.join(root_dir, rel_path)
        
        if local_target.endswith('/'):
            local_target = os.path.join(local_target, 'index.html')
            url = url + '/' # Ensure trailing slash for directory fetching
            
        os.makedirs(os.path.dirname(local_target) or '.', exist_ok=True)
        
        print(f"Attempting to download {url} -> {local_target}")
        
        try:
            urllib.request.urlretrieve(url, local_target)
            print(f" -> SUCCESS")
        except Exception as e:
            # Try appending a trailing slash if it didn't have one and failed as 403 or 404 (maybe it's a directory)
            if not url.endswith('/') and "search" in url:
                try:
                    local_target_dir = os.path.join(local_target, 'index.html')
                    os.makedirs(os.path.dirname(local_target_dir), exist_ok=True)
                    url_dir = url + '/'
                    urllib.request.urlretrieve(url_dir, local_target_dir)
                    print(f" -> SUCCESS (as directory)")
                    continue
                except:
                    pass
            print(f" -> FAILED: {e}")

if __name__ == '__main__':
    main()
