import datetime
import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import expect
import os
from utils.common_utils import CommonUtils

title=None

@pytest.mark.dependency()
@pytest.mark.test_case_ids([247679])
def test_validatePublishForGroupEditors_step1(page_setup) -> None:
    global title
    logging.info("Starting test_validatePublishForGroupEditors_step1")
    page = page_setup    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "validatePublishForGroupEditors_"
    title = common_utils.createCatalogueRecordTitle(title)
      
    # Get the userId and username from environment variables
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")   
    if not userId_reviewer_a:
        raise ValueError("Environment variables USERNAME_REVIEWER_A, is not set.")
    
    # Login
    common_utils.login(userId_reviewer_a)
    # Create new spatial record
    page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
    logging.info("Clicking contribute menu")
    page.locator(catalogue_objects.ADD_NEW_RECORD_OPTION).click()
    logging.info("Clicking add new record option")
    page.locator(catalogue_objects.DATASET).click()
    logging.info("Clicking dataset option")
    page.locator(catalogue_objects.TEMPLATE_A).click()
    logging.info("Clicking template A option")
    page.locator(catalogue_objects.GROUP_DDL_A_OPTION).select_option("a")
    logging.info("Selecting group option a")
    page.locator(catalogue_objects.CREATE_TOGGLE_BUTTON).click()
    logging.info("Clicking create toggle button")
    page.locator(catalogue_objects.PUBLISH_FOR_GROUP_EDITORS_CHECKBOX).is_checked() or page.locator(catalogue_objects.PUBLISH_FOR_GROUP_EDITORS_CHECKBOX).click()
    logging.info("Selecting publish for group editors checkbox")
    page.locator(catalogue_objects.CREATE_BUTTON).click()
    logging.info("Clicking create button")
    page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
    page.locator(catalogue_objects.TITLE_TEXTBOX).fill(title)
    logging.info("Entering title: %s", title)

    page.locator(catalogue_objects.VALIDATE_BUTTON).wait_for(state="visible", timeout=10000)
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    time.sleep(2)
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")
       
    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)

@pytest.mark.test_case_ids([247679])
@pytest.mark.dependency(depends=["test_validatePublishForGroupEditors_step1"])
def test_validatePublishForGroupEditors_step2(page_setup) -> None:     
    #Login as Business Data Trustee 
    global title
    page = page_setup
    common_utils = CommonUtils(page)
    editTitle = "Edit_validatePublishForGroupEditors"
    editTitle = common_utils.createCatalogueRecordTitle(editTitle)
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    username_editor_a = os.getenv("EDITOR_A_NAME")
    logging.info("Start testing test_validatePublishForGroupEditors_step2")
    
    #common_utils = CommonUtils(page)
    common_utils.login(userId_editor_a)    
    #search record in editor board
    common_utils.searchRecordInEditorBoard(title)
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")   
    #Validate edit button is present
    page.locator(catalogue_objects.EDIT_RECORD_BUTTON).wait_for(state="visible", timeout=10000)
    page.locator(catalogue_objects.EDIT_RECORD_BUTTON).click()
    logging.info("Clicking on edit record button")
    page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
    logging.info("Clearing title textbox")
    page.locator(catalogue_objects.TITLE_TEXTBOX).fill(editTitle)
    logging.info("Clicking on add title button")
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")
    
    #Validate working copy by opening original record in editor board
    time.sleep(3)
    common_utils.searchRecordInEditorBoard(editTitle)
     # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=editTitle)).click()
    logging.info("Clicking on record title link to go to record details")
    time.sleep(3)

    # Delete the record
    deleteMessage = editTitle+" removed"
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator(catalogue_objects.DELETE_RECORD_BUTTON).click()
    logging.info("Clicking delete record button")  
    page.get_by_role("alert").wait_for(state="visible", timeout=10000)
    expect(page.get_by_role("alert")).to_contain_text(deleteMessage)
    time.sleep(1)

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)

    
   

