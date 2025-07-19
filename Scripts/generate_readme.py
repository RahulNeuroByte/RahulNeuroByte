
import os
import datetime
import matplotlib.pyplot as plt
from github import Github
from dotenv import load_dotenv
import requests

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
repos = sorted(
    [r for r in user.get_repos() if not r.fork and not r.private],
    key=lambda r: r.stargazers_count,
    reverse=True
)

# -------------------------------
# Get Total Contributions Using GraphQL
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

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": GRAPHQL_QUERY},
    headers={"Authorization": f"Bearer {TOKEN}"}
)

try:
    contributions = response.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
except:
    contributions = 0

followers = user.followers
public_repos = user.public_repos
stars = sum(repo.stargazers_count for repo in repos)

# -------------------------------
# Collect Language and Topic Data
# -------------------------------
langs = {}
topics = {}
forked_count = 0

for repo in user.get_repos():
    if repo.fork:
        forked_count += 1
        continue
    if repo.private:
        continue

    for lang, val in repo.get_languages().items():
        langs[lang] = langs.get(lang, 0) + val

    for topic in repo.get_topics():
        topics[topic] = topics.get(topic, 0) + 1

# -------------------------------
# Chart 1: Language Pie
# -------------------------------
if langs:
    plt.figure(figsize=(6, 6))
    plt.pie(langs.values(), labels=langs.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("\U0001F4CA Language Distribution")
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
    plt.title("\U0001F4C8 Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "topic_bar.png"))
    plt.close()

# -------------------------------
# Chart 3: GitHub Summary Bar
# -------------------------------
labels = ["Contributions", "Repos", "Followers", "Stars"]
values = [contributions, public_repos, followers, stars]

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='purple')
plt.title("\U0001F4CB GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(VISUAL_DIR, "summary_bar.png"))
plt.close()

# -------------------------------
# Load README Template
# -------------------------------
template_path = "TEMPLATE_README.md"
output_path = "README.md"

if not os.path.exists(template_path):
    raise FileNotFoundError("❌ TEMPLATE_README.md not found.")

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# -------------------------------
# Inject Auto Date and Dynamic Data
# -------------------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
template = template.replace("{{auto_date}}", timestamp)
template = template.replace("{{forked_count}}", str(forked_count))
template = template.replace("{{contribution_count}}", str(contributions))
template = template.replace("{{follower_count}}", str(followers))
template = template.replace("{{star_count}}", str(stars))
template = template.replace("{{repo_count}}", str(public_repos))

# -------------------------------
# Inject Tech Stack into README
# -------------------------------
tech_stack_md = """

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OOPs-4B8BBE?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white"/>
  <img src="https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>
  <img src="https://img.shields.io/badge/NoSQL-005571?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/MS Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google Cloud Platform-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/Machine Learning-FF6F00?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/NLP-7F00FF?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Deep Learning-8E44AD?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Generative AI-FF69B4?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/RAG-800000?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/LLM-00008B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Hugging Face-FCC624?style=for-the-badge&logo=huggingface&logoColor=black"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyCharm-000000?style=for-the-badge&logo=pycharm&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pylance-007ACC?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/VS Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"/>
</p>
"""
template = template.replace("{{auto_tech_tags}}", tech_stack_md)

# -------------------------------
# Generate Project Cards
# -------------------------------
project_cards_md = ""
top_repos = [
    repo for repo in repos
    if not repo.fork and not repo.private and not repo.archived
][:3]

for repo in top_repos:
    card = f"""
<p align="center">
  <a href="{repo.html_url}">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={repo.name}&theme=tokyonight" />
  </a>
</p>
"""
    project_cards_md += card

template = template.replace("{{auto_project_cards}}", project_cards_md)

# -------------------------------
# Save Final README.md
# -------------------------------
with open(output_path, "w", encoding="utf-8") as f:
    f.write(template)

print("✅ README.md updated successfully!")

# -------------------------------
# Auto Git Commit (optional)
# -------------------------------
os.system("git add README.md && git commit -m '🔄 Auto-update README' && git push")

















