from src.trends.google import GoogleTrendsCrawler

google_crawler = GoogleTrendsCrawler()
data = google_crawler(date_string='20211019')
