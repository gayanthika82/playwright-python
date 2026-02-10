# Playwright Test Automation Framework

This project implements UI and API testing using Playwright with Python and pytest.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Visual Studio Code

## Getting Started
Open visual code and run these commands in terminal:
1. Clone the repository
git clone <your-repo-url>
cd test-ui-playwright


2. Set up Python virtual environment
python -m venv venv
.\venv\Scripts\activate


3. Install dependencies
pip install -r requirements.txt
playwright install


## Project Structure
```
test-ui-playwright/
├── tests/              # Test files
├── pages/              # Page object models
├── reports/            # Test reports
├── screenshots/        # Failure screenshots
├── conftest.py        # Pytest configurations
└── requirements.txt    # Project dependencies
```

## Running Tests

Run all tests:
    pytest


Run specific test file:
 
    pytest tests/test_login.py -v
 

Generate HTML report:
 
    pytest --html=reports/test_report.html
 
## Running test with environment files 
Example :
pytest -v --env-file=.env.test --browser-mode=headless .\tests\test_login.py

--env-file      lets you choose the environment profile like QA,DEV,STAGE depends on your project.
--browser-mode  lets you choose wheather you want to run HEADLESS or HEAD(show brower) mode.


## Contributing

Please read our contributing guidelines before submitting pull requests.

## Useful Resources
- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)


## Run test in docker image locally
1. Open powershell as administrator and install
winget install --exact --id Microsoft.AzureCLI

2. Type az login (pop up window will be opened and continue it) in Git Bash

3. Open git bash and type following command to get the token
TOKEN=$(az acr login --name edhunclassacr --expose-token --output tsv --query accessToken)

3. Docker login by using token
docker login edhunclassacr.azurecr.io  --username 00000000-0000-0000-0000-000000000000 --password $TOKEN

4. Pull the image
docker pull edhunclassacr.azurecr.io/azure-build-agent:1.8.3

5. Build the image
docker run --rm -v $(pwd):/app -w /app edhunclassacr.azurecr.io/azure-build-agent

6. To run the test in docker image

- Go to wsl
- Go to project path (ex: /mnt/c/Gaya/Automation/test-ui-playwright)
- Type docker run -it --rm -v $(pwd)/test-ui-playwright:/playwright -w /playwright --name playwright-test edhunclassacr.azurecr.io/azure-build-agent:1.8.3 /bin/bash // Mount to working  directory 
- pytest -v --env-file=.env.test --browser-mode=headless .\tests\test_login.py //To run the test
