import json
import threading
import requests

covid_keywords = ["covid", "Covid", "covid-19", "Covid-19", "Coronavirus"]

economy_keywords = ["economy", "economic", "money", "monetary", "fiscal",
                    "price", "shortage", "stock", "inflation", "cost", "tax",
                    "growth", "currency", "industry", "revenue", "budget"]

dates = ["2020-05", "2020-10", "2020-16", "2020-24", "2020-29",
         "2020-34", "2020-40", "2020-45", "2020-50"]

months = ["Jan", "Feb", "March/April", "May/June", "July", "Aug", "Sept", "Oct", "Nov/Dec"]

websites = ["cnn.com", "economist.com", "nytimes.com", "abcnews.go.com",
            "usatoday.com", "washingtonpost.com", "forbes.com", "foxnews.com",
            "cbsnews.com", "chicagotribune.com", "yahoo.com/news", "nbcnews.com"]

checked_sites = 0
successful_matches = 0
matches = []

# Count no of occurences of words
def word_appearance(content, word_list):
    final_num = 0

    for word in word_list:
        final_num += content.count(word)
    return final_num


# Read content of valid site if already not visited and send to count the no of occurences of valid keywords
def check_covid_economy_link(site, month):
    if str(site.url) not in matches:
        global checked_sites
        global successful_matches
        checked_sites += 1
        content = str(site.content)
        key_words_num = word_appearance(content, covid_keywords)
        if key_words_num < 20:
            return

        secondary_words_num = word_appearance(content, economy_keywords)

        if secondary_words_num < 5:
            return

        successful_matches += 1
        print(str(successful_matches) + ": " + month + " -> " + site.url)
        matches.append(str(site.url))


# Loops over every website. Discards the link if it does not contain a mention of covid-19
def crawl_site(response, month):
    for site_json in response.content.splitlines():
        if successful_matches > 1000:
            return
        site_json = json.loads(site_json)
        if word_appearance(site_json["url"], covid_keywords) == 0:
            continue
        site = requests.get(site_json['url'])
        check_covid_economy_link(site, month)


# Creates a link for every time period and website combination
def start_crawl():
    threads = []
    for site in websites:
        for date, month in zip(dates, months):
            url = f'http://index.commoncrawl.org/CC-MAIN-{date}-index?url=https://{site}&matchType=domain&output=json'
            response = requests.get(url)
            if response.status_code != 200:
                continue
            thread = threading.Thread(target=crawl_site, args=(response, month,), daemon=True)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start_crawl()
    print("----------------Finished----------------")
