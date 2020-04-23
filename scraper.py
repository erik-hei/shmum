import requests
import json

def scrape_athleta(pid):
    url = 'https://api.bazaarvoice.com/data/batch.json?'
    query = (
        'passkey=7dtpedhgbgp2vn5p0ykid4opx&apiversion=5.5&'
        'displaycode=3755_22_0-en_us&'
        'resource.q0=products&'
        'filter.q0=id%3Aeq%3A' + str(pid) + '&'
        'stats.q0=reviews&'
        'filteredstats.q0=reviews&'
        'filter_reviews.q0=contentlocale%3Aeq%3Aen_US&'
        'filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_US&'
        'callback=BV._internal.dataHandler0'
    )
    res = requests.get(url + query)
    q0 = json.loads(res.text[26:-1])['BatchedResults']['q0']['Results'][0]
    num_reviews = q0['TotalReviewCount'] - q0['ReviewStatistics']['RatingsOnlyReviewCount']
    q1 = []
    for i in range(num_reviews // 100 + 1):
        limit = 100
        offset = 100 * i
        query = (
            'passkey=7dtpedhgbgp2vn5p0ykid4opx&apiversion=5.5&'
            'displaycode=3755_22_0-en_us&'
            'resource.q1=reviews&'
            'filter.q1=isratingsonly%3Aeq%3Afalse&'
            'filter.q1=productid%3Aeq%3A' + str(pid) + '&'
            'filter.q1=contentlocale%3Aeq%3Aen_US&'
            'sort.q1=submissiontime%3Adesc&'
            'stats.q1=reviews&'
            'filteredstats.q1=reviews&'
            'include.q1=authors%2Cproducts%2Ccomments&'
            'filter_reviews.q1=contentlocale%3Aeq%3Aen_US&'
            'filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_US&'
            'filter_comments.q1=contentlocale%3Aeq%3Aen_US&'
            'limit.q1=' + str(limit) + '&'
            'offset.q1=' + str(offset) + '&'
            'limit_comments.q1=3&'
            'callback=BV._internal.dataHandler0'
        )
        res = requests.get(url + query)
        q1 = q1 + json.loads(res.text[26:-1])['BatchedResults']['q1']['Results']
    return {'q0' : q0, 'q1' : q1}
    
    
    
