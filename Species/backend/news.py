import requests
def fetch_latest_articles():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=17a4e63f2d5b480cad93d0fcbfdcc415"
    

    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print(f"Error fetching articles: {response.status_code} - {response.text}")
        return []