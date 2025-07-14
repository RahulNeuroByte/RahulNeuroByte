import os
import datetime
import matplotlib.pyplot as plt
from github import Github

# 1. CONFIG
USERNAME = "RahulNeuroByte"
TOKEN = os.getenv("GH_TOKEN")  # Secret Token
VISUAL_DIR = "visual_stats"

# Create folder if not exists
os.makedirs(VISUAL_DIR, exist_ok=True)

# 2. INIT
g = Github(TOKEN)
user = g.get_user()
repos = user.get_repos()

# 3. Extract Langs & Topics
langs = {}
topics = {}

for repo in repos:
    if repo.fork or repo.private:
        continue

    for lang, val in repo.get_languages().items():
        langs[lang] = langs.get(lang, 0) + val

    for topic in repo.get_topics():
        topics[topic] = topics.get(topic, 0) + 1

# 4. Language Pie Chart
if langs:
    plt.figure(figsize=(6, 6))
    plt.pie(langs.values(), labels=langs.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("📊 Language Distribution")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/lang_pie.png")
    plt.close()

# 5. Topic Frequency Bar Chart
if topics:
    sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(8, 4))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='teal')
    plt.title("📈 Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/topic_bar.png")
    plt.close()

# 6. GitHub Profile Summary Bar Chart (Manual or via GitHub GraphQL API in future)
contributions = 1298
public_repos = 23
streak_current = 12
streak_longest = 45
profile_views = 762  # You can automate via external badge if desired

labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Views"]
values = [contributions, public_repos, streak_current, streak_longest, profile_views]

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='purple')
plt.title("📊 GitHub Profile Summary")
plt.tight_layout()
plt.savefig(f"{VISUAL_DIR}/summary_bar.png")
plt.close()

print("✅ Visual charts generated!")
