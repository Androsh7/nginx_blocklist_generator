# Nginx_Blocklist_Generator

Compiles a list of malicious ip addresses to implement nginx IP blocklists

# Setup service with Cron
Either run the service manually or run it automatically using a cronjob:

NOTE: the nginx service needs to be reloaded for the new blacklist to be used
```
0 2 * * * /usr/bin/python /opt/nginx_blacklist_generator/blacklist_generator.py ; nginx -s reload
```

# Add blacklist to nginx.conf

```
# http { ... }
geo $block_ip {
    include /path/to/blacklist/file.txt;
}

server {
    ...
    # Silently drop blocked IPs
    if ($block_ip) {
        return 444;
    }
    ...
}