from github import Github
import statistics

# Access GitHub API using Personal Access Token
g = Github('<PERSONAL ACCESS TOKEN>')

# Access Kaggle's repositories
kaggle = g.get_user('Kaggle')
repositories = kaggle.get_repos()

# Initialize variables to store statistics specified in question
commits = []
stars = []
contributors = []
branches = []
tags = []
forks = []
releases = []
closed_issues = []
languages = {}

# Loop through each repository
for repo in repositories:
    # Gather repository statistics
    try:
        commits.append(repo.get_commits().totalCount)

        # Gather source code lines per programming language
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.type == "file":
                extension = file_content.name.split('.')[-1]
                if extension in ["py", "java", "c", "cpp", "php", "rb", "js", "html", "css"]:
                    if extension not in languages:
                        languages[extension] = 0
                    languages[extension] += file_content.size
    except:
        pass
    stars.append(repo.stargazers_count)
    contributors.append(repo.get_contributors().totalCount)
    branches.append(repo.get_branches().totalCount)
    tags.append(repo.get_tags().totalCount)
    forks.append(repo.forks_count)
    releases.append(repo.get_releases().totalCount)
    closed_issues.append(repo.get_issues(state='closed').totalCount)

# Print statistics
print("Repository Statistics:")
print("Total Commits:", sum(commits))
print("Median Commits:", statistics.median(commits))
print("Total Stars:", sum(stars))
print("Median Stars:", statistics.median(stars))
print("Total Contributors:", sum(contributors))
print("Median Contributors:", statistics.median(contributors))
print("Total Branches:", sum(branches))
print("Median Branches:", statistics.median(branches))
print("Total Tags:", sum(tags))
print("Median Tags:", statistics.median(tags))
print("Total Forks:", sum(forks))
print("Median Forks:", statistics.median(forks))
print("Total Releases:", sum(releases))
print("Median Releases:", statistics.median(releases))
print("Total Closed Issues:", sum(closed_issues))
print("Median Closed Issues:", statistics.median(closed_issues))

print("\nSource Code Lines per Programming Language:")
for language, lines in languages.items():
    print(language.upper(), ":", lines)
