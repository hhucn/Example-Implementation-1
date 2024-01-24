# Example Recommendation System 1 - Comment Centric Comment Recommendation

Here, we see an example implementation of the comment recommendation framework.

## Model

This model recommends comments not based on previous interests and behavior of the user, but on the comment,
he or she is currently interested in. It uses this comment and the keywords of the article the comment appeared under 
to compile a selection of comments.

With the keywords of the article, it searches for similar articles and takes all comments that appeared under these articles.
Afterwards, it sorts this set of comments by the semantic similarity to the comment the user is interested in. Finally, it
takes the top n most similar comments and presents them as the recommendation.

## Framework

The Comment Recommendation Framework is a modular approach to support scientists in the development of prototypes for
comment recommendation systems that can be used in real-world scenarios. The advantage of such a system is that it
relieves the scientist from the majority of the technical code and only prototype-specific components have to be developed. In this way, the researchers can invest
more time in the development of recommendation models and less time has to be spent in the development of a prototype 
while at the same time getting prototypes that can be used in real-world settings.

## Implementation Effort
To implement this example recommendation system. The following files have been edited:
* Embedder/embedding_model.py -> Here, we implemented the method to compute the vector embedding.
* Embedder/run_embedder.py -> Here, we determined for which properties the embeddings are computed.
* Model/model.py -> Here, we implemented the recommendation model.
* NewsAgencyScraper/NewsAgencyScraper/spiders/WashingtonTimesSpyder.py -> Here, we replaced the template class `NewsAgencySpyder` with the implementation for the WashingtonTimesSpyder.
* NewsAgencyScraper/NewsAgencyScraper/spiders/NewYorkTimesSpyder.py -> Here, we replaced the template class `NewsAgencySpyder` with the implementation for the NewYorkTimesSpyder.
* NewsAgencyScraper/run_scraper.py -> Here, we called the `WashingtonTimesSpyder` and 'NewYorkTimesSpyder'.
* UI -> Here, we installed the npm packages and built the chrome extension


## Setup
Ensure that the following tools are installed:
* Docker
* Docker-Compose
* Python >= 3.10

## Documentation

To build the latest version of the documentation, please run in the docs folder:

```
$ make clean && make html
```

Then you find the latest documentation [here](RecommendationSystem/docs/_build/html/index.html)

## Environment Variables
The framework need some environment variables to be set for running properly. Please ensure that you have an ```.env```
file with the following variables:
* NEO4J_PASSWORD
* NEO4J_BOLT_URL (Format: `bolt://neo4j:<NEO4J_PASSWORD>@neo4j:7687`)


### Run different moduls with docker-compose
We provide you with the following `docker-compose` files to run the different components of the recommendation framework. 

* `docker-compose.scraping.yml`: Runs the news agency scraper to retrieve articles and comments from various news agencies.
* `docker-compose.embed.yml`: Starts the embedding process to compute the embeddings for the comments and articles. Should be run directly after `docker-compose.scraping.yml`.
* `docker-compose.test.yml`: Runs the tests for the system.
* `docker-compose.api.yml`: Runs the comment-recommendation systems.

### User-Interface
If you would like to use the default user interface. You have to install the npm packages and build the chrome extension.
For this you have to run in the `UI` folder:

```bash
$ npm install
```

and afterwards:

```bash
$ npm run build
```

Then you can import the `build` folder in a chromium browser.

## Maintainers:
* Anonymous

## Contributors:
* Anonymous

## License:
Copyright(c) 2022 - today Anonymous

Distributed under the [MIT License](LICENSE)

