
import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

@pytest.mark.test_case_ids([79426,97633,101408])
def test_service_request(page_setup) -> None:
    logging.info("Starting test_service_request")
    page = page_setup
        
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "ServiceRequest_"
    title = common_utils.createCatalogueRecordTitle(title)
    # Generate a unique title for the record
    channel = "Federal Geospatial Platform"
    # Get the userId and username from environment variables
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    username_editor_a = os.getenv("EDITOR_A_NAME")
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")
    app_url = os.getenv("APP_URL")
    
    if not userId_reviewer_a or not userId_editor_a :
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
    service_page.close()
    logging.info("Service request page closed")

    #Switch to catalogue tab    
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")
        
    #Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)
   
   #Login as GIS Team 
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_reviewer_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")

    # Find the record and complete accept request
    # Click the "Complete Accept Service Request" button for the given title
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"Accept Service Request\"')"
    portal_page.locator(button_locator).wait_for(state="visible", timeout=10000)
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Accept Service Request' button for title: {title}")

    #Validate Accept Service Request Page
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_FORM)).to_contain_text("Mapping")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_FORM)).to_contain_text("Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Request Progress")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Accept Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Provide map service info")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Requester approval")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)

    #Accept Service Request
    portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_BUTTON).click()
    logging.info("Clicking on Accept Service Request button")

    portal_page.locator(portal_objects.SERVICE_REQUEST_DETAILS_TEXTAREA).fill("Service Request accepted successfully")
    logging.info("Filling Service Request details textarea with 'Service Request accepted successfully'")
    portal_page.locator(portal_objects.SEND_BUTTON).click()
    logging.info("Clicking on Send button to accept service request")

    # Search Service Request in the Pending Request table
    portal_page.locator(portal_objects.PENDING_REQUEST_INPUT_FIELD).fill(title)
    logging.info("Filling Pending Request input field with title: %s", title)   
    # Validate the Service Request in the Pending Request table
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('Pending "Requester approval"')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('0')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('Mapping')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('groupa editor')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('groupa editor')

    portal_page.close()
    logging.info("Portal page closed")

    # Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")        

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)

    # Login as Service Requester
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_editor_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")
    time.sleep(2)
    # Click the "Complete requester approval" button for the given title
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"Requester approval\"')"
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Requester approval' button for title: {title}")
    time.sleep(2)
    #Validate Request progress section in service request details
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Request Progress")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Provide map service info - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Requester approval")

    #Complete Requester approval
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_APPROVE_RADIO_BUTTON).click()
    logging.info("Selecting Approve radio button")
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_SUBMIT_BUTTON).click()
    logging.info("Clicking on Submit button to complete requester approval")

    #Validate Service request in Completed Request table
    portal_page.locator(portal_objects.COMPLETED_REQUEST_INPUT_FIELD).fill(title)
    logging.info("Filling Completed Request input field with title: %s", title)
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_COMPLETED_TABLE)).to_contain_text('Completed')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_COMPLETED_TABLE)).to_contain_text('Mapping')
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_COMPLETED_TABLE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_COMPLETED_TABLE)).to_contain_text('groupa editor')

    #Validate completed service request details
    
    # Click the "Complete Accept Service Request" button for the given title
    row_locator = f"table#wb-auto-5 tr:has(td a:has-text('{title}'))"
    link_title = f"{row_locator} a:has-text('{title}')"
    portal_page.locator(link_title).click()
    logging.info(f"Clicked on 'Completed service request for title: {title}")


    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Request Progress")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Provide map service info - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Requester approval - approved")
    
    # Close the portal page
    portal_page.close()
    logging.info("Portal page closed")

    # Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)
    logging.info("test_service_request completed successfully")