"""
URL Shortener Client Library
Use this to integrate URL shortening into other Python applications
"""

import requests
from typing import Optional, Dict, List

class URLShortenerClient:
    def __init__(self, backend_url: str = "http://localhost:5000"):
        self.backend_url = backend_url.rstrip('/')
        self.session = requests.Session()
    
    def shorten(self, long_url: str) -> Dict:
        """
        Shorten a URL
        
        Args:
            long_url: The URL to shorten
            
        Returns:
            Dictionary with short_code, short_url, long_url, clicks
        """
        response = self.session.post(
            f"{self.backend_url}/api/shorten",
            json={"long_url": long_url}
        )
        response.raise_for_status()
        return response.json()
    
    def get_all(self) -> List[Dict]:
        """
        Get all shortened URLs
        
        Returns:
            List of URL mappings
        """
        response = self.session.get(f"{self.backend_url}/api/urls")
        response.raise_for_status()
        return response.json()
    
    def get_info(self, short_code: str) -> Dict:
        """
        Get information about a shortened URL
        
        Args:
            short_code: The short code
            
        Returns:
            Dictionary with URL information
        """
        response = self.session.get(f"{self.backend_url}/api/url/{short_code}")
        response.raise_for_status()
        return response.json()
    
    def delete(self, short_code: str) -> Dict:
        """
        Delete a shortened URL
        
        Args:
            short_code: The short code to delete
            
        Returns:
            Deletion confirmation
        """
        response = self.session.delete(f"{self.backend_url}/api/url/{short_code}")
        response.raise_for_status()
        return response.json()
    
    def get_redirect_url(self, short_code: str) -> str:
        """
        Get the redirect URL for a short code (without following redirect)
        
        Args:
            short_code: The short code
            
        Returns:
            The original long URL
        """
        info = self.get_info(short_code)
        return info['long_url']


# Example usage
if __name__ == "__main__":
    client = URLShortenerClient()
    
    # Shorten a URL
    result = client.shorten("https://www.github.com/some/very/long/url/that/needs/shortening")
    print(f"Shortened URL: {result['short_url']}")
    
    # Get all URLs
    all_urls = client.get_all()
    print(f"Total URLs: {len(all_urls)}")
    
    # Get info about a URL
    info = client.get_info(result['short_code'])
    print(f"Clicks: {info['clicks']}")
