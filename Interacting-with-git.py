# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: conda_python3
#     language: python
#     name: conda_python3
# ---

# %cd /home/ec2-user/SageMaker/

# +
import getpass

# Prompt for GitHub username and PAT securely
#username = input("GitHub Username: ")
#token = getpass.getpass("GitHub Personal Access Token (PAT): ")

# +
# #!git config --global user.name "Manoj Elavalli" # This is your GitHub username (or just your name), which will appear in the commit history as the author of the changes.
# #!git config --global user.email "nambiarmanoj@gmail.coom" # This should match the email associated with your GitHub account so that commits are properly linked to your profile.
# -

# !pip install jupytext

# Adjust filename(s) if you used something different
# !jupytext --to py Interacting-with-S3.ipynb
