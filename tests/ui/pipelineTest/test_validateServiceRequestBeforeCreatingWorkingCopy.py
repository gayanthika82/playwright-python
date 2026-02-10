import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

title=None
editTitle=None

@pytest.mark.dependency()
@pytest.mark.test_case_ids([88142])
def test_validateServiceRequestBeforeCreatingWorkingCopy_step1(page_setup) -> None:
    logging.info("Starting test_validateServiceRequestBeforeCreatingWorkingCopy_step1")
    page = page_setup
    global title
    global editTitle
    
    # Create record title
    common_utils = CommonUtils(page)
    title = "WorkingCopyWithServiceRequest"
    title = common_utils.createCatalogueRecordTitle(title)
    editTitle = "Edit WorkingCopyWithServiceRequest"
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

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)



@pytest.mark.test_case_ids([88142])
@pytest.mark.dependency(depends=["test_validateServiceRequestBeforeCreatingWorkingCopy_step1"])
def test_validateServiceRequestBeforeCreatingWorkingCopy_step2(page_setup) -> None:
    logging.info("Starting test_validateServiceRequestBeforeCreatingWorkingCopy_step2")
    page = page_setup
    common_utils = CommonUtils(page)

    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    username_editor_a = os.getenv("EDITOR_A_NAME")

    if not userId_editor_a:
        raise ValueError("USERNAME_REVIEWER_A environment variable is not set")

    # Login
    common_utils.login(userId_editor_a)

    #Go to portal home page
    portal_page = common_utils.goToPortalHomePage()
    time.sleep(2)  # Wait for the page to load
    #Search the record in the portal
    common_utils.searchRecordInPortal(portal_page,title)
    #Open the record details from portal
    portal_page.locator(portal_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details from portal")
    time.sleep(3)
    #Click on Initial service request button
    portal_page.locator(portal_objects.INITIAL_SERVICE_REQUEST_BUTTON).click()
    logging.info("Clicking on initial service request button from portal")
    # Click on Map Service Request option
    portal_page.locator(portal_objects.MAP_SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Map Service Request option from portal")
    # Add message in service request form
    portal_page.locator(portal_objects.SERVICE_REQUEST_MESSAGE_TEXTAREA).fill("Creating service request for working copy record")
    logging.info("Filling message in service request form from portal")
    # Submit service request
    portal_page.locator(portal_objects.SUBMIT_SERVICE_REQUEST_BUTTON).click()
    logging.info("Submitting service request from portal")

    #Switch to catalogue tab    
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)


@pytest.mark.test_case_ids([88142])
@pytest.mark.dependency(depends=["test_validateServiceRequestBeforeCreatingWorkingCopy_step2"])
def test_validateServiceRequestBeforeCreatingWorkingCopy_step3(page_setup) -> None:
    logging.info("Starting test_validateServiceRequestBeforeCreatingWorkingCopy_step3")
    page = page_setup
    common_utils = CommonUtils(page)
    # Get the userId and username from environment variables
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")

    if not userId_reviewer_a:
        raise ValueError("USERNAME_REVIEWER_A environment variable is not set")

    # Login
    common_utils.login(userId_reviewer_a)
    # Search record in editor board
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")        
    
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

    #Open working copy record
    time.sleep(3)
    page.locator(catalogue_objects.WORKING_COPY_LINK).click()
    logging.info("Working copy record is opened successfully")
    expect(page.locator("#main-content")).to_contain_text(editTitle+" Draft")
    expect(page.locator("#main-content")).to_contain_text("This record has an approved and published version. Click here to see it.")
    
    #Approve working copy record
    common_utils.dirrectApproveRecord(editTitle)
    
    # Delete the record
    time.sleep(2)
    error_message_title = "An error occurred while updating status"
    error_message_firstPart = "At least one active service request currently exists for this catalogue entry "
    error_message_secondPart = "Cannot approve this catalogue entry at this time."
    page.once("dialog", lambda dialog: dialog.accept())
       
    expect(page.get_by_role("alert")).to_contain_text(error_message_title)
    expect(page.get_by_role("alert")).to_contain_text(error_message_firstPart)
    expect(page.get_by_role("alert")).to_contain_text(error_message_secondPart)
    time.sleep(1)
    page.locator(catalogue_objects.CLOSE_DELETE_POPUP_BUTTON).click()
    logging.info("Clicking close button")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)