import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


# @pytest.mark.skip(reason="Skipping this test during runtime due to fail")
@pytest.mark.test_case_ids([88118])
def test_approveWorkingCopy(page_setup) -> None:
    logging.info("Starting test_approve_workingCopy")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    title = "ApproveWorkingCopy"
    title = common_utils.createCatalogueRecordTitle(title)
    editTitle = "Edit Approve Working Copy Title"
    editTitle = common_utils.createCatalogueRecordTitle(editTitle)

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
    
    time.sleep(5)
    #page.locator(catalogue_objects.EDIT_RECORD_BUTTON).click()
    page.get_by_role("link", name="Edit").click()
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
    common_utils.searchRecordInEditorBoard(title)
    expect(page.locator("body")).to_contain_text("Approved (Working copy is Draft)")
    expect(page.locator("body")).to_contain_text("Working copy")

     # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")
    expect(page.locator("#main-content")).to_contain_text("This record has a working copy version. Click here to see it.")
    expect(page.locator("#main-content")).to_contain_text(title+" Approved")

    time.sleep(3)
    page.locator(catalogue_objects.WORKING_COPY_LINK).click()
    logging.info("Working copy record is opened successfully")
    expect(page.locator("#main-content")).to_contain_text(editTitle+" Draft")
    expect(page.locator("#main-content")).to_contain_text("This record has an approved and published version. Click here to see it.")
    
    #Approve working copy record
    common_utils.dirrectApproveRecord(editTitle)
    
    #Validate no more original copy
    time.sleep(5)
    common_utils.searchRecordInEditorBoard(title) 
    time.sleep(3)
    #expect(page.locator("body")).to_contain_text("No results found!")

    #Validate working copy record is approved
    time.sleep(3)
    common_utils.searchRecordInEditorBoard(editTitle) 
    time.sleep(3)
    expect(page.locator("body")).to_contain_text("ago · Approved")

     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)



  
    


