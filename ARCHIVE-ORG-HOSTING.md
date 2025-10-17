# Archive.org Hosting Guide for Orlando Tapes

This guide explains how to host audio files on Archive.org instead of directly in the GitHub repository to overcome the 50MB file size limit.

## Why Archive.org?

- **No file size limits** for audio content
- **Permanent URLs** that won't change
- **Built for preservation** of cultural content like live music
- **Free hosting** for non-commercial content
- **CDN delivery** for fast global access
- **Metadata support** for proper cataloging

## Setting Up Archive.org Account

1. Create an account at https://archive.org/account/login.createaccount.php
2. Verify your email address
3. Complete your profile with Orlando Tapes information

## Uploading Audio Files

### Method 1: Web Interface (Recommended for individual files)

1. Go to https://archive.org/create/
2. Choose "Software & Applications" or "Community Audio" collection
3. Fill out metadata:
   - **Title**: "Orlando Tapes - [Episode Title]"
   - **Description**: Include venue, date, band info, series info
   - **Subject Tags**: "orlando music", "live music", "florida", "punk", "indie", "[venue-name]", "[band-name]"
   - **Creator**: "Orlando Tapes"
   - **Date**: Performance date
   - **Language**: English
   - **Collection**: Consider creating a custom "Orlando Tapes" collection

4. Upload your MP3 file
5. Set to "Public Domain" or appropriate Creative Commons license
6. Submit and wait for processing

### Method 2: Command Line (For bulk uploads)

Install Internet Archive CLI:
```bash
pip install internetarchive
ia configure  # Enter your credentials
```

Upload files:
```bash
ia upload orlando-tapes-episode-01 YTF-Dogsmiles-4.19.25-wills-pub.mp3 \
  --metadata="title:Orlando Tapes - Youth To The Front - Dogsmiles Live at Will's Pub" \
  --metadata="description:Live performance by Dogsmiles at Will's Pub, Orlando, FL on April 19, 2025" \
  --metadata="subject:orlando music;live music;florida;punk;wills pub;dogsmiles" \
  --metadata="creator:Orlando Tapes" \
  --metadata="date:2025-04-19"
```

## Getting Archive.org URLs

After upload, your files will have URLs in this format:
```
https://archive.org/download/[identifier]/[filename]
```

Example:
```
https://archive.org/download/orlando-tapes-episode-01/YTF-Dogsmiles-4.19.25-wills-pub.mp3
```

## URL Naming Convention

Use consistent identifiers:
- **Pattern**: `orlando-tapes-episode-[number]` or `orlando-tapes-[band-name]-[date]`
- **Examples**: 
  - `orlando-tapes-episode-01`
  - `orlando-tapes-dogsmiles-04-19-25`
  - `orlando-tapes-ytf-catnap-04-19-25`

## Integration with Orlando Tapes

### Episode Data Structure (Updated)

```python
episode_data = {
    "title": "Youth To The Front - Dogsmiles Live at Will's Pub",
    "audio_url": "https://archive.org/download/orlando-tapes-episode-01/YTF-Dogsmiles-4.19.25-wills-pub.mp3",
    "description": "Live performance by Dogsmiles at Will's Pub, Orlando, FL on April 19, 2025.",
    "pub_date": "Mon, 21 Apr 2025 00:00:00 GMT",
    "duration": "00:18:10",
    "image_url": "https://github.com/godlessamerica/orlandotapes.github.io/blob/main/images/dogsmiles.jpg?raw=true",
    "learnmore_url": "https://dogsmiles.bandcamp.com/album/demo",
    "archive_identifier": "orlando-tapes-episode-01"  # New field for tracking
}
```

## Migration Steps

1. **Upload existing MP3s** to Archive.org with proper metadata
2. **Update feed.xml** with new Archive.org URLs
3. **Update index.html** audio sources
4. **Update update_feed_and_index.py** script
5. **Remove MP3s from Git repository**
6. **Update WARP.md** documentation

## Archive.org Best Practices

### Metadata Standards
- Use consistent naming for all uploads
- Include comprehensive descriptions
- Add relevant subject tags
- Set appropriate date fields
- Use consistent creator field "Orlando Tapes"

### Collection Organization
- Consider creating a dedicated "Orlando Tapes" collection
- Group episodes by series (Youth To The Front, etc.)
- Include venue information in descriptions
- Tag with band names for discoverability

### URL Management
- Keep a spreadsheet mapping episodes to Archive.org URLs
- Use descriptive identifiers that won't need to change
- Test URLs before updating feed.xml

## Backup Strategy

Archive.org serves as both hosting and backup, but consider:
- Keep local copies of all recordings
- Document Archive.org identifiers in a spreadsheet
- Regular verification that all URLs are accessible

## Legal Considerations

- Ensure you have permission to distribute the recordings
- Consider Creative Commons licensing for clarity
- Include performance date and venue information
- Credit bands appropriately in metadata

## Benefits of This Approach

1. **Unlimited file sizes** - No more 50MB GitHub limit
2. **Permanent preservation** - Archive.org's mission is long-term preservation
3. **Better metadata** - Rich description fields for discoverability
4. **Professional URLs** - Clean, permanent links for RSS feeds
5. **Bandwidth savings** - Archive.org handles the heavy lifting
6. **Discoverability** - Archive.org's search helps people find Orlando music

## Next Steps

1. Create Archive.org account
2. Upload a test episode to learn the process
3. Update one episode in the feed as a proof of concept
4. Gradually migrate all existing episodes
5. Update documentation and scripts for future episodes