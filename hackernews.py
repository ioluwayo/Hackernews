import json, logging, sys, argparse, requests
from bs4 import BeautifulSoup
from rfc3986 import validators, uri_reference
from rfc3986.exceptions import ValidationError as UriValidationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))
URI_VALIDATOR = (
    validators.Validator()
    .require_presence_of("scheme", "host")
    .check_validity_of(
        "scheme", "userinfo", "host", "port", "path", "query", "fragment"
    )
)
BASE_URL = "https://news.ycombinator.com/"


def is_valid_uri(uri):
    try:
        URI_VALIDATOR.validate(uri_reference(uri))
        return True
    except UriValidationError as exc:
        LOGGER.debug(exc)
        return False


def is_valid_string(string):
    if not string or len(string) > 256:
        return False
    return True


def retrieve_title(storylink_tag):
    title = storylink_tag.text
    if is_valid_string(title):
        return title
    LOGGER.debug("title is invalid")


def retrieve_uri(storylink_tag):
    uri = storylink_tag["href"]
    if is_valid_uri(uri):
        return uri
    LOGGER.debug("uri is invalid")


def retrieve_rank(rank_tag):
    rank = rank_tag.text
    rank = rank.rstrip(".")
    if rank.isdigit():
        rank = int(rank)
        if rank >= 0:
            return rank
        else:
            LOGGER.debug("rank is less than 0..")
    else:
        LOGGER.debug("rank is not a number")


def retrieve_author(author_tag):
    author = author_tag.text
    if is_valid_string(author):
        return author
    LOGGER.debug("author is Invalid")


def retrieve_points(points_tag):
    points = points_tag.text
    points = points.split()[0]
    if points.isdigit():
        points = int(points)
        if points >= 0:
            return points
        else:
            LOGGER.debug("points is less than 0")
    else:
        LOGGER.debug("points is not a number")


def retrieve_comments(comments_tag):
    comments = comments_tag.text
    comments = comments.split()[0]
    if comments.isdigit():
        comments = int(comments)
        if comments >= 0:
            return comments
        else:
            LOGGER.debug("comments is less than 0")
    elif (
        comments == "discuss"
    ):  # when there are no comments on a post, this value is "discuss"
        comments = 0  # no comments implies 0
        return comments
    else:
        LOGGER.debug("comments is not a number")


def retrieve_valid_posts(post_tags, max_posts):
    valid_posts = []
    count = 0
    for post_tag in post_tags:
        LOGGER.debug(f"Processing post ID: {post_tag['id']}")
        storylink_tag = post_tag.find("a", {"class": "storylink"})

        if not storylink_tag:
            LOGGER.debug("Skipping post. Unable to find storylink tag")
            continue
        title = retrieve_title(storylink_tag)
        if title is None:
            LOGGER.debug("Skipping post")
            continue
        uri = retrieve_uri(storylink_tag)
        if uri is None:
            LOGGER.debug("Skipping post")
            continue

        rank_tag = post_tag.find("span", {"class": "rank"})
        if not rank_tag:
            LOGGER.debug("Skipping post. Unable to find rank tag")
            continue

        rank = retrieve_rank(rank_tag)
        if rank is None:
            LOGGER.debug("Skipping post")
            continue

        # only proceed to find subtext/sibling when prior validations are successful. avoid unnecessary work
        subtext_tag = post_tag.next_sibling.find("td", {"class": "subtext"})
        if not subtext_tag:
            LOGGER.debug("Skipping post. Unable to find subtext_tag")
            continue

        author_tag = subtext_tag.find("a", {"class": "hnuser"})
        if not author_tag:
            LOGGER.debug("Skipping post. Unable to find author tag")
            continue

        author = retrieve_author(author_tag)
        if author is None:
            LOGGER.debug("Skipping post")
            continue

        points_tag = subtext_tag.find("span", {"class": "score"})
        if not points_tag:
            LOGGER.debug("Skipping post. Unable to find points tag")
            continue
        points = retrieve_points(points_tag)
        if points is None:
            LOGGER.debug("Skipping post")
            continue

        comments_tag = subtext_tag.find_all("a", recursive=False)[
            2
        ]  # find_all maintains order
        if not comments_tag:
            LOGGER.debug("Skipping post. Unable to find comment tag")
            continue

        comments = retrieve_comments(comments_tag)
        if comments is None:
            LOGGER.debug("Skipping post")
            continue

        # all data is valid. create post dict and append to list
        valid_posts.append(
            {
                "title": title,
                "uri": uri,
                "author": author,
                "points": points,
                "comments": comments,
                "rank": rank,
            }
        )
        count += 1

        if count == max_posts:  # stop retrieving posts to avoid unnecessary work
            break
    return valid_posts


def scrape_posts(n):
    posts = []
    url = BASE_URL
    page = 1
    while len(posts) < n:
        required = n - len(posts)
        LOGGER.debug(f"scraping {url} for {required} posts")
        try:
            response = requests.get(url)
            athings = BeautifulSoup(response.text, "html.parser").find_all(
                "tr", {"class": "athing"},
            )
            LOGGER.debug(athings)
            posts.extend(retrieve_valid_posts(athings, required))
            page += 1
            url = BASE_URL + "news?p=" + str(page)
        except requests.exceptions.RequestException as exc:
            LOGGER.error(exc)
            LOGGER.error("Exiting")
            sys.exit(1)
    return json.dumps(posts, indent=2)


def main():
    def validate_post_input(val):
        try:
            val = int(val)  # if not integer, will raise
            if val < 0 or val > 100:
                raise argparse.ArgumentTypeError(f"{val} is not in the range 0-100")
        except ValueError:
            raise argparse.ArgumentTypeError(f"invalid int value: '{val}'")
        return val

    parser = argparse.ArgumentParser(
        description="This script scrapes https://news.ycombinator.com/ and prints to stdout the top posts. "
        "The output is in json format. "
        "Sample usage: hackernews --posts 10"
    )
    parser.add_argument(
        "--posts",
        type=validate_post_input,
        metavar="n",
        required=True,
        help="The number of posts to display. Value must be in the range 0-100",
    )
    parser.add_argument(
        "-v", "--verbose", help="sets logging level to debug", action="store_true"
    )
    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    posts = scrape_posts(args.posts)
    print(posts)


if __name__ == "__main__":
    main()
