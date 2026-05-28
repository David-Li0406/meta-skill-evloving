import sys
import urllib.parse
import json

# Configuration for Affiliate Tags
AFFILIATE_TAGS = {
    "amazon": "adhdsupps-20",
    "iherb": "ADHDSUPPS"
}

def generate_affiliate_link(product_token, platform="amazon"):
    """
    Generates a standardized affiliate link based on the platform.
    """
    platform = platform.lower()
    
    if platform == "amazon":
        # Amazon format: https://amazon.com/dp/{ASIN}?tag={TAG}
        base_url = f"https://www.amazon.com/dp/{product_token}"
        params = {"tag": AFFILIATE_TAGS["amazon"]}
        
    elif platform == "iherb":
        # iHerb format: https://iherb.com/pr/{slug}/{id}?rcode={TAG}
        # Assuming product_token is the product ID or slug
        base_url = f"https://www.iherb.com/pr/product/{product_token}"
        params = {"rcode": AFFILIATE_TAGS["iherb"]}
        
    else:
        return json.dumps({
            "error": f"Unsupported platform: {platform}",
            "supported": list(AFFILIATE_TAGS.keys())
        })

    # Construct final URL
    query_string = urllib.parse.urlencode(params)
    final_url = f"{base_url}?{query_string}"
    
    return json.dumps({
        "platform": platform,
        "product_token": product_token,
        "affiliate_link": final_url,
        "tag_used": AFFILIATE_TAGS[platform]
    }, indent=2)

if __name__ == "__main__":
    # Usage: python link_gen.py [product_token] [platform]
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python link_gen.py [product_token] [platform]"}));
        sys.exit(1)
        
    token = sys.argv[1]
    plat = sys.argv[2] if len(sys.argv) > 2 else "amazon"
    
    print(generate_affiliate_link(token, plat))
