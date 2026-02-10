import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

@pytest.mark.test_case_ids([79426,97633,101408])
def test_service_request_abandon(page_setup) -> None:
    logging.info("Starting test_service_request_abandon")
    page = page_setup
        
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "ServiceRequestAbandon_"
    title = common_utils.createCatalogueRecordTitle(title)
    # Generate a unique title for the record
    channel = "Federal Geospatial Platform"
    # Get the userId and username from environment variables
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    username_editor_a = os.getenv("EDITOR_A_NAME")
       
    if not userId_editor_a :
        raise ValueError("Environment variables USERNAME_REVIEWER_A, USERNAME_REVIEWER_B, or USERNAME_CDO are not set")
    
    # Login
    common_utils.login(userId_editor_a)

    # Create new spatial record
    common_utils.createNewSpatialRecord(title) 
 
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")
    
    #search record in editor board
    common_utils.searchRecordInEditorBoard(title)
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details") 

    page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
    logging.info("Clicking manage record button")  
    
    #Create service request
    service_page =common_utils.createServiceRequest(page,title)
    
    # Search Service Request in the Pending Request table
    service_page.locator(portal_objects.PENDING_REQUEST_INPUT_FIELD).fill(title)
    logging.info("Filling Pending Request input field with title: %s", title) 

    # Click on the service request link to open the details
    row_locator = f"table#wb-auto-4 tr:has(td a:has-text('{title}'))"
    link_title = f"{row_locator} a:has-text('{title}')"
    service_page.locator(link_title).click()

    # Click on Abandone button
    time.sleep(5)
    service_page.once("dialog", lambda dialog: dialog.accept())
    service_page.locator(portal_objects.ABANDON_SERVICE_REQUEST_BUTTON).click()
    logging.info("Clicking abandon service request button")
    
    service_page.locator(portal_objects.SUCCESS_MESSAGE_ALERT).wait_for(state="visible")
    expect(service_page.locator(portal_objects.SUCCESS_MESSAGE_ALERT)).to_contain_text("The request was successfully abandoned")
    logging.info("The request was successfully abandoned")

    service_page.close()
    logging.info("Service request page closed")

    #Switch to catalogue tab    
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")
        
    #Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)
   
   