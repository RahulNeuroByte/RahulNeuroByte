import os
import datetime
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
TOKEN = os.getenv("GH_TOKEN")

if not TOKEN:
    raise Exception("❌ GitHub token not found. Please set GH_TOKEN in .env or GitHub Secrets.")

# -------------------------------
# GitHub API Setup
# -------------------------------
g = Github(TOKEN)
user = g.get_user()
repos = user.get_repos()

# -------------------------------
# Output Directory
# -------------------------------
OUTPUT_DIR = "assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# 1. Language Distribution
# -------------------------------
language_data = {}
for repo in repos:
    if repo.fork or repo.private:
        continue
    lang = repo.language
    if lang:
        language_data[lang] = language_data.get(lang, 0) + 1

if language_data:
    plt.figure(figsize=(8, 6))
    plt.pie(language_data.values(), labels=language_data.keys(), autopct='%1.1f%%', startangle=140)
    plt.title(f"Language Usage Distribution for {user.login}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "language_distribution.png"))
    plt.close()

# -------------------------------
# 2. Topic Frequency
# -------------------------------
topic_data = {}
for repo in repos:
    if repo.fork or repo.private:
        continue
    for topic in repo.get_topics():
        topic_data[topic] = topic_data.get(topic, 0) + 1

if topic_data:
    sorted_topics = dict(sorted(topic_data.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(10, 5))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='seagreen')
    plt.title("Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "topic_frequency.png"))
    plt.close()

# -------------------------------
# 3. Profile Summary (Static or Placeholder)
# -------------------------------
summary_labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Profile Views"]
summary_values = [
    1298,                  # Contributions (static or estimate)
    user.public_repos,     # Public repos
    12,                    # Current streak (placeholder)
    45,                    # Longest streak (placeholder)
    762                    # Profile views (placeholder or shield.io)
]

plt.figure(figsize=(8, 4))
plt.bar(summary_labels, summary_values, color='mediumpurple')
plt.title("GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "profile_summary.png"))
plt.close()

# -------------------------------
# Done
# -------------------------------
print("✅ All visual charts successfully generated in the 'assets' folder.")
