'''
This example shows how we fetched the issues from the Infineon organisation on GitHub.
Feel free to modify this code and fetch the issues again depending on your preferences.
If you run into API limits you can talk to us, maybe we can fetch some data for you using our access tokens.
'''

from github import Github
from datetime import datetime, timedelta
import pandas as pd

# Filter pandas warnings for better readability of output
import warnings
warnings.filterwarnings("ignore")

def isInfineonMember(user):
    if 'Infineon' in user.get_orgs():
        return True
    else:
        return False

def main():
    
    try:
        import secret
        github = Github(secret.access_token)
    except:
        github = Github()

    github_org = 'Infineon'
    ifx = github.get_organization(github_org)

    # Go through all open GitHub issues and put them in a Pandas Dataframe

    df = pd.DataFrame()

    issue_count = 0

    for repo in ifx.get_repos():
        #print(f'Working on repo {repo.name}...')
        issues = repo.get_issues(state='all') # state='all' -> we also take closed issues for training.

        for issue in issues:
            issue_count += 1
            print(f'Current issue: #{issue_count} (Repo: {repo.name}, Issue: {issue.title})', end='\r')
            comments = issue.get_comments()
            concatenated_comment = f''
            for comment in comments:
                #print(f'comment is {comment.body} and on {comment.created_at} and updated at {comment.updated_at}')
                if isInfineonMember(comment.user): addition = ' (member of Infineon)'
                else: addition = ''
                concatenated_comment = concatenated_comment + f'comment is {str(comment.body)} and on {comment.created_at} and updated at {comment.updated_at} by user {str(comment.user.name)}{addition}. \n'
            #print (concatenated_comment)
            if issue.pull_request == None: issue_type = 'issue'
            else: issue_type = 'pull-request'
            # These closed_by values are only available for closed issues.
            try:
                closed_by = str(issue.closed_by.name)
                closed_by_infineon = isInfineonMember(issue.closed_by),
            except:
                closed_by = None
                closed_by_infineon = False
            issue_data = {
                'id': [str(issue.id)],
                'title': [str(issue.title)],
                'repo_name': [str(repo.name)],
                'type': [issue_type],
                'pr': [issue_type], # deprecated, don't use anymore
                'state': [str(issue.state)],
                'created': [issue.created_at],
                'updated': [issue.updated_at],
                'modified': [issue.last_modified_datetime],
                'body': [str(issue.body)],
                'user_login': [str(issue.user.login)],
                'user_name': [str(issue.user.name)],
                'is_infineon':[isInfineonMember(issue.user)],
                'url': [str(issue.url)],
                'comments': [issue.comments],
                'comments_url': [str(issue.comments_url)],
                'number': [issue.number],
                'parent_url':[str(issue._parentUrl)],
                'user_type': [str(issue.user.type)],
                'raw_data':[str(issue.raw_data)],
                'labels': [[str(x) for x in issue.labels]],
                'assignees': [[str(x) for x in issue.assignees]],
                'requester':[str(issue._requester)],
                # added attributes
                'closed': [issue.closed_at], # deprecated, don't use anymore
                'closed_at': [issue.closed_at],
                'alr':[str(issue.active_lock_reason)],
                'etag':[str(issue.etag)],
                'comment':[concatenated_comment],
                'closed_by':[closed_by],
                'closed_by_infineon':[closed_by_infineon],
                'comments_list':[[str(x.body) for x in issue.get_comments()]]
            }

            df = pd.concat([
                df, 
                pd.DataFrame(issue_data)
                ], ignore_index=True)
            #print(df)
        # For testing: End loop after first few issues
        
        #if not df.empty: break
        if len(df) > 100: break

    # Make the issue ID the Dataframe index
    df.set_index('id', inplace=True)

    # Write Dataframe to Pickle file
    print(100*'-')
    print('Saving dataframe:')
    print(df)
    df.to_pickle('github_issues_test.pkl')

    # Test readback from Pickle file
    '''
    print('Loading dataframe:')
    df = pd.read_pickle('github_issues_new.pkl')
    print(df)
    '''

if __name__ == '__main__':
    main()