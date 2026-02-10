import logging
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


# @pytest.mark.skip(reason="Skipping this test during runtime due to fail")
@pytest.mark.test_case_ids([90026])
def test_abandon_validation(page_setup) -> None:
    logging.info("Starting test_abandon_validation")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    title = "AbandonRecord_Validation"
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
    
    # Abandon the publication process
    common_utils.abandonPublicationProcess(publish_page)

    # Close the publication page
    publish_page.close()

    # Close the portal page
    portal_page.close()

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)

 

