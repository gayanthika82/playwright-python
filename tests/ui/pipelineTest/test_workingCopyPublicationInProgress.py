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
@pytest.mark.test_case_ids([99125])
def test_workingCopyPublicationInProgress_step1(page_setup) -> None:
    global title
    logging.info("Starting test_publish_record_to_FGP_withResources")
    page = page_setup    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "PublishRecordToFGP_"
    title = common_utils.createCatalogueRecordTitle(title)
    editTitle = "Edit Approve Working Copy Title"
    editTitle = common_utils.createCatalogueRecordTitle(editTitle)
    # Generate a unique title for the record
    now = datetime.datetime.now()
    extendImage = "PublishRecordToFGPwithResources_" + now.strftime("%Y-%m-%d %H:%M:")
    channel = "Federal Geospatial Platform"
    # Get the userId and username from environment variables
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")   
    if not userId_reviewer_a:
        raise ValueError("Environment variables USERNAME_REVIEWER_A, is not set.")
    
    # Login
    common_utils.login(userId_reviewer_a)
    # Create new spatial record
    common_utils.createNewSpatialRecord(title)   

    page.locator(catalogue_objects.VALIDATE_BUTTON).wait_for(state="visible", timeout=10000)
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    time.sleep(2)
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")
   
    #search record in editor board
    common_utils.searchRecordInEditorBoard(title)
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")   
    
    #Validate details of the record
    expect(page.locator("#main-content")).to_contain_text(title)   
    
    #Approve and publish record internally
    common_utils.dirrectApproveRecord(title)
    common_utils.publishRecordInternally()       
    
    #Publish record externally    
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

    # Search record in editor board
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")        
    
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
    expect(page.locator("#main-content")).to_contain_text(title+" Approved")

    page.locator(catalogue_objects.WORKING_COPY_LINK).wait_for(state="visible", timeout=9000)
    page.locator(catalogue_objects.WORKING_COPY_LINK).click()
    logging.info("Working copy record is opened successfully")
    expect(page.locator("#main-content")).to_contain_text(editTitle+" Draft")
    expect(page.locator("#main-content")).to_contain_text("This record has an approved and published version. Click here to see it.")
    
    #Approve working copy record
    common_utils.dirrectApproveRecord(editTitle)
        
    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)

@pytest.mark.test_case_ids([99125])
@pytest.mark.dependency(depends=["test_workingCopyPublicationInProgress_step1"])
def test_workingCopyPublicationInProgress_step2(page_setup) -> None:     
    #Login as Business Data Trustee 
    global title
    userId_reviewer_b = os.getenv("USERNAME_REVIEWER_B")
    username_reviewer_b = os.getenv("REVIEWER_B_NAME")
    logging.info("Start testing 'test_publish_to_FGP_approve_by_BDT'")
    page = page_setup
    common_utils = CommonUtils(page)
    common_utils.login(userId_reviewer_b)    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    #Go to Approve record page
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).wait_for(state="visible", timeout=90000)
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button")
    portal_page.locator(portal_objects.DATA_PUBLISHING_OPTION).wait_for(state="visible", timeout=180000) 
    portal_page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
    logging.info("Clicking on Data Publishing option")
    # Wait for the page to load completely              
    expect(portal_page).to_have_title("EDH Publishing - Dashboard", timeout=180000)  # Timeout is 180 seconds
    logging.info("Validated that the page title is 'EDH Publishing - Dashboard'")
    row_locator = portal_page.locator(f'tr:has(td.force-wrap:has-text("{title}"))') 
    row_locator.wait_for(state="visible", timeout=150000) 
    row_locator.locator('td:nth-child(1) a').click()
    portal_page.locator(portal_objects.APPROVE_RADIO_BUTTON).wait_for(state="visible", timeout=90000)
    
    # Validate the presence of the warning alert
    expect(portal_page.locator(portal_objects.CATALOGUE_MODIFIED_WARNING)).to_be_visible()
    logging.info("Validated the presence of the warning alert about catalogue entry modification")

    # Close the portal page
    portal_page.close() 
    logging.info("Portal page closed")

    # Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_b)

    
   

