# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Orlando Tapes is a static website for a live music podcast documenting Orlando, FL's underground music scene. It features live recordings from iconic venues like Will's Pub and Stardust Coffee & Video.

## Architecture & Structure

**Static Site Setup:**
- Hosted on GitHub Pages at `orlandotapes.com`
- Single-page application using vanilla HTML, CSS, and JavaScript
- Audio files hosted on Archive.org for unlimited file sizes
- Images stored in `/images/` directory

**Key Components:**
- `index.html` - Main landing page with embedded podcast episodes
- `feed.xml` - RSS podcast feed with iTunes/Podcast Index namespace support
- `sitemap.xml` - SEO sitemap for search engines
- `styles.css` - Dark mode styling optimized for music content
- `update_feed_and_index.py` - Python script for adding new episodes

**Content Structure:**
- Episodes are embedded directly in `index.html` as `<article>` elements
- Each episode includes structured data (schema.org markup)
- Audio files follow naming convention: `YTF-[BandName]-[Date]-[Venue].mp3`
- Episode images follow pattern: `[band-name].jpg`

## Development Commands

**Local Development:**
```bash
# Serve locally (Python 3)
python -m http.server 8000

# Serve locally (Python 2)  
python -m SimpleHTTPServer 8000

# View at http://localhost:8000
```

**Content Updates:**
```bash
# Add new episode using Python script
python update_feed_and_index.py

# Validate RSS feed
curl https://orlandotapes.com/feed.xml | xmllint --format -

# Test HTML validation
curl -s https://validator.w3.org/nu/?doc=https://orlandotapes.com

# Check SEO elements
curl -s https://orlandotapes.com | grep -E "(title|description|og:)"
```

**Git Workflow:**
```bash
# Standard workflow - GitHub Pages auto-deploys from main branch
git add .
git commit -m "Add new episode: [Band Name]"
git push origin main
```

## SEO & Podcast Distribution

**SEO Implementation:**
- Comprehensive meta tags with Orlando-specific keywords
- Open Graph and Twitter Card optimization
- JSON-LD structured data for podcasts and local business
- Local SEO targeting Orlando music venues and scene

**RSS Feed Features:**
- iTunes-compatible podcast feed at `/feed.xml`
- Podcast Index namespace support
- Episode-level structured data
- Proper enclosure tags for audio files

**Missing Images** (see `IMAGES-NEEDED.md`):
- `orlando-tapes-cover.jpg` (1400x1400) - Main podcast artwork
- `orlando-tapes-og-image.jpg` (1200x630) - Social media sharing
- `orlando-tapes-twitter-card.jpg` (1200x675) - Twitter sharing
- `favicon.ico` (32x32) - Website icon

## Content Management

**Adding New Episodes:**
1. Upload audio file to Archive.org (see `ARCHIVE-ORG-HOSTING.md`)
2. Add band image to `/images/` directory  
3. Update `update_feed_and_index.py` with Archive.org URL and episode data
4. Run script to update both `feed.xml` and `index.html`
5. Update `sitemap.xml` with new episode URL
6. Commit and push changes

**Episode Data Structure:**
```python
episode_data = {
    "title": "Series Name - Band Live at Venue",
    "audio_url": "https://archive.org/download/orlando-tapes-episode-XX/filename.mp3",
    "description": "Live performance description with venue and date",
    "pub_date": "Day, DD Mon YYYY HH:MM:SS GMT",
    "duration": "HH:MM:SS",
    "image_url": "Band image URL",
    "learnmore_url": "Band's website/Bandcamp/social media",
    "archive_identifier": "orlando-tapes-episode-XX"  # For tracking Archive.org uploads
}
```

## Content Focus

**Primary Series:** "Youth To The Front" - Live recordings from Will's Pub
**Featured Venues:** Will's Pub (Mills 50), Stardust Coffee & Video (near Winter Park)
**Music Genres:** Punk, indie rock, experimental, underground Orlando bands
**Local SEO:** Heavily optimized for Orlando music scene searches

## File Conventions

**Audio Files:** `YTF-[BandName]-[MM.DD.YY]-[venue].mp3`
**Images:** `[band-name-lowercase].jpg`
**Episodes:** Numbered sequentially, embedded in single HTML page
**URLs:** Fragment-based navigation (`#episode-[number]-[band-name]`)

## Technical Notes

**GitHub Pages Deployment:** 
- Auto-deploys from `main` branch
- Custom domain configured via `CNAME` file
- SSL/HTTPS automatically provided

**Audio Hosting:**
- Audio files hosted on Archive.org to overcome GitHub's 50MB limit
- Permanent URLs with Archive.org's CDN delivery
- See `ARCHIVE-ORG-HOSTING.md` for upload and management guide
- Local copies kept as backup only

**SEO Monitoring:**
- Google Search Console recommended for tracking
- Submit sitemap: `https://orlandotapes.com/sitemap.xml`
- Monitor Orlando + music keyword rankings