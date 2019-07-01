import json
import urllib.request
from slugify import slugify
from multiprocessing.dummy import Pool as ThreadPool
import parmap

from src.helper import (
    parse_arguments,
    create_output_folders,
    get_url,
    get_crawler,
)
from src.queries import get_queries
from src.crawler import Query, RankingItemEncoder, QueryEncoder


def crawl_query(query: Query, index, args, results_path, pictures_path):
    """
    Crawl a single query.
    :param query: query to be crawled.
    :param args: commandline arguments. Expects args.platform and args.webdriver
    :param results_path
    :param pictures_path
    :param index: the number of the query
    :return: query if the query failed or None if it did not.
    """
    print("query " + str(index))

    Crawler = get_crawler(args.platform)
    crawler = Crawler(query, args.webdriver)
    try:
        list_result = crawler.crawl()
        with open(
                results_path + "/" + slugify(query.city + "-" + query.title) + ".json",
                "w",
        ) as fout:
            json.dump(list_result, fout, cls=RankingItemEncoder)
        for result in list_result:
            urllib.request.urlretrieve(
                result.picture_url, pictures_path + "/" + result.id + ".jpg"
            )
    except Exception as e:
        print(e)
        crawler.exit()
        return query

    return None


def main():
    args = parse_arguments()

    if args.queriesfile is None:
        args.queriesfile = get_queries(args)

    with open(args.queriesfile) as f:
        entries = json.load(f)

    results_path, pictures_path, root_output_path = create_output_folders(args.output)

    list_query = [
        Query(get_url(args.platform, entry), entry["title"], entry["city"])
        for entry in entries
    ]

    indexes = [i for i in range(len(list_query))]
    results = parmap.starmap(
        crawl_query, zip(list_query, indexes), args, results_path, pictures_path, pm_processes=args.threads)

    failed = [query for query in results if query is not None]

    with open(root_output_path + "/failed_queries.json", "w") as f:
        json.dump(failed, f, cls=QueryEncoder)


if __name__ == "__main__":
    main()
