# SrappingTool
Application for scrapping data from an e-commerce website via API, below is the tech stack information.
<ul>
  <li><b>Backend</b> - FastAPI</li>
  <li><b>Caching</b> - Redis</li>
  <li><b>Database</b> - MongoDB</li>
</ul>

### Application structure
<ul>
  <li><b>app/auth.py</b> - Used for static token authentication</li>
  <li><b>app/caching.py</b> - Used for caching mechanism</li>
  <li><b>app/MongoConnection.py</b> - Consist of MongoCollection class returning mongoDb collection instance for DB Operation</li>
  <li><b>app/scapper.py</b> - Logic for scrapping from the URL</li>
  <li><b>app/database.py</b> - Handling local storage, on application load it fetched data from DB</li>
  <li><b>config.json</b> - Environment information related to DB credentials</li>
</ul>

### Libraries used
<ul>
  <li>bs4 - for scrapping</li>
  <li>fastapi - backend</li>
  <li>redis - for connecting redis</li>
  <li>pymongo - for connecting mongoDB</li>
  <li>requests - for scrapping data from target url</li>
</ul>

### How does the application work?
1. The server will be up and running, on load it will fetch existing data from DB and load into cache.
2. The user will send a POST request to the server on route <b>/scrape</b> with the target URL and number of pages to scrap
3. During the processing of the request, application will scrap the data and add new products to DB only if there is any update in price or new product added on site.
4. There are a fixed number of retries if the target page is not reachable, after which it will move to the next page.
