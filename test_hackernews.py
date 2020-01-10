import unittest
from unittest import mock
import json
import hackernews


class HackerNewsE2ETest(unittest.TestCase):
    @mock.patch("requests.get")
    def test_scrape_posts(self, mock_get):
        """
        This test verifies that the correct number of posts and the json payload are accurate.
        """
        with open("test_data/hackernews.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()

            actual_posts = hackernews.scrape_posts(30)
            self.assertEqual(
                len(json.loads(actual_posts)), 30
            )  # verify that the number of posts retrieved is accurate

            actual_posts = hackernews.scrape_posts(2)
            expected_posts = [
                {
                    "title": "Why are not some things darker when wet?",
                    "uri": "https://aryankashyap.com/why-are-some-things-darker-when-wet",
                    "author": "aryankashyap",
                    "points": 63,
                    "comments": 5,
                    "rank": 1,
                },
                {
                    "title": "Broot – A new way to see and navigate directory trees",
                    "uri": "https://dystroy.org/broot/",
                    "author": "gilad",
                    "points": 631,
                    "comments": 158,
                    "rank": 2,
                },
            ]
            self.assertEqual(json.loads(actual_posts), expected_posts)

    @mock.patch("requests.get")
    def test_skip_invalid_post(self, mock_get):
        """
        If the url/author/rank/points/comment of a post are not valid, the post should not be included in the result.
        This test verifies this.
        See test_data/hackernews_bad_comment.html
        """
        expected_posts = [
            {
                "title": "Broot – A new way to see and navigate directory trees",
                "uri": "https://dystroy.org/broot/",
                "author": "gilad",
                "points": 631,
                "comments": 158,
                "rank": 2,
            },
            {
                "author": "hellofunk",
                "comments": 0,
                "points": 8,
                "rank": 3,
                "title": "A simple C++11 Thread Pool implementation",
                "uri": "https://github.com/progschj/ThreadPool",
            },
        ]
        with open("test_data/hackernews_bad_url.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertEqual(json.loads(actual_posts), expected_posts)

        with open("test_data/hackernews_bad_comment.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertEqual(json.loads(actual_posts), expected_posts)

        with open("test_data/hackernews_bad_author.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertEqual(json.loads(actual_posts), expected_posts)

        with open("test_data/hackernews_bad_rank.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertEqual(json.loads(actual_posts), expected_posts)

        with open("test_data/hackernews_bad_points.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertEqual(json.loads(actual_posts), expected_posts)

        # if all posts are valid as in test_data/hackernews.html then no post should be skipped
        with open("test_data/hackernews.html") as test_data:
            mock_get.return_value = mock.Mock(ok=True)
            mock_get.return_value.text = test_data.read()
            actual_posts = hackernews.scrape_posts(2)
            self.assertNotEqual(json.loads(actual_posts), expected_posts)
            expected_posts = [
                {
                    "title": "Why are not some things darker when wet?",
                    "uri": "https://aryankashyap.com/why-are-some-things-darker-when-wet",
                    "author": "aryankashyap",
                    "points": 63,
                    "comments": 5,
                    "rank": 1,
                },
                {
                    "title": "Broot – A new way to see and navigate directory trees",
                    "uri": "https://dystroy.org/broot/",
                    "author": "gilad",
                    "points": 631,
                    "comments": 158,
                    "rank": 2,
                },
            ]
        self.assertEqual(json.loads(actual_posts), expected_posts)


if __name__ == "__main__":
    unittest.main()
