import datetime
import pytest
import os
import base64
from dotenv import load_dotenv,find_dotenv
import pytest_html
from playwright.sync_api import sync_playwright, Page
from pathlib import Path
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)



@pytest.fixture(scope="session")
def playwright_instance():
    try:
        with sync_playwright() as playwright:
            yield playwright
    except Exception as e:
        logging.error(f"Failed to create playwright instance: {str(e)}")
        raise


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env-file",
        action="store",
        default=".env.test",
        help="Environment file to load (e.g. .env.test, .env.prod)"
    )
    parser.addoption(
        "--browser-mode",
        action="store",
        default="headed",
        choices=["headed", "headless"],
        help="Browser mode: headed or headless"
    )

@pytest.fixture(scope="session", autouse=True)
def load_env(request):
    """Load environment variables from specified file"""
    env_file = request.config.getoption("--env-file")
    if not os.path.exists(env_file):
        raise FileNotFoundError(f"Environment file not found: {env_file}")
    
    load_dotenv(find_dotenv(env_file))  # Use find_dotenv to locate the file
    # Alternatively, you can use:
   # load_dotenv(env_file)
    logging.info(f"Loaded environment from: {env_file}")



@pytest.fixture(scope="session")
def browser_mode(request):
    """Get browser mode from command line argument"""
    return request.config.getoption("--browser-mode")

@pytest.fixture(scope="session")
def browser(playwright_instance, browser_mode):
    """Modified browser fixture with dynamic headless mode"""
    try:
        browser_options = {
            "headless": browser_mode == "headless",
            "args": ["--start-maximized"]
        }
        
        browserType = os.getenv("BROWSER_TYPE", "chromium")
        if browserType == "firefox":
            browser = playwright_instance.firefox.launch(**browser_options)
        elif browserType == "webkit":
            browser = playwright_instance.webkit.launch(**browser_options)
        else:
            browser = playwright_instance.chromium.launch(**browser_options)
            
        logging.info(f"Started {browserType} browser in {browser_mode} mode")
        yield browser
        browser.close()
    except Exception as e:
        logging.error(f"Browser setup failed: {str(e)}")
        raise
@pytest.fixture(scope="function")
def page_setup(browser):
    """Setup page with default configurations"""
    try:
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.set_default_navigation_timeout(30000)
        page.set_default_timeout(30000)
        page.goto(os.getenv("APP_URL"))
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Add delay between clicks
        page.on("click", lambda: page.wait_for_timeout(500))
        
        yield page
        #page.close()
    except Exception as e:
        logging.error(f"Page setup failed: {str(e)}")
        raise
    finally:
        # Ensure the browser context and page are closed after each test
        if not page.is_closed():
            page.close()
        context.close()

@pytest.fixture
def handle_popup():
    """Helper fixture for handling popups"""
    def _handle_popup(page, action):
        try:
            with page.expect_popup() as popup_info:
                action()
            return popup_info.value
        except Exception as e:
            logging.error(f"Popup handling failed: {str(e)}")
            raise
    return _handle_popup



def pytest_html_report_title(report):
    report.title = "Pytest HTML Report Example"


# Pytest-html configuration
def pytest_configure(config):
    # Set the report file name and location
    config.option.htmlpath = "reports/test_report.html"
    config.option.self_contained_html = True  # Embed resources in the HTML file


# Hook to capture screenshots for failed tests
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" and report.failed:
        # Define the screenshot path        
        now = datetime.datetime.now()
        screenshot_name = f"failed_screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = Path("./screenshot/"+screenshot_name)

        # Remove the old screenshot if it exists
        if screenshot_path.exists():
            screenshot_path.unlink()

        # Capture a new screenshot (assuming you use Playwright's page object)
        page = item.funcargs.get("page_setup")
        if page:
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
            page.screenshot(path=str(screenshot_path))

            # Encode the screenshot and attach it to the report
            with open(screenshot_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                extra.append(pytest_html.extras.image(encoded_string))
        report.extras = extra


# Customizing the HTML report
@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    # Add a header for the screenshot column
    cells.insert(2, "Screenshot")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    # Insert the screenshot into the results table if it exists
    screenshot = next(
        (extra for extra in getattr(report, "extra", []) if extra.get("image")),
        None,
    )
    if screenshot:
        cells.insert(2, f'<a href="data:image/png;base64,{screenshot["content"]}" target="_blank">View</a>')
    else:
        cells.insert(2, "N/A")

def pytest_sessionstart(session):
    screenshot_dir = Path("./screenshot")
    if screenshot_dir.is_dir():
        for file in screenshot_dir.iterdir():
            if file.is_file():
                file.unlink()
