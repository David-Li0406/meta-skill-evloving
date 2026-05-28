import argparse
import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Fetch RSS feed')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of articles')
    parser.add_argument('--title_include', type=str, help='Filter by title keyword')
    parser.add_argument('--keyword', type=str, dest='title_include', help='Alias for title_include')
    return parser.parse_args()

def fetch_rss(limit, title_include=None):
    # Construct URLs to try (Docker host first, then localhost)
    urls_to_try = [
        "http://host.docker.internal:4000/feeds/all.atom",
        "http://localhost:4000/feeds/all.atom"
    ]
    
    xml_content = None
    last_error = None
    
    # Try different URLs
    for base_url in urls_to_try:
        try:
            params = {}
            if limit:
                params['limit'] = limit
            if title_include:
                params['title_include'] = title_include
            
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            
            with urllib.request.urlopen(request, timeout=5) as response:
                xml_content = response.read()
                break # Success
        except Exception as e:
            last_error = e
            continue

    if xml_content is None:
        return {
            "version": "1.0.0",
            "operation": "list",
            "error": {
                "code": "RSS_CONNECTION_ERROR",
                "message": str(last_error),
                "suggestion": "Ensure WeWe-RSS service is running (tried host.docker.internal:4000 and localhost:4000)"
            }
        }
    
    try:    
        root = ET.fromstring(xml_content)
        # Handle namespaces if any (Atom usually has one)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        articles = []
        for entry in root.findall('atom:entry', ns):
            title_node = entry.find('atom:title', ns)
            if title_node is None:
                continue
                
            title = title_node.text or ""
            
            # Additional filtering if API didn't do it (or to be safe)
            if title_include and title_include not in title:
                continue
            
            # Extract ID
            id_node = entry.find('atom:id', ns)
            article_id = id_node.text if id_node is not None else ""
            
            # Extract Author
            author_node = entry.find('atom:author/atom:name', ns)
            author = author_node.text if author_node is not None else "Unknown"
            
            # Extract Date
            pub_node = entry.find('atom:published', ns)
            pub_date = pub_node.text if pub_node is not None else ""
            
            # Extract Link - FIX: ElementTree doesn't support [@rel="alternate"] in find() with namespaces reliably in all versions
            # iterate links to find the right one
            link_href = ""
            links = entry.findall('atom:link', ns)
            for link in links:
                if link.get('rel') == 'alternate' or not link.get('rel'):
                    link_href = link.get('href', "")
                    break
            
            # Extract Summary
            summary_node = entry.find('atom:summary', ns)
            summary = summary_node.text if summary_node is not None else ""

            article = {
                "id": article_id,
                "title": title,
                "author": author,
                "published_at": pub_date,
                "url": link_href,
                "summary": summary
            }
            articles.append(article)
            
            if len(articles) >= limit:
                break
                
        return {
            "version": "1.0.0",
            "operation": "list" if not title_include else "search",
            "result": {
                "type": "summary",
                "total_count": len(articles),
                "articles": articles,
                "query": {
                    "limit": limit,
                    "title_include": title_include
                }
            }
        }
        
    except Exception as e:
        return {
            "version": "1.0.0",
            "operation": "list",
            "error": {
                "code": "RSS_PARSE_ERROR",
                "message": f"Failed to parse XML: {str(e)}",
                "suggestion": "Check feed format"
            }
        }

if __name__ == "__main__":
    args = parse_args()
    result = fetch_rss(args.limit, args.title_include)
    print(json.dumps(result, ensure_ascii=False, indent=2))
