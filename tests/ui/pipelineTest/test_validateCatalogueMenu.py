import logging
import pytest
from objects_repository import catalogue_objects
from playwright.sync_api import Page,expect
import os

from utils.common_utils import CommonUtils

#@pytest.mark.skip(reason="Skipping this test during runtime due to fail")
@pytest.mark.test_case_ids([89861])
def test_validateCatalogueMenu(page_setup) -> None:
    page = page_setup
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a  = os.getenv("REVIEWER_A_NAME")
    if not userId_reviewer_a:
        raise ValueError("USERNAME_REVIEWER_A environment variable is not set")
    
    common_utils = CommonUtils(page)
    common_utils.login(userId_reviewer_a)

    try:
        page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        page.locator(catalogue_objects.ADD_NEW_RECORD_OPTION).click()
        expect(page.get_by_text("Create a Dataset")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for Add New Record: %s", e)

    try:
        page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        page.locator(catalogue_objects.EDITOR_BOARD_OPTION).click()
        expect(page.get_by_text("Sorted by last updates")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for Editor Board: %s", e)

    try:
        page.locator(catalogue_objects.MAP_MENU).click()
        expect(page.get_by_role("searchbox", name="Search for a place")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for Map Menu: %s", e)
        
    try:
        page.locator(catalogue_objects.SEARCH_MENU).click()
        expect(page.get_by_role("button", name="Sorted by relevancy ")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for Search Menu: %s", e)

    # Navigate to Manage Directory
    try:
        page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        page.locator(catalogue_objects.MANAGE_DIRECTORY_OPTION).click()
        expect(page.locator("#gn-directory-container")).to_contain_text("Manage directory")
    except Exception as e:
        logging.error("Validation failed for Manage Directory: %s", e)

    # Navigate to Import New Records
    try:
        page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        page.locator(catalogue_objects.IMPORT_NEW_RECORD_OPTION).click()
        expect(page.get_by_role("heading")).to_contain_text("Import new records")
    except Exception as e:
        logging.error("Validation failed for Import New Records: %s", e)

    # Navigate to User Profile
    try:
        page.locator(catalogue_objects.USER_NAME).click()
        expect(page.get_by_text("User groupa reviewer")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for User Name: %s", e)
     
    try:
        page.locator(catalogue_objects.USER_PROFILE).click()
        expect(page.get_by_text("User groupa reviewer")).to_be_visible()
    except Exception as e:
        logging.error("Validation failed for User Profile: %s", e)
    
    # Navigate to Catalogue home page
    try:
        portal_page = common_utils.goToPortalHomePage()
        portal_page.close()
    except Exception as e:
        logging.error("Navigation to Portal Home Page failed: %s", e)
    
     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
