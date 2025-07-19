import os
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv
import requests

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
USERNAME = "RahulNeuroByte"
TOKEN = os.getenv("GH_PAT")

if not TOKEN:
    raise EnvironmentError("❌ GitHub token not found. Please set GH_PAT in .env or GitHub Secrets.")

# -------------------------------
# GitHub API connection
# -------------------------------
g = Github(TOKEN)
user = g.get_user()
repos = [repo for repo in user.get_repos() if not repo.fork and not repo.private]

# -------------------------------
# GraphQL API for Contributions
# -------------------------------
GRAPHQL_QUERY = f"""
{{
  user(login: "{USERNAME}") {{
    contributionsCollection {{
      contributionCalendar {{
        totalContributions
      }}
    }}
  }}
}}
"""

res = requests.post(
    "https://api.github.com/graphql",
    json={"query": GRAPHQL_QUERY},
    headers={"Authorization": f"Bearer {TOKEN}"}
)

try:
    contributions = res.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
except Exception as e:
    print("⚠️ Error fetching contributions via GraphQL:", e)
    contributions = 0

followers = user.followers
public_repos = user.public_repos
stars = sum(repo.stargazers_count for repo in repos)

# -------------------------------
# Output Directory for Visuals
# -------------------------------
OUTPUT_DIR = "visual_stats"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# Chart 1: Language Distribution Pie
# -------------------------------
langs = {}
for repo in repos:
    for lang, val in repo.get_languages().items():
        langs[lang] = langs.get(lang, 0) + val

if langs:
    plt.figure(figsize=(6, 6))
    plt.pie(langs.values(), labels=langs.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("📊 Language Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "lang_pie.png"))
    plt.close()

# -------------------------------
# Chart 2: Topics Frequency Bar
# -------------------------------
topics = {}
for repo in repos:
    for topic in repo.get_topics():
        topics[topic] = topics.get(topic, 0) + 1

if topics:
    sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(8, 4))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='teal')
    plt.title("📈 Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "topic_bar.png"))
    plt.close()

# -------------------------------
# Chart 3: GitHub Profile Summary Bar
# -------------------------------
summary_labels = ["Contributions", "Repos", "Followers", "Stars"]
summary_values = [contributions, public_repos, followers, stars]

plt.figure(figsize=(8, 4))
plt.bar(summary_labels, summary_values, color='mediumpurple')
plt.title("📋 GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "summary_bar.png"))
plt.close()

# -------------------------------
# Done
# -------------------------------
print("✅ Visual charts generated in 'visual_stats/' folder")
