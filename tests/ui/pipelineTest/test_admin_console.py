import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


# @pytest.mark.skip(reason="Skipping this test during runtime due to fail")

def test_admin_console(page_setup) -> None:
    
    logging.info("Starting test_admin_console")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    

    # Get the userId and username from environment variables
    userId_admin = os.getenv("USERNAME_ADMIN")
    username_admin = os.getenv("ADMIN_NAME")

    if not userId_admin:
        raise ValueError("USERNAME_ADMIN environment variable is not set")

    # Login
    common_utils.login(userId_admin)
    logging.info("User %s logged in successfully", username_admin)
    time.sleep(2)
    # Navigate to Admin Console

    page.locator(catalogue_objects.ADMIN_CONSOLE).click()
    logging.info("Clicking Admin Console menu")
    page.locator(catalogue_objects.SUMMARY_MENU_ITEM).click()
    logging.info("Clicking Summary menu item")    
    expect(page.locator(catalogue_objects.SUMMARY_MENU_ITEM_VALIDATION)).to_be_visible()
    logging.info("Validated the presence of the text: 'Total number of records visible to you.'")
    page.locator(catalogue_objects.CATALOGUE_HOME_MENU).click()  # Click on CATALOGUE_HOME_MENU to reset menu state

    page.locator(catalogue_objects.ADMIN_CONSOLE).click()
    logging.info("Clicking Admin Console menu")
    page.locator(catalogue_objects.METADATA_AND_TEMPLATE_MENU_ITEM).click()
    logging.info("Clicking Metatdata and Template menu item")    
    expect(page.locator(catalogue_objects.METADATA_AND_TEMPLATE_MENU_ITEM_VALIDATION)).to_be_visible()
    logging.info("Validated the presence of the text: 'Load samples and templates for metadata standards'")
    page.locator(catalogue_objects.CATALOGUE_HOME_MENU).click()  # Click on CATALOGUE_HOME_MENU to reset menu state

    
    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_admin)

   
    