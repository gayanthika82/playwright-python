import datetime
import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils


#@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.test_case_ids([136326,136357])
def test_reprocess_publication(page_setup) -> None:
    logging.info("Starting test_reprocess_publication")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "ReprocessPublication_"
    title = common_utils.createCatalogueRecordTitle(title)
    # Generate a unique title for the record
    channel = "Federal Geospatial Platform"
    # Get the userId and username from environment variables
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")
    app_url = os.getenv("APP_URL")
    userId_reviewer_b = os.getenv("USERNAME_REVIEWER_B")
    username_reviewer_b = os.getenv("REVIEWER_B_NAME")
    userId_cdo = os.getenv("USERNAME_CDO")
    username_cdo = os.getenv("CDO_NAME")
    if not userId_reviewer_a or not userId_reviewer_b or not userId_cdo:
        raise ValueError("Environment variables USERNAME_REVIEWER_A, USERNAME_REVIEWER_B, or USERNAME_CDO are not set")
    
    # Login
    common_utils.login(userId_reviewer_a)

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
    
    #Validate details of the record
    expect(page.locator("#main-content")).to_contain_text(title)   
    expect(page.locator("#main-content")).to_contain_text("Access and use constraints Open Government Licence - Canada (https://open.canada.ca/en/open-government-licence-canada)")
    
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
        
    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
      
    #Login as Business Data Trustee 
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_reviewer_b)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()
    time.sleep(3)  # Wait for the new tab to open

    #Not approving record
    common_utils.notApproveRecord(portal_page,username_reviewer_b, title)
    
    # Close the portal page
    portal_page.close() 
    logging.info("Portal page closed")

    #Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_b)

    #Login as Reviewer and restart the publication
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_reviewer_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    #Restart publication process
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking restart publication button")
    time.sleep(1)
    portal_page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
    logging.info("Clicking data publishing option")
    portal_page.locator(portal_objects.ROW_LOCATOR_TEMPLATE.format(title=title)).locator("td:nth-child(1) a").wait_for(state="visible", timeout=10000)
    portal_page.locator(portal_objects.ROW_LOCATOR_TEMPLATE.format(title=title)).locator("td:nth-child(1) a").click()
    portal_page.get_by_role("button", name="Restart Publication Process").wait_for(state="visible", timeout=10000)
    #portal_page.locator(portal_objects.RESTART_PUBLICATION_BUTTON).click()
    portal_page.get_by_role("button", name="Restart Publication Process").click()
    logging.info("Clicking restart publication process button")
    portal_page.locator(portal_objects.CONFIRM_AND_CONTINUE_BUTTON).wait_for(state="visible", timeout=10000)
    portal_page.locator(portal_objects.CONFIRM_AND_CONTINUE_BUTTON).click()
    common_utils.releaseProcess(portal_page)

    # start Validation process
    time.sleep(2)
    #publish_page.locator(portal_objects.START_VALIDATION_BUTTON).click()
    portal_page.get_by_role("button", name="Start Validation and Draft Upload").click()
    logging.info("Clicking start validation and draft upload button")
    time.sleep(5)
    
    # Close the portal page
    portal_page.close()
    logging.info("Portal page closed")

    #Switch to catalogue tab    
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")
        
    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
  







'''
    #Login as Chief Digital Officer 
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_cdo)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    #Approve record
    common_utils.approveRecordInPortal(portal_page, title)
    
    # Close the portal page
    portal_page.close() 
    logging.info("Portal page closed")

    #Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_cdo)

    # Login as Reviewer A and complete the final review for FGP
    common_utils.navigateToUrl(app_url)
    common_utils.loginwithoutAcceptButton(userId_reviewer_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Final review for FGP
    common_utils.finalReview(portal_page, title)

    #Validate record in FGP
    FGP_page = common_utils.FGPValidation(portal_page,title)
    if FGP_page is None:
     logging.error("FGP validation failed. FGP page is None.")
     return  # Exit the test or handle the failure appropriately

    FGP_page.close()
    logging.info("FGP validation completed successfully")
    portal_page.close()
    logging.info("Portal page closed")    

     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
'''    
   

