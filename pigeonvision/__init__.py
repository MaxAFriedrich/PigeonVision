import logging
import logging.config
import time

from pigeonvision import persistent, heuristics, validate, redirects
from pigeonvision.validate import QueryType

persistent.load()


def certainty_to_estimate_word(certainty: float, query_type: QueryType) -> str:
    if certainty == 1.0:
        return f"We are certain that the {query_type.value} is malicious."
    elif 0.87 <= certainty < 1.0:
        return (f"We are almost certain that the {query_type.value} is "
                f"malicious.")
    elif 0.60 <= certainty < 0.87:
        return (f"We think the {query_type.value} is probably "
                f"malicious.")
    elif 0.40 <= certainty < 0.60:
        return (
            f"We think chances are about even as to whet"
            f"her the {query_type.value} is "
            "malicious or not.")
    elif 0.20 <= certainty < 0.40:
        return (
            f"We think there is a realistic, but low possibility that the "
            f"{query_type.value} is "
            "malicious.")
    elif 0.01 <= certainty < 0.20:
        return (f"We think it is unlikely that the {query_type.value} is "
                f"malicious.")
    elif 0 <= certainty < 0.01:
        return f"We are certain that the {query_type.value} is not malicious."
    else:
        raise ValueError(f"Unknown certainty value: {certainty}")


def log_query(func):
    def wrapper(query: str, *args, **kwargs):
        query_time = int(time.time())
        result = func(query, *args, **kwargs)
        try:
            # certainty is the third return value from main
            certainty = result[2] if len(result) > 2 else 0.0
            with open(persistent.LOCAL_APP_DATA / 'queries', 'a') as f:
                f.writelines(f"{query_time} {certainty:.2f}: {query}\n")
        except Exception as e:
            logging.error("Failed to log query: %s", e)
        return result

    return wrapper


@log_query
def main(query: str, verbose: bool = False, level: str = "DEBUG") -> (
        str, str, float):
    message = ""

    logger = logging.getLogger(__name__)
    log_level = getattr(logging, level.upper())

    logging.basicConfig(encoding='utf-8',
                        level=log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %('
                               'message)s')

    if not verbose: logging.basicConfig(filename=persistent.LOCAL_APP_DATA)

    logger.debug("Starting pigeon vision")

    query_type, validation_outcome, normalised_query = validate.validate_query(
        query)

    logger.info("QueryType: %s Validation outcome: %s Normalised query: %s",
                query_type, validation_outcome, normalised_query)

    if validation_outcome == validate.ValidationOutcome.INVALID:
        return "This is not a valid query.", "INVALID", 0.5
    elif validation_outcome == validate.ValidationOutcome.WHITELIST:
        return ("This domain is certainly not malicious.",
                "The item you queried is whitelisted and therefore we do not "
                "think it is malicious.", 0.0)
    elif validation_outcome != validate.ValidationOutcome.UNCERTAIN:
        raise ValueError("Unknown validation outcome.")

    if query_type == validate.QueryType.UNKNOWN:
        return (
            "This query is in an unknown format.",
            "Valid formarts are: "
            "IP address, domain name, email address, URL, MD5, SHA256, "
            "or SHA1 hash.",
            0.5)

    if query_type == QueryType.URL or query_type == QueryType.DOMAIN:
        redirect_count = 0
        final_url = []
        status_code = 200
        try:
            final_url, redirect_count, status_code = redirects.follow_redirects(
                query)
            logging.debug("Redirect results: %s %s %s", final_url,
                          redirect_count, status_code)
        except Exception as e:
            logging.error("Redirects for %s failed", query)

        if redirect_count > 0:
            logging.info("Redirects followed, renormalising final URL %s",
                         final_url)
            final_url_list = []

            for url in final_url:
                final_url_list.append(validate.normalise.url(url))
            [normalised_query].extend(final_url_list)
            logging.debug("Normalised query now %s", normalised_query)
            message += (
                f"We followed {redirect_count} redirects and ended up at "
                f"<b>{final_url}<b> with status code "
                f"{status_code}.<br>")

    logging.debug("Running heuristics on %s")
    certainty, heuristics_message = heuristics.run(normalised_query, query_type)
    logging.info("Heuristics certainty: %f Message: %s", certainty,
                 heuristics_message)
    certainty_word = certainty_to_estimate_word(certainty, query_type)
    message = ((f"<h1>We think that there is a {certainty * 100:.2f}% chance "
                f"that the item is malicious because:</h1>") + message +
               heuristics_message)
    logging.debug("Execution complete")
    return certainty_word, message, certainty
