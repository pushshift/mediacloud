import unittest
import os

from mediawords.util.topic_modeling.token_pool import TokenPool
from mediawords.util.topic_modeling.model_gensim import ModelGensim
from mediawords.util.paths import mc_root_path
from typing import Dict, List


class TestModelGensim(unittest.TestCase):
    """
    Test the methods in ..model_gensim.py
    """

    _SAMPLE_STORIES \
        = os.path.join(mc_root_path(),
                       "mediacloud/mediawords/util/topic_modeling/sample_stories.txt")

    def setUp(self):
        """
        Prepare the token pool
        """
        self.LIMIT = 5
        self.OFFSET = 1
        sample_file = open(self._SAMPLE_STORIES)
        token_pool = TokenPool(sample_file)
        self._story_tokens = token_pool.output_tokens(limit=self.LIMIT, offset=self.OFFSET)
        sample_file.close()
        self._flat_story_tokens = self._flatten_story_tokens()
        self._lda_model = ModelGensim()
        self._lda_model.add_stories(self._story_tokens)
        self._topics = self._lda_model.summarize_topic()

    def _flatten_story_tokens(self) -> Dict[int, List[str]]:
        """
        Flatten all tokens of a story into a single dimension list
        :return: A dictionary of {story_id : [all tokens of that story]}
        """
        flat_story_tokens = {}
        for story in self._story_tokens.items():
            story_id = story[0]
            grouped_tokens = story[1]
            flat_story_tokens[story_id] \
                = [tokens for sentence_tokens in grouped_tokens for tokens in sentence_tokens]
        return flat_story_tokens

    def test_one_to_one_relationship(self):
        """
        Test if there is one-to-one relationship for articles and topics
        (i.e. no mysteries topic id or missing article id)
        """
        topic_ids = self._topics.keys()
        story_ids = self._story_tokens.keys()

        for topic_id in topic_ids:
            unittest.TestCase.assertTrue(
                self=self,
                expr=(topic_id in story_ids),
                msg="Mysteries topic id: {}".format(topic_id))

        for article_id in story_ids:
            unittest.TestCase.assertTrue(
                self=self,
                expr=(article_id in topic_ids),
                msg="Missing article id: {}".format(article_id))

    def test_story_contains_topic_word(self):
        """
        Test if each story contains at least one of the topic words
        """

        story_ids = self._story_tokens.keys()

        for story_id in story_ids:
            exist = False
            for topic in self._topics.get(story_id):
                for word in topic:
                    exist = word in self._flat_story_tokens.get(story_id)
                    if exist:
                        break
                if not exist:
                    raise ValueError("Story {id} does not contain any of its topic words: {topic}"
                                     .format(id=story_id, topic=self._topics.get(story_id)))

    def test_default_topic_params(self):
        default_topic_num = 1
        default_word_num = 4
        for topics in self._topics.values():
            unittest.TestCase.assertEqual(
                self=self, first=default_topic_num, second=len(topics),
                msg="topics = {}".format(topics))
            for topic in topics:
                unittest.TestCase.assertEqual(
                    self=self, first=default_word_num, second=len(topic),
                    msg="topic = {}".format(topic))


if __name__ == '__main__':
    unittest.main()