import os
import datetime
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv

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
# Chart 3: GitHub Summary Bar
# -------------------------------
contributions = 1298  # You can replace with real data if using GitHub GraphQL
public_repos = user.public_repos
streak_current = 12   # Static placeholder
streak_longest = 45   # Static placeholder
profile_views = 762   # Static or from shields.io

labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Views"]
values = [contributions, public_repos, streak_current, streak_longest, profile_views]

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='purple')
plt.title("📋 GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(VISUAL_DIR, "summary_bar.png"))
plt.close()

# -------------------------------
# Load README Template
# -------------------------------
template_path = "TEMPLATE_README.md"
output_path = "README.md"

if not os.path.exists(template_path):
    raise FileNotFoundError("❌ TEMPLATE_README.md not found. Please ensure it's in the repo root.")

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# -------------------------------
# Inject Auto Date and Forked Count
# -------------------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
template = template.replace("{{auto_date}}", timestamp)
template = template.replace("{{forked_count}}", str(forked_count))

# -------------------------------
# Generate Tech Stack Section
# -------------------------------
tech_stack = [
    "Python", "Pandas", "NumPy", "Scikit-learn", "PyTorch",
    "HuggingFace", "Matplotlib", "LangChain", "Streamlit"
]

tech_stack_md = "\n".join([f"- 🛠️ {tech}" for tech in tech_stack])
template = template.replace("{{auto_tech_tags}}", tech_stack_md)

# -------------------------------
# Generate Project Cards Section
# -------------------------------
starred_repos = user.get_starred()[:3]  # You can use get_repos() instead if you want your own
project_cards_md = ""

for repo in starred_repos:
    card = f"""
<p align="center">
  <a href="{repo.html_url}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={repo.owner.login}&repo={repo.name}&theme=tokyonight" />
  </a>
</p>
"""
    project_cards_md += card

template = template.replace("{{auto_project_cards}}", project_cards_md)

# -------------------------------
# Write Final README
# -------------------------------
with open(output_path, "w", encoding="utf-8") as f:
    f.write(template)

print("✅ README.md updated successfully!")
