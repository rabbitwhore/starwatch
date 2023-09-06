import re

def extract_domain_and_tld(url):
    # Regular expression to match the domain name and top-level domain (TLD)
    pattern = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.([a-zA-Z0-9.-]+)\/?'

    # Extract the domain name and TLD using regex
    match = re.search(pattern, url)
    if match:
        domain = match.group(1)
        tld = match.group(2)
        return domain, tld
    else:
        return None, None

# Example usage with the given URL
url = "https://www.danslogen.se/"
domain, tld = extract_domain_and_tld(url)

print(f"Original URL: {url}")
print(f"Extracted Domain: {domain}")
print(f"Extracted TLD: {tld}")
