
import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

title=None
@pytest.mark.dependency()
@pytest.mark.test_case_ids([90423])
def test_publish_to_OpenInformation_create_catalogue(page_setup) -> None:
    global title
    logging.info("Starting test: test_publish_to_OpenInformation_create_catalogue")
    page = page_setup
    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "PublishToOpenInformation_"
    title = common_utils.createCatalogueRecordTitle(title)
    channel="Open Information"
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
    common_utils.createNewNoneSpatialRecord(title) 
  
   # Add public resource data
     # Add public resource data
    data_public = {
        "file_path": "test_data/Largefile_excel.xlsx",
        "description": "test",
        "description_french": "test",
        "disposition_period_count": "1",
        "disposition_action": "DELETE",
        "disposition_period_type": "MONTHS",
        "disposition_contact_email": "ahmedhussain.mohammad@dfo-mpo.gc.ca",
        "sensitivity": "UNCLASSIFIED",
        "publication_level": "PUBLIC",
        "file_name": "Largefile_excel.xlsx",
        "protocol": "HTTPS",
        "file_type": "XLSX",
        "language": "eng",
        "function": "RI_375",
        "content_type_eng": "Application"
    }     
    #common_utils.add_online_resource(data_public)
            
    #Add internal resource data
    data_private = {
        "file_path": "test_data/map.pdf",
        "description": "test",
        "description_french": "test",
        "disposition_period_count": "1",
        "disposition_action": "DELETE",
        "disposition_period_type": "MONTHS",
        "disposition_contact_email": "ahmedhussain.mohammad@dfo-mpo.gc.ca",
        "sensitivity": "UNCLASSIFIED",
        "publication_level": "INTERNAL",
        "file_name": "map.pdf",
        "protocol": "HTTPS",
        "file_type": "PDF",
        "language": "eng",
        "function": "RI_375",
        "content_type_eng": "Application"
    }
    #common_utils.add_online_resource(data_private)

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
    # expect(page.locator("#main-content")).to_contain_text(data_public["file_name"])
    # expect(page.locator("#main-content")).to_contain_text(data_private["file_name"])  
    
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

@pytest.mark.dependency(depends=["test_publish_to_OpenInformation_create_catalogue"])
def test_publish_to_OpenInformation_approve_by_BDT(page_setup) -> None:     
    #Login as Business Data Trustee 
    global title
    userId_reviewer_b = os.getenv("USERNAME_REVIEWER_B")
    username_reviewer_b = os.getenv("REVIEWER_B_NAME")
    logging.info("Start testing 'test_publish_to_OpenInformation_approve_by_BDT'")
    page = page_setup
    common_utils = CommonUtils(page)
    common_utils.login(userId_reviewer_b)     
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
    logging.info("User %s logged out successfully", username_reviewer_b)

@pytest.mark.dependency(depends=["test_publish_to_OpenInformation_approve_by_BDT"])
def test_publish_to_OpenInformation_approve_by_CDO(page_setup) -> None:
    global title
    userId_cdo = os.getenv("USERNAME_CDO")
    username_cdo = os.getenv("CDO_NAME")
    logging.info("Start testing 'test_publish_to_OpenInformation_approve_by_CDO'")
    page = page_setup
    common_utils = CommonUtils(page)
    #Login as Chief Digital Officer 
    common_utils.login(userId_cdo)     
    
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

@pytest.mark.dependency(depends=["test_publish_to_OpenInformation_approve_by_CDO"])
def test_publish_to_OpenInformation_final_review(page_setup) -> None:
    # Login as Reviewer A and complete the final review for FGP
    global title
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")   
    if not userId_reviewer_a:
        raise ValueError("Environment variables USERNAME_REVIEWER_A, is not set.")
    
    logging.info("Start testing 'test_publish_to_OpenInformation_final_review'")
    page = page_setup
    common_utils = CommonUtils(page)
    common_utils.login(userId_reviewer_a)
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Final review for FGP
    common_utils.finalReview(portal_page, title)
    time.sleep(10) # Wait for the final review to complete
    
    # Verify Publication
    time.sleep(2) # Wait for the portal to load
    portal_page.locator(portal_objects.DASHBOARD_LINK).click()
    logging.info("Clicking on Dashboard link")
    time.sleep(2) # Wait for the portal to load
    row_locator= portal_page.locator(portal_objects.ROW_LOCATOR_TEMPLATE.format(title=title))
    row_locator.locator('td:nth-child(1) a').click()
    logging.info("Clicking on record title link to go to record details")
    time.sleep(3) # Wait for the record details to load
    expect(portal_page.locator(portal_objects.VERIFY_PUBLICATION_PAGE_HEADER)).to_contain_text("Verify Publication")
    expect(portal_page.locator(portal_objects.VERIFY_PUBLICATION_PAGE_P1)).to_contain_text("There is a delay from when the catalogue record is published to Open Government registry and when the catalogue record is available on their public site.") 
    expect(portal_page.locator(portal_objects.VERIFY_PUBLICATION_PAGE_P1)).to_contain_text("In this step, a verification is performed on the public Open Government site to ensure that the most recent changes are available online.")
    expect(portal_page.locator(portal_objects.VERIFY_PUBLICATION_PAGE_P1)).to_contain_text("Use the button below to perform the verification process.")
    portal_page.locator(portal_objects.VERIFY_PUBLICATION_BUTTON).click()
    logging.info("Clicking on Verify Publication button")       
    expect(portal_page.locator(portal_objects.VERIFY_PUBLICATION_VERIFICATION)).to_contain_text("Unable to complete the publication process due to the following verification errors:Not yet published to the Open Government public sitePlease try again later.")
    logging.info("Verification process completed with expected errors")

    #Close portal page
    portal_page.close()
    
     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
    
   

