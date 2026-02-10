import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


# @pytest.mark.skip(reason="Skipping this test during runtime due to fail")
def test_deleteRecordBeforeExternalPublication(page_setup) -> None:
    logging.info("Starting test_delete_Record_Before_External_Publication")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    title = "delete_Record_Before_External_Publication"
    title = common_utils.createCatalogueRecordTitle(title)
    
    # Get the userId and username from environment variables
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")

    if not userId_reviewer_a:
        raise ValueError("USERNAME_REVIEWER_A environment variable is not set")

    # Login
    common_utils.login(userId_reviewer_a)

    # Create new spatial record
    common_utils.createNewSpatialRecord(title)
    
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")

    # Search record in editor board
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")
    
    # Approve and publish record internally
    common_utils.dirrectApproveRecord(title)

    # Publish record internally
    common_utils.publishRecordInternally()   

    #search record in editor board   
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")
    
     # Delete the record
    time.sleep(2)
    deleteMessage= title + " removed"
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator(catalogue_objects.DELETE_RECORD_BUTTON).click()
    logging.info("Clicking delete record button")    
    expect(page.get_by_role("alert")).to_contain_text(deleteMessage)
       
     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
  
    


