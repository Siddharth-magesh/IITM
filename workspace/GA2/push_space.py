import os
from huggingface_hub import HfApi, Repository

HF_USER = os.environ.get('HF_USER')
HF_TOKEN = os.environ.get('HF_TOKEN')
SPACE_NAME = 'ga2-25c816'

if not HF_USER or not HF_TOKEN:
    print('Please set HF_USER and HF_TOKEN environment variables and run again')
    raise SystemExit(1)

api = HfApi()
repo_id = f"{HF_USER}/{SPACE_NAME}"

print('Creating space repo (if not exists)...')
api.create_repo(name=SPACE_NAME, repo_type='space', private=False, exist_ok=True)

git_url = f"https://{HF_USER}:{HF_TOKEN}@huggingface.co/spaces/{HF_USER}/{SPACE_NAME}"
print('Cloning and pushing to', git_url)
repo = Repository(local_dir='hf_space_repo', clone_from=git_url, use_auth_token=HF_TOKEN)
repo.copy_to(os.getcwd(), include_hidden=True)
repo.push_to_hub(commit_message='Add Docker Space files')
print('Pushed. Now go to the Space settings on the Hugging Face website to set hardware (CPU Basic) and add secret GA2_TOKEN_AC88')
