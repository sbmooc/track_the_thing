from github import Github
from django.conf import settings

class GitHubClient:

    def __init__(self):
        self.access_token = settings.GITHUB_ACCESS_TOKEN
        if self.access_token:
            self.g = Github(self.access_token)
            self.repo = self.g.get_repo('sbmooc/track_the_thing')

    def create_issue(self, title, body):
        if self.access_token:
            self.repo.create_issue(
                title=title,
                body=body,
                labels=['Site-Generated'])
