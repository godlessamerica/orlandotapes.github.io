#!/usr/bin/env python3
"""
Migration script to update Orlando Tapes URLs from GitHub to Archive.org

This script helps you update feed.xml and index.html after uploading
your audio files to Archive.org.

IMPORTANT: Upload all MP3 files to Archive.org FIRST, then update
this mapping and run the script.
"""

# Mapping of current GitHub URLs to Archive.org URLs
# Based on actual Archive.org uploads using filename-based identifiers
URL_MAPPING = {
    # Episode 1: Dogsmiles
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-Dogsmiles-4.19.25-wills-pub.mp3": 
        "https://archive.org/download/ytf-dogsmiles-4.19.25-wills-pub/YTF-Dogsmiles-4.19.25-wills-pub.mp3",
    
    # Episode 2: Soft  
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-Soft-4.19.25-wills-pub.mp3": 
        "https://archive.org/download/ytf-soft-4.19.25-wills-pub/YTF-Soft-4.19.25-wills-pub.mp3",
    
    # Episode 3: Catnap
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-Catnap-4.19.25-wills-pub.mp3": 
        "https://archive.org/download/ytf-catnap-4.19.25-wills-pub/YTF-Catnap-4.19.25-wills-pub.mp3",
    
    # Episode 4: M.A.C.E.
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/M.A.C.E.-5.3.25-stardust-coffee.mp3": 
        "https://archive.org/download/m.-a.-c.-e.-5.3.25-stardust-coffee/M.A.C.E.-5.3.25-stardust-coffee.mp3",
    
    # Episode 5: S.M.O.P.
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/S.M.O.P.-stardust-coffee-and-video-5.3.25.mp3": 
        "https://archive.org/download/s.-m.-o.-p.-stardust-coffee-and-video-5.3.25/S.M.O.P.-stardust-coffee-and-video-5.3.25.mp3",
    
    # Episode 6: Misspell
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-Misspell-6.7.25.wills-pub.mp3": 
        "https://archive.org/download/ytf-misspell-6.7.25.wills-pub/YTF-Misspell-6.7.25.wills-pub.mp3",
    
    # Episode 7: Kitty Kitty Meow Meow
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-kitty-kitty-meow-meow-6.7.25.wills-pub.mp3": 
        "https://archive.org/download/ytf-kitty-kitty-meow-meow-6.7.25.wills-pub/YTF-kitty-kitty-meow-meow-6.7.25.wills-pub.mp3",
    
    # Additional episodes from mp3s directory
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-default-friends-6.7.25.wiils-pub.mp3": 
        "https://archive.org/download/ytf-default-friends-6-7-25-wills-pub/YTF-default-friends-6.7.25.wiils-pub.mp3",
    
    "https://github.com/godlessamerica/orlandotapes.github.io/raw/refs/heads/main/mp3s/YTF-No-Clue-6.7.25.wills-pub.mp3": 
        "https://archive.org/download/ytf-no-clue-6-7-25-wills-pub/YTF-No-Clue-6.7.25.wills-pub.mp3",
}

def update_feed_xml():
    """Update feed.xml with Archive.org URLs"""
    with open('feed.xml', 'r') as f:
        content = f.read()
    
    for github_url, archive_url in URL_MAPPING.items():
        content = content.replace(github_url, archive_url)
    
    with open('feed.xml', 'w') as f:
        f.write(content)
    
    print("✓ Updated feed.xml")

def update_index_html():
    """Update index.html with Archive.org URLs"""
    with open('index.html', 'r') as f:
        content = f.read()
    
    for github_url, archive_url in URL_MAPPING.items():
        content = content.replace(github_url, archive_url)
    
    with open('index.html', 'w') as f:
        f.write(content)
    
    print("✓ Updated index.html")

def verify_archive_urls():
    """Test that Archive.org URLs are accessible"""
    import urllib.request
    import urllib.error
    
    print("Testing Archive.org URLs...")
    for github_url, archive_url in URL_MAPPING.items():
        try:
            urllib.request.urlopen(archive_url)
            print(f"✓ {archive_url}")
        except urllib.error.URLError as e:
            print(f"✗ {archive_url} - Error: {e}")

if __name__ == "__main__":
    print("Orlando Tapes - Archive.org Migration Script")
    print("=" * 50)
    
    response = input("Have you uploaded ALL MP3 files to Archive.org? (y/N): ")
    if response.lower() != 'y':
        print("Please upload all MP3 files to Archive.org first!")
        print("See ARCHIVE-ORG-HOSTING.md for instructions.")
        exit(1)
    
    response = input("Have you updated the URL_MAPPING in this script? (y/N): ")
    if response.lower() != 'y':
        print("Please update the URL_MAPPING with your actual Archive.org URLs!")
        exit(1)
    
    print("\n1. Testing Archive.org URLs...")
    try:
        verify_archive_urls()
    except KeyboardInterrupt:
        print("\nURL verification interrupted. Some URLs may not be accessible.")
        response = input("Continue with migration anyway? (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            exit(1)
    
    response = input("\n2. Proceed with updating files? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        exit(1)
    
    print("\n3. Updating files...")
    update_feed_xml()
    update_index_html()
    
    print("\n✓ Migration complete!")
    print("\nNext steps:")
    print("1. Test the website locally: python -m http.server 8000")
    print("2. Verify all audio players work")
    print("3. Test RSS feed: curl https://orlandotapes.com/feed.xml")
    print("4. Commit and push changes: git add . && git commit -m 'Migrate to Archive.org hosting' && git push")
    print("5. Remove MP3 files from repository after confirming everything works")