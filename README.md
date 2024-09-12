# Product Market Fit
## Exercise Overview:
The candidate will build a scoring system to evaluate product/market fit for companies using Salesforce CRM, based on free AI models and publicly available data sources.

Requirements:
* Input: Any Company name (ie. Jollibee or Metrobank).
* Output: Product/market fit score for Salesforce CRM.
* Tools: Any free framework, language, or AI model.
* Deliverables: Functional code and clear documentation explaining the thought process.

## Getting Started
Make sure Docker is installed on your machine. If not, please follow the instructions [here](https://docs.docker.com/get-docker/).
Also Github CLI is required to fork the repository. If not installed, please follow the instructions [here](https://cli.github.com/manual/installation).
```bash
gh repo fork --clone=true https://github.com/dax1216/pmf.git
brew install pyenv pyenv-virtualenv
pyenv init  # append the output to your .zshrc and restart your shell
pyenv install 3.12.2
pyenv virtualenv 3.12.2 pmf-py3.12.2
pyenv activate pmf-py3.12.2  # do this every time you start working on this project
cp env-sample .env
pip install -r requirements.txt
docker compose down --volumes && docker compose up -d
```
## Contributing
* Make sure to create a copy of .env-sample and rename to .env
* OPENAI API Key is needed to run the app. Please sign up [here](https://platform.openai.com/signup) and get the API key.

## Basic Commands
### Create superuser (optional)
```bash
docker exec -it pmf_local_django bash
python manage.py createsuperuser
```
### Run linting, flake8, and isort
```bash
pre-commit install
pre-commit run --all-files
```
## Using the app
* Open your browser and go to http://127.0.0.1:8000/pmf/
* Put in the company on the input field and press Enter
* This will take you to the company list. Status is pending or in_progress until the scores are fetched.
* Refresh the page to see the status change to done.
