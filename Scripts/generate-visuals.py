import os
from github import Github
from dotenv import load_dotenv
import matplotlib.pyplot as plt

#  Load environment variables
load_dotenv()
token = os.getenv("GH_TOKEN")
if not token:
    raise Exception(" GitHub token not found. Please set GH_TOKEN in .env file.")

#  Setup GitHub client
g = Github(token)
user = g.get_user()
repos = user.get_repos()

#  Create output folder
output_dir = "assets"
os.makedirs(output_dir, exist_ok=True)

#  1. Language Distribution
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
    plt.title(f' Language Usage Distribution for {user.login}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "language_distribution.png"))
    plt.close()

#  2. Topic Frequency
topic_data = {}
for repo in repos:
    if repo.fork or repo.private:
        continue
    topics = repo.get_topics()
    for topic in topics:
        topic_data[topic] = topic_data.get(topic, 0) + 1

if topic_data:
    sorted_topics = dict(sorted(topic_data.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(10, 5))
    plt.bar(sorted_topics.keys(), sorted_topics.values(), color='seagreen')
    plt.title(" Repo Topics Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "topic_frequency.png"))
    plt.close()

#  3. Manual GitHub Profile Summary (Static Inputs)
summary_labels = ["Contributions", "Repos", "Current Streak", "Longest Streak", "Profile Views"]
summary_values = [1298, 23, 12, 45, 762]  #  Customize these numbers as needed

plt.figure(figsize=(8, 4))
plt.bar(summary_labels, summary_values, color='mediumpurple')
plt.title(" GitHub Profile Summary")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "profile_summary.png"))
plt.close()

print(" All visual charts successfully generated in the 'assets' folder.")
