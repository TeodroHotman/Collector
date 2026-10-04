def check_source(websites, keywords, topics):
    try:
        results = search_source(websites, keywords, topics)
        return results
    except Exception as e:
        return {"valid": False, "problems": [str(e)]}