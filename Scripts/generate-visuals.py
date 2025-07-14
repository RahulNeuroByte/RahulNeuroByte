import os
from github import Github
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load GitHub token
load_dotenv()
token = os.getenv("GH_TOKEN")
if not token:
    raise Exception("GitHub token not found. Please set GH_TOKEN in .env file")

# Authenticate
g = Github(token)
user = g.get_user()

# Fetch all repos
repos = user.get_repos()

# Language distribution
language_data = {}

for repo in repos:
    lang = repo.language
    if lang:
        language_data[lang] = language_data.get(lang, 0) + 1

# Plotting the language usage
plt.figure(figsize=(8, 6))
plt.pie(language_data.values(), labels=language_data.keys(), autopct='%1.1f%%', startangle=140)
plt.title(f'Language Usage Distribution for {user.login}')
plt.tight_layout()

# Save chart
output_dir = "assets"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "language_distribution.png"))
print(f"✅ Visual saved at {output_dir}/language_distribution.png")
