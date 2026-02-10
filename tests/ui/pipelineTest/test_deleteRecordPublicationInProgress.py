import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


# @pytest.mark.skip(reason="Skipping this test during runtime due to fail")
def test_delete_record_publication_inProgress(page_setup) -> None:
    logging.info("test_delete_record_publication_inProgress started")   
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    title = "test_delete_record_publication_inProgress"
    title = common_utils.createCatalogueRecordTitle(title)
    channel = "Federal Geospatial Platform"

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

    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Search the record and go to record details
    common_utils.searchRecordInPortal(portal_page,title)
    portal_page.locator(portal_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record link to go to record details")
    
    # Select the channel
    publish_page = common_utils.selectPublicationChannel(portal_page, channel)

    #Confirm the details in publication process
    common_utils.confirmDetailsInPublicationProcess(publish_page)

    # Release the publication process
    common_utils.releaseProcess(publish_page)

    # start Validation process
    time.sleep(2)
    #publish_page.locator(portal_objects.START_VALIDATION_BUTTON).click()
    publish_page.get_by_role("button", name="Start Validation and Draft Upload").click()
    logging.info("Clicking start validation and draft upload button")
    time.sleep(5)
    # Wait for the spinner to disappear
    publish_page.locator("#loader").wait_for(state="hidden")
    logging.info("Waiting for the loader to disappear")

    # Close the publication page
    publish_page.close()
    logging.info("Publication page closed")

    # Close the portal page
    portal_page.close()
    logging.info("Portal page closed")

    #Switch to catalogue tab    
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    #search record in editor board   
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")
    
    # Delete the record
    time.sleep(2)
    deleteMessage= "Cannot delete this catalogue entry;  there are publication(s) in progress associated with this catalogue entry:"
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator(catalogue_objects.DELETE_RECORD_BUTTON).click()
    logging.info("Clicking delete record button")    
    expect(page.get_by_role("alert")).to_contain_text(deleteMessage)
       
     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
    
    
       
    


