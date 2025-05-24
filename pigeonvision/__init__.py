from pigeonvision import persistent, heuristics, validate, redirects
from pigeonvision.validate import QueryType

persistent.load()


def certainty_to_estimate_word(certainty: float) -> str:
    if certainty == 1.0:
        return "We are certain that the item is malicious."
    elif 0.87 <= certainty < 1.0:
        return "We are almost certain that the item is malicious."
    elif 0.60 <= certainty < 0.87:
        return "We think it is probable that the item is malicious."
    elif 0.40 <= certainty < 0.60:
        return ("We think chances are about even as to whether the item is "
                "malicious or not.")
    elif 0.20 <= certainty < 0.40:
        return ("We think there is a realistic possibility that the item is "
                "malicious.")
    elif 0.01 <= certainty < 0.20:
        return "We think it is unlikely that the item is malicious."
    elif certainty == 0.0:
        return "We are certain that the item is not malicious."
    else:
        raise ValueError(f"Unknown certainty value: {certainty}")


def main(query: str) -> (str, str):
    message = ""

    query_type, validation_outcome, normalised_query = validate.validate_query(
        query)

    if validation_outcome == validate.ValidationOutcome.INVALID:
        return "This is not a valid query.", "INVALID"
    elif validation_outcome == validate.ValidationOutcome.WHITELIST:
        return ("This domain is certainly not malicious.",
                "The item you queried is whitelisted and therefore we do not "
                "think it is malicious.")
    elif validation_outcome != validate.ValidationOutcome.UNCERTAIN:
        raise ValueError("Unknown validation outcome.")

    if query_type == validate.QueryType.UNKNOWN:
        return (
            "This query is in an unknown format.",
            "Valid formarts are: "
            "IP address, domain name, email address, URL, MD5 or SHA1 hash.")

    if query_type == QueryType.URL:
        redirect_count = 0
        final_url = ""
        status_code = 200
        try:
            final_url, redirect_count, status_code = redirects.follow_redirects(
                query)
        except Exception as e:
            message += (f"We could not follow redirects for this URL: "
                        f"{str(e)}<br>")
        if redirect_count > 0:
            message += (
                f"We followed {redirect_count} redirects and ended up at "
                f"<b>{final_url}<b> with status code "
                f"{status_code}.<br>")

    certainty, heuristics_message = heuristics.run(query, query_type)
    certainty_word = certainty_to_estimate_word(certainty)
    message = ((f"<h1>We think that there is a {certainty * 100:.2f}% chance "
                f"that the item is malicious because:</h1>") + message +
               heuristics_message)
    return certainty_word, message
