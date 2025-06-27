from flask import Flask, render_template, jsonify, request
import requests
#requests for api requests

app = Flask(__name__)


NEWS_API_KEY = "c2c8127d75274a5b8b5af80e4be1a9ec"
NEWS_BASE_URL = "https://newsapi.org/v2/top-headlines"
PIXABAY_API_KEY = "49225244-4c2c651867908e3eb46a522c5"
PIXABAY_BASE_URL = "https://pixabay.com/api/"
PAGE_SIZE = 20  
MAX_ARTICLES = 50  
#fetching news
def fetch_news(query="India", category=None, total_articles=MAX_ARTICLES):
    """Fetches news articles and returns JSON."""
    articles = []
    page = 1  
    total_fetched = 0


    while total_fetched < total_articles:
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": PAGE_SIZE,
            "page": page
        }


        if category:
            params["category"] = category


        try:
            response = requests.get(NEWS_BASE_URL, params=params)
            response.raise_for_status()  
            news_data = response.json()
            current_articles = news_data.get("articles", [])


            if not current_articles:
                break


            for article in current_articles:
                image_url = fetch_image(query) or article.get("urlToImage")
                article["image"] = image_url
                articles.append(article)
           
            total_fetched += len(current_articles)
            page += 1


        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


    return articles[:total_articles]


def fetch_image(query):
    """Fetches an image from Pixabay API."""
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "per_page": 1
    }
    try:
        response = requests.get(PIXABAY_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["hits"]:
            return data["hits"][0]["webformatURL"]
    except requests.exceptions.RequestException:
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news", methods=["GET"])
def get_news():
    """API Endpoint to fetch news"""
    query = request.args.get("query", "India")  
    category = request.args.get("category", None)  
    articles = fetch_news(query=query, category=category)
    return jsonify(articles)


if __name__ == "__main__":
    with app.app_context():
        print("\n🔍 Registered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule} -> {rule.endpoint}")


    app.run(debug=True)


