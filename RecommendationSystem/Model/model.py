import os
import sys
from typing import List

import torch
from sentence_transformers import SentenceTransformer
from torch import nn

from RecommendationSystem.API.RESTApi.abstract_model import AbstractModel
from RecommendationSystem.DB.db_models.article import Article
from RecommendationSystem.DB.utils import get_all_article, get_all_comments_for_given_article


class Model(AbstractModel):
    def __init__(self):
        self.model = SentenceTransformer("stsb-roberta-base-v2")

    def get_recommendations(self, comment_data: dict) -> List[str]:
        """
        Interface method for the REST API view
        :param comment_data: Dict with all information the model needs to extract the recommendations from the database
        :return: List of recommendations
        """
        if len(comment_data.keys()) == 0:
            return []

        # Add model here
        user_comment_embedding, keyword_embeddings = self.__compute_embeddings(
            user_comment=comment_data["user_comment"], keywords=comment_data["keywords"])

        article_candidates = self.__find_article_candidates(keyword_embeddings)

        candidate_comments = self.__find_comment_candidates(article_candidates)

        recommendations = self.__compute_scores(candidate_comments, user_comment_embedding)

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return [[comment[0], comment[2], comment[3], comment[4]] for comment in recommendations[:6]]

    def __find_article_candidates(self, keyword_embeddings):
        all_article = get_all_article()
        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        results = []
        for article in all_article:
            score = cos(torch.Tensor(article.embedding), torch.Tensor(keyword_embeddings))
            results.append([article, score])
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results[:5]]

    def __find_comment_candidates(self, articles: List[Article]):
        comments = []
        for article in articles:
            comments_for_article = get_all_comments_for_given_article(article)
            for comment in comments_for_article:
                comments.append({"comment": comment, "article": article})
        return comments

    def __compute_embeddings(self, user_comment, keywords):
        user_comment_embedding = self.model.encode([user_comment])[0]
        keywords_embeddings = self.model.encode([keywords])[0]
        return user_comment_embedding, keywords_embeddings

    def __compute_scores(self, candidate_comments, user_comment_embedding):
        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        comments_with_scores = []
        for comment_candidate in candidate_comments:
            score = cos(torch.Tensor(comment_candidate["comment"].embedding), torch.Tensor(user_comment_embedding))
            comments_with_scores.append([comment_candidate["comment"].text, score.item(),
                                         comment_candidate["article"].news_agency,
                                         comment_candidate["article"].article_title,
                                         comment_candidate["article"].url])
        return comments_with_scores