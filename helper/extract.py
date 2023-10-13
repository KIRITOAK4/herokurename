import re
from Krito import Text, Text1, Text2, Text3

def extract_message_id(link):
    message_id_match = re.search(r'https?://(www\.)?telegram\.me/(c/)?[^/]+/(\d+)', link)
    if message_id_match:
        return message_id_match.group(3)
    else:
        return None

# Extract message IDs from the Text variables
extracted_text = {
    'Text': extract_message_id(Text),
    'Text1': extract_message_id(Text1),
    'Text2': extract_message_id(Text2),
    'Text3': extract_message_id(Text3)
}

