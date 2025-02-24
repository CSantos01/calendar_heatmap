import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor

from pathlib import Path
this_dir = Path(__file__).resolve().parent
output_dir = this_dir / 'output/events'
output_dir.mkdir(parents=True, exist_ok=True)

def events_extracter(month, day):
    '''
    Return the total number of events for a given day of the Gregorian calendar
    and write a CSV file with the number of events, births, and deaths on a given day of the year.
    
    Parameters:
    month (str): Month of the Wikipedia page you want to fetch.
    day (int): Day of the Wikipedia page you want to fetch.

    Returns:
    int: Number of events on the given day.
    '''
    # URL of the Wikipedia page
    url = f"https://en.wikipedia.org/wiki/{month}_{day}"

    # Fetch the content of the page
    response = requests.get(url)
    if response.status_code == 200:
        print("Page fetched successfully")
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Function to extract events from a section
    def extract_events(section_title):
        section = soup.find(id=section_title)
        events = []
        
        index = 0
        if section:
            sub_sections = []
            for tag in section.find_all_next(['h2', 'h3']):
                if tag.name == 'h2':
                    break
                sub_sections.append(tag)
            if sub_sections:
                for sub_section in sub_sections: 
                    ul = sub_section.find_next('ul')
                    if ul:
                        for li in ul.find_all('li'):
                            events.append(li.text)
                    else:
                        print(f"No <ul> found after section: {section_title}")
            else:
                ul = section.find_next('ul')
                if ul:
                    for li in ul.find_all('li'):
                        events.append(li.text)
                else:
                    print(f"No <ul> found after section: {section_title}")
            
        else:
            print(f"Section not found: {section_title}")
        
        return events

    # Extracting events, births, and deaths
    with ThreadPoolExecutor() as executor:
        events_future = executor.submit(extract_events, 'Events')
        births_future = executor.submit(extract_events, 'Births')
        deaths_future = executor.submit(extract_events, 'Deaths')
        others_future = executor.submit(extract_events, 'Holidays_and_observances')

        events = events_future.result()
        births = births_future.result()
        deaths = deaths_future.result()
        others = others_future.result()

        
    # Writing the number of each type of event to a CSV file
    with open(output_dir / f'{month}_{day}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Count'])
        writer.writerow(['Total', len(events) + len(births) + len(deaths)])
        writer.writerow(['Events', len(events)])
        writer.writerow(['Births', len(births)])
        writer.writerow(['Deaths', len(deaths)])
        writer.writerow(['Others', len(others)])

    print(f"File saved to {output_dir / f'{month}_{day}.csv'}")
    return len(events)+len(births)+len(deaths)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--month', type=str, default="January", help='Month of the Wikipedia page you want to fetch')
    parser.add_argument('--day', type=int, default=1, help='Day of the Wikipedia page you want to fetch')
    args = parser.parse_args()

    month = args.month
    day = args.day
    events_extracter(month, day)

    