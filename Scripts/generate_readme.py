'''

import os
import datetime
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv

# Load GitHub token from .env
load_dotenv()
USERNAME = "RahulNeuroByte"
TOKEN = os.getenv("GH_TOKEN")

if not TOKEN:
    raise Exception("❌ GitHub token not found. Please set GH_TOKEN in .env file.")

# Create visuals directory
VISUAL_DIR = "visual_stats"
os.makedirs(VISUAL_DIR, exist_ok=True)

# Connect to GitHub
g = Github(TOKEN)
user = g.get_user()
repos = user.get_repos()

# -----------------------
# Data Collection
# -----------------------
langs = {}
topics = {}
forked_count = 0

for repo in repos:
    if repo.fork:
        forked_count += 1
        continue
    if repo.private:
        continue

    for lang, val in repo.get_languages().items():
        langs[lang] = langs.get(lang, 0) + val

    for topic in repo.get_topics():
        topics[topic] = topics.get(topic, 0) + 1

# -----------------------
# Chart: Language Pie
# -----------------------
if langs:
    plt.figure(figsize=(6, 6))
    plt.pie(langs.values(), labels=langs.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("📊 Language Distribution")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/lang_pie.png")
    plt.close()

# -----------------------
# Chart: Topic Bar
# -----------------------
if topics:
    sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(8, 4))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='teal')
    plt.title("📈 Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{VISUAL_DIR}/topic_bar.png")
    plt.close()

# -----------------------
# Chart: GitHub Summary
# -----------------------
contributions = 1298
public_repos = user.public_repos
streak_current = 12
streak_longest = 45
profile_views = 762

labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Views"]
values = [contributions, public_repos, streak_current, streak_longest, profile_views]

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='purple')
plt.title("📋 GitHub Profile Summary")
plt.tight_layout()
plt.savefig(f"{VISUAL_DIR}/summary_bar.png")
plt.close()

# -----------------------
# Replace in Template
# -----------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Read from TEMPLATE_README.md
with open("TEMPLATE_README.md", "r", encoding="utf-8") as f:
    template = f.read()

# Replace placeholders
template = template.replace("{{auto_date}}", timestamp)
template = template.replace("{{forked_count}}", str(forked_count))

# Write to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(template)

print("✅ README.md updated successfully!")


'''










import os
import datetime
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv



import os
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()

TOKEN = os.getenv("GH_TOKEN")
if not TOKEN:
    raise Exception("❌ GitHub token not found.")


# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
USERNAME = "RahulNeuroByte"
TOKEN = os.getenv("GH_TOKEN")

if not TOKEN:
    raise EnvironmentError("❌ GitHub token not found. Set GH_TOKEN in .env or GitHub Secrets.")

# -------------------------------
# Output directory setup
# -------------------------------
VISUAL_DIR = "visual_stats"
os.makedirs(VISUAL_DIR, exist_ok=True)

# -------------------------------
# GitHub API connection
# -------------------------------
g = Github(TOKEN)
user = g.get_user()
repos = user.get_repos()

# -------------------------------
# Collect data
# -------------------------------
langs = {}
topics = {}
forked_count = 0

for repo in repos:
    if repo.fork:
        forked_count += 1
        continue
    if repo.private:
        continue

    # Language stats
    for lang, val in repo.get_languages().items():
        langs[lang] = langs.get(lang, 0) + val

    # Topics
    for topic in repo.get_topics():
        topics[topic] = topics.get(topic, 0) + 1

# -------------------------------
# Chart 1: Language Pie
# -------------------------------
if langs:
    plt.figure(figsize=(6, 6))
    plt.pie(langs.values(), labels=langs.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("📊 Language Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "lang_pie.png"))
    plt.close()

# -------------------------------
# Chart 2: Topic Frequency Bar
# -------------------------------
if topics:
    sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(8, 4))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='teal')
    plt.title("📈 Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "topic_bar.png"))
    plt.close()

# -------------------------------
# Chart 3: GitHub Summary Bar (static or enhanced later)
# -------------------------------
contributions = 1298  # Replace with dynamic logic if desired
public_repos = user.public_repos
streak_current = 12   # Replace with real data if needed
streak_longest = 45   # Replace with real data if needed
profile_views = 762   # Static or from shield.io

labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Views"]
values = [contributions, public_repos, streak_current, streak_longest, profile_views]

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='purple')
plt.title("📋 GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(VISUAL_DIR, "summary_bar.png"))
plt.close()

# -------------------------------
# Template Replacement
# -------------------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

template_path = "TEMPLATE_README.md"
output_path = "README.md"

if not os.path.exists(template_path):
    raise FileNotFoundError("❌ TEMPLATE_README.md not found. Please ensure it's in the repo root.")

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# Inject dynamic content
template = template.replace("{{auto_date}}", timestamp)
template = template.replace("{{forked_count}}", str(forked_count))

# Write final README
with open(output_path, "w", encoding="utf-8") as f:
    f.write(template)

print("✅ README.md updated successfully!")
