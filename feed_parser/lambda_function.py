import feedparser

def get_last_entry(feed_url):
    feed = feedparser.parse(feed_url)
    entries = feed.entries
    sorted_entries = sorted(
        entries, key=lambda entry: entry['readingdatetime'])
    sorted_entries.reverse()

    return sorted_entries[0]


def get_all_entries(feed_url):
    feed = feedparser.parse(feed_url)
    entries = feed.entries

    sorted_entries = sorted(
        entries, key=lambda entry: entry['readingdatetime'])

    colors_map = {
        'Good': '#008000',
        'Moderate': '#FFCC00',
        'Unhealthy for Sensitive Groups': '#FF6600',
        'Unhealthy': '#ff0000',
        'Very Unhealthy': '#FF00CC',
        'Hazardous': '#800000'
    }

    values = map(lambda e: int(e['aqi']), sorted_entries)
    time_points = map(lambda e: e['readingdatetime'][-8:-3], sorted_entries)
    desc = map(lambda e: colors_map[e['desc']], sorted_entries)
    data = {'y': values, 'x': time_points, 'color': desc}
    return data
    
def handler(event, context):
    feed_url = "http://dosairnowdata.org/dos/RSS/Sarajevo/Sarajevo-PM2.5.xml"

    latest_entry = get_last_entry(feed_url)
    data = get_all_entries(feed_url)
    
    return { 
        'last': latest_entry,
        'all': data
    }  
