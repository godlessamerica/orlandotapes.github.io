import xml.etree.ElementTree as ET
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

    # Create a new <item> element for the episode with proper namespaces
    item = ET.Element("item")
    ET.SubElement(item, "title").text = episode_data["title"]
    ET.SubElement(item, "link").text = episode_data["audio_url"]
    ET.SubElement(item, "description").text = episode_data["description"]
    ET.SubElement(item, "pubDate").text = episode_data["pub_date"]
    ET.SubElement(item, "enclosure", {
        "url": episode_data["audio_url"],
        "length": episode_data["audio_length"],
        "type": "audio/mpeg"
    })
    ET.SubElement(item, "guid", {"isPermaLink": "true"}).text = episode_data["audio_url"]
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}image", {"href": episode_data["image_url"]})
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}author").text = episode_data["author"]
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}summary").text = episode_data["summary"]
    ET.SubElement(item, "{http://www.itunes.com/dtds/podcast-1.0.dtd}duration").text = episode_data["duration"]
    ET.SubElement(item, "{https://podcastindex.org/namespace/1.0}episodeType").text = "full"
    ET.SubElement(item, "{https://podcastindex.org/namespace/1.0}explicit").text = "no"
    ET.SubElement(item, "{https://podcastindex.org/namespace/1.0}season").text = str(episode_data["season"])
    ET.SubElement(item, "{https://podcastindex.org/namespace/1.0}episode").text = str(episode_data["episode"])

    # Insert the new item as the first episode (after channel metadata)
    # Find the first existing <item> and insert before it
    items = channel.findall("item")
    if items:
        item_index = list(channel).index(items[0])
        channel.insert(item_index, item)
    else:
        channel.append(item)

    # Write the updated feed.xml back to file with updated image
    tree.write(feed_path, encoding="utf-8", xml_declaration=True)
    
    # Now update the image in the written file using the regex-updated content
    with open(feed_path, 'r', encoding='utf-8') as f:
        written_content = f.read()
    
    # Apply the image update to the written content
    written_content = re.sub(image_pattern, new_image, written_content, count=1)
    
    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(written_content)

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