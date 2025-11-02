import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

# Register namespaces to preserve prefixes
ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
ET.register_namespace('podcast', 'https://podcastindex.org/namespace/1.0')
ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')
ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')

def add_episode_to_feed(feed_path, index_path, episode_data):
    """
    Add a new episode to both feed.xml and index.html.
    Also updates the podcast's main cover image to match the latest episode.
    """
    # Read the original feed content to preserve formatting
    with open(feed_path, 'r', encoding='utf-8') as f:
        feed_content = f.read()
    
    # Update the podcast's main image using regex (to preserve XML formatting)
    # Find the <itunes:image href="..." /> line and update it
    image_pattern = r'<itunes:image href="[^"]+"'
    new_image = f'<itunes:image href="{episode_data["image_url"]}"'
    feed_content = re.sub(image_pattern, new_image, feed_content, count=1)
    
    # Parse the feed to add the new episode
    tree = ET.parse(feed_path)
    root = tree.getroot()
    channel = root.find("channel")

    # Instead of using ElementTree, manually insert the formatted XML
    # to preserve proper formatting and match existing episodes
    new_item_xml = f"""<item><title>{episode_data["title"]}</title><link>{episode_data["audio_url"]}</link><description>{episode_data["description"]}</description><pubDate>{episode_data["pub_date"]}</pubDate><enclosure url="{episode_data["audio_url"]}" length="{episode_data["audio_length"]}" type="audio/mpeg" /><guid isPermaLink="true">{episode_data["audio_url"]}</guid><itunes:image href="{episode_data["image_url"]}" /><itunes:author>{episode_data["author"]}</itunes:author><itunes:summary>{episode_data["summary"]}</itunes:summary><itunes:duration>{episode_data["duration"]}</itunes:duration><podcast:episodeType>full</podcast:episodeType><podcast:explicit>no</podcast:explicit><podcast:season>{episode_data["season"]}</podcast:season><podcast:episode>{episode_data["episode"]}</podcast:episode></item>"""
    
    # Find where to insert the new item (after the <podcast:explicit>false</podcast:explicit> line)
    insert_marker = '<podcast:explicit>false</podcast:explicit>'
    
    if insert_marker in feed_content:
        # Insert the new episode right after the channel metadata
        feed_content = feed_content.replace(
            insert_marker,
            insert_marker + '\n    ' + new_item_xml,
            1  # Only replace the first occurrence
        )
    else:
        # Fallback: insert before first <item> tag
        feed_content = feed_content.replace('<item>', new_item_xml + '<item>', 1)
    
    # Write the updated feed
    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(feed_content)

    # Update the index.html file
    with open(index_path, "r") as file:
        html_content = file.read()

    # Format episode number with leading zero
    episode_num = f"{episode_data['episode']:02d}"
    
    # Insert the new episode into the HTML at the top of the episodes list
    new_episode_html = f"""
      <!-- Episode {episode_data['episode']}: {episode_data['title']} -->
      <article>
        <h3>{episode_num} {episode_data["title"]}</h3>
        <img src="{episode_data["image_url"]}" alt="{episode_data["title"]}">
        <p>{episode_data["description"]}</p>
        <p><a href="{episode_data["learnmore_url"]}">Learn More</a></p>
        <audio controls>
          <source src="{episode_data["audio_url"]}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        <p><strong>Duration:</strong> {episode_data["duration"]}</p>
      </article>

"""
    # Insert after "Latest Podcast Episodes" header instead of at the bottom
    header_marker = "<h2>Latest Podcast Episodes</h2>"
    if header_marker in html_content:
        updated_html_content = html_content.replace(
            header_marker,
            header_marker + "\n" + new_episode_html
        )
    else:
        # Fallback to old method if header not found
        updated_html_content = html_content.replace(
            "<!-- Add more episodes here -->",
            new_episode_html + "      <!-- Add more episodes here -->"
        )

    # Write the updated HTML back to file
    with open(index_path, "w") as file:
        file.write(updated_html_content)

# Example usage
# This is where would add the new episode data
# NOTE: Upload audio file to Archive.org first, then use the Archive.org URL
episode_data = {
    "title": "Tiger Beat Live at Uncle Lou's",
    "audio_url": "https://archive.org/download/tiger-beat-uncle-lous-9.12.25/tiger-beat-uncle-lous-9.12.25.mp3",
    "description": "A fuzzed out freak out at the most important incubator of the underground music the world famous Uncle Lou's on Mills Ave in Orlando FL.",
    "pub_date": "Fri, 12 Sep 2025 00:00:00 GMT",
    "audio_length": "31457280",  # 30.0 MB
    "image_url": "https://github.com/godlessamerica/orlandotapes.github.io/blob/main/images/tiger-beat.jpg?raw=true",
    "author": "Orlando Tapes",
    "summary": "A fuzzed out freak out at the most important incubator of the underground music the world famous Uncle Lou's on Mills Ave in Orlando FL.",
    "duration": "22:21",
    "season": 1,
    "episode": 9,
    "learnmore_url": "https://radioinformationservices.bandcamp.com/album/art-imitates-art",
    "archive_identifier": "tiger-beat-uncle-lous-9.12.25"  # Archive.org identifier for tracking
}

feed_path = "/home/cloudcassette/Projects/orlandotapes.github.io/feed.xml"
index_path = "/home/cloudcassette/Projects/orlandotapes.github.io/index.html"

add_episode_to_feed(feed_path, index_path, episode_data)