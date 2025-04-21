from django import template

register = template.Library()

@register.filter
def filter_by_review(responses, review_id):
    """Filter responses by review ID"""
    return [response for response in responses if response.review_id == review_id]

@register.filter
def regroup_by_reviewer(reviews):
    """Regroup reviews by reviewer and return a list of (reviewer_id, reviewer_name) tuples"""
    reviewers = {}
    for review in reviews:
        if review.reviewer_id not in reviewers:
            reviewers[review.reviewer_id] = review.reviewer.username
    
    return reviewers.items()

@register.filter
def unique_reviewers(reviewers):
    """Return a list of unique reviewers based on their ID"""
    unique_dict = {}
    for reviewer in reviewers:
        if reviewer.id not in unique_dict:
            unique_dict[reviewer.id] = reviewer
    
    return unique_dict.values()

