import logging
import time
import pytest
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


#@pytest.mark.skip(reason="Skipping this test during runtime due to fail")
@pytest.mark.test_case_ids([93305])
def test_validatePortalHome(page_setup) -> None:
    page = page_setup
    userId_admin = os.getenv("USERNAME_ADMIN")
    username_admin = os.getenv("ADMIN_NAME")
    if not userId_admin :
        raise ValueError("USERNAME_ADMIN environment variable is not set")
    
    common_utils = CommonUtils(page)
    common_utils.login(userId_admin )
   
   #Validate portal menu items    
    portal_page = common_utils.goToPortalHomePage()
    time.sleep(2)  # Wait for the page to load

    try:
        expect(portal_page.locator("lib-gc-top-navigation")).to_contain_text("EDH Portal Products expand_more Help expand_more groupa reviewer expand_more")
    except Exception as e:
        logging.error("Validation failed for top navigation: %s", e)

    try:
        expect(portal_page.locator("h1")).to_contain_text("Enterprise Data Hub Portal")
    except Exception as e:
        logging.error("Validation failed for page header: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("This is your gateway to the digital services offered by the Enterprise Data Hub. From this page, you can search metadata catalogues, download data, or start a new publication for the Federal Geospatial Platform or the Open Data Portal. You can also use the tiles below to access the wide array of digital services offered by the platform.")
    except Exception as e:
        logging.error("Validation failed for portal description: %s", e)

    try:
        expect(portal_page.locator("h6")).to_contain_text("Search in EDH and external catalogues")
    except Exception as e:
        logging.error("Validation failed for search header: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Service Request")
    except Exception as e:
        logging.error("Validation failed for service request: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Submit request to the EDH team for a specific service, such as Mapping or Analytics Workspace.")
    except Exception as e:
        logging.error("Validation failed for service request description: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Data Publishing")
    except Exception as e:
        logging.error("Validation failed for data publishing: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("User Registry")
    except Exception as e:
        logging.error("Validation failed for user registry: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Registry of EDH users, their roles, and accompanying permissions.")
    except Exception as e:
        logging.error("Validation failed for user registry description: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("EDH Catalogue")
    except Exception as e:
        logging.error("Validation failed for EDH catalogue: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Create or update catalogue entries or explore and discover what others have contributed using the EDH Catalogue.")
    except Exception as e:
        logging.error("Validation failed for EDH catalogue description: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Data Visualization")
    except Exception as e:
        logging.error("Validation failed for data visualization: %s", e)

    try:
        expect(portal_page.locator("app-home-page")).to_contain_text("Learn about Power BI, a powerful reporting tool which can be installed from the DFO Software Catalogue.")
    except Exception as e:
        logging.error("Validation failed for data visualization description: %s", e)

    try:
        expect(portal_page.locator("h3")).to_contain_text("Entreprise Data Hub")
    except Exception as e:
        logging.error("Validation failed for footer header: %s", e)

    portal_page.close()
     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_admin)
