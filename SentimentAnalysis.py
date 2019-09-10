import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='cZ6Ug3411dsANw',
                     client_secret='VNv8mtS5zEFNE1YiDniwF6-1rZk',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def process_comments(comments, neutral_comments, positive_comments, negative_comments):
    # this for loop traverses through all the main comments, variable item in the for loop is each comment in the comments list
    for item in comments:
        # gets the positive value to see where the comment will belong
        positive = get_text_positive_proba(item.body)

        # gets the neutral value of the comment to classify the comment in the correct list later
        neutral = get_text_neutral_proba(item.body)

        # gets the negative value of the comment to classify the comment in the correct list later
        negative = get_text_negative_proba(item.body)

        # compare the negative value of the comment with the other values to see if the comment is a negative value
        if negative > neutral and negative > positive:
            # if it is a negative comment, add it to the negative comments list
            negative_comments.append(item.body)

        # compare the neutral value of the comment with other values to see if the comment is a neutral value
        elif neutral > positive and neutral > negative:
            # if it is a neutral comment, add it to the neutral comments list
            neutral_comments.append(item.body)

        # since the other two values taken care of, the only other option is a positive comment
        else:
            # if it is not a negative comment or a neutral comment, add it to the positive comments list
            positive_comments.append(item.body)

        # recursive call, this time we send the replies of the comment as a parameter and then the replies of the replies and so on until there are no more replies
        process_comments(item.replies, neutral_comments,
                         positive_comments, negative_comments)


def main():
    comments = get_submission_comments(
        'https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    
    # create list of negative comments
    negative_comments = []
    # create list of positive comments
    positive_comments = []
    # create list of neutral comments
    neutral_comments = []

    # call process_comments with 4 lists as parameters
    process_comments(comments, neutral_comments,
                     positive_comments, negative_comments)

    # testing neutral comments list by printing the first five comments in neutral comments list
    print("Neutral Comments List:")
    for item in range(5):
        print(neutral_comments[item])

    print()
    #testing positive comments list by printing the first five comments in positive comments list
    print("Positive Comments List:")
    for item in range(5):
        print(positive_comments[item])

    print()
    # testing negative comments list by printing all comments in negative comments list since there are only two negative comments in the list
    print("Negative Comments List:")
    for item in range(len(negative_comments)):
        print(negative_comments[item])

    print()
    # testing all lists by printing the last comment in each list and comparing it with the website
    print("Last Neutral Comment:")
    print(neutral_comments[-1])
    print()
    print("Last Positive Comment:")
    print(positive_comments[-1])
    print()
    print("Last Negative Comment:")
    print(negative_comments[-1])


main()
