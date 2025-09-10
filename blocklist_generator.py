"""Generates an IP blocklist file for use with Nginx"""

# Standard libraries
import re
from datetime import datetime

# Third-party libraries
import requests
import toml

PARENT_DIR = '/'.join(__file__.replace('\\', '/').split('/')[:-1])
CONFIG_PATH = 'config.toml'

def load_config() -> dict:
    """Load configuration from the TOML file"""
    with open(file=f'{PARENT_DIR}/{CONFIG_PATH}', mode='r', encoding='utf-8') as config_file:
        return toml.load(config_file)

def fetch_blocklist(url: str, ip_set: set) -> set:
    """Fetch blocklist from a given URL and return a set of IPs"""
    response = requests.get(url.strip())
    response.raise_for_status()

    for line in response.text.splitlines():
        # Skip comments and empty lines
        if line.startswith('#') or line.startswith(';') or not line.strip():
            continue

        # Extract IP address using regex
        match = re.match(r'(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?', line)
        if match:
            ip_set.add(match.group(0))

def main():
    """Main function to generate the blocklist"""
    config = load_config()
    ip_set = set()

    for source in config.get('sources'):
        try:
            print(f"Fetching blocklist from {source}...")
            fetch_blocklist(source, ip_set)
        except requests.RequestException as e:
            print(f"Error fetching {source}: {e}")

    with open(file=config.get('output_file'), mode='w', encoding='utf-8') as output_file:
        output_file.write("# Auto-generated blocklist (\n")
        output_file.write(f"# Generated on {datetime.utcnow().isoformat()} UTC\n")
        output_file.write("# Total unique IPs: {}\n".format(len(ip_set)))
        output_file.write("default 0;\n")
        for ip in sorted(ip_set):
            output_file.write(f"{ip} 1;\n")

if __name__ == "__main__":
   # main()
   pass
