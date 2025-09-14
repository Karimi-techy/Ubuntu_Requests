import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_image(url):
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch the image with timeout
        response = requests.get(url, timeout=10, headers={"User-Agent": "UbuntuFetcher/1.0"})
        response.raise_for_status()  # Raise error for bad status codes

        # Check Content-Type to ensure it's an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # Generate filename if missing
        if not filename:
            filename = "downloaded_image.jpg"

        # Prevent duplicate downloads by hashing content
        file_hash = hashlib.md5(response.content).hexdigest()
        filename = f"{file_hash[:8]}_{filename}"

        filepath = os.path.join("Fetched_Images", filename)

        if os.path.exists(filepath):
            print(f"⚠ Duplicate skipped: {filename}")
            return

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter image URLs (comma-separated): ").split(",")

    for url in urls:
        url = url.strip()
        if url:
            fetch_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
