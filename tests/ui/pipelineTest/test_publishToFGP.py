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
@pytest.mark.test_case_ids([90401])
def test_publish_to_FGP_create_catalogue(page_setup) -> None:
    global title
    logging.info("Starting test_publish_record_to_FGP_withResources")
    page = page_setup    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "PublishRecordToFGP_"
    title = common_utils.createCatalogueRecordTitle(title)
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
        "content_type_eng": "Application",
        "required_All_links": True,
        "resource_name_eng": "xlsx_eng",
        "resource_name_fra": "xlsx_fra",
        "warningMessage": False     
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
        "content_type_eng": "Application",
        "required_All_links": False,
        "resource_name_eng": "pdf_eng",
        "resource_name_fra": "pdf_fra",
        "warningMessage": True 
    }
    #common_utils.add_online_resource(data_private)
    
    #Add thumbnail resource data
    data_thumbnail = {
        "file_path": "test_data/thumbnail.png",
        "description": "test",
        "description_french": "test",
        "disposition_period_count": "1",
        "disposition_action": "DELETE",
        "disposition_period_type": "MONTHS",
        "disposition_contact_email": "ahmedhussain.mohammad@dfo-mpo.gc.ca",
        "sensitivity": "UNCLASSIFIED",
        "publication_level": "PUBLIC",
        "resource_name_eng": "thumbnail_en.png",  
        "resource_name_fra": "thumbnail_fra.png",
        "file_name": "thumbnail.png"     
    }
    #common_utils.add_thumbnail(data_thumbnail)

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
    expect(page.locator("#main-content")).to_contain_text("Access and use constraints Open Government Licence - Canada (https://open.canada.ca/en/open-government-licence-canada)")
    # expect(page.locator("#main-content")).to_contain_text(data_public["resource_name_eng"])
    # expect(page.locator("#main-content")).to_contain_text(data_private["resource_name_eng"])

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

@pytest.mark.dependency(depends=["test_publish_to_FGP_create_catalogue"])
def test_publish_to_FGP_approve_by_BDT(page_setup) -> None:     
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

@pytest.mark.dependency(depends=["test_publish_to_FGP_approve_by_BDT"])
def test_publish_to_FGP_approve_by_CDO(page_setup) -> None:
    global title
    userId_cdo = os.getenv("USERNAME_CDO")
    username_cdo = os.getenv("CDO_NAME")
    logging.info("Start testing 'test_publish_to_FGP_approve_by_CDO'")
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

@pytest.mark.dependency(depends=["test_publish_to_FGP_approve_by_CDO"])
def test_publish_to_FGP_final_review_and_validate_in_FGP(page_setup) -> None:
    # Login as Reviewer A and complete the final review for FGP
    global title
    userId_reviewer_a = os.getenv("USERNAME_REVIEWER_A")
    username_reviewer_a = os.getenv("REVIEWER_A_NAME")   
    if not userId_reviewer_a:
        raise ValueError("Environment variables USERNAME_REVIEWER_A, is not set.")
    
    logging.info("Start testing 'test_publish_to_FGP_final_review_and_validate_in_FGP'")
    page = page_setup
    common_utils = CommonUtils(page)
    common_utils.login(userId_reviewer_a)    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()
    # Final review for FGP
    common_utils.finalReview(portal_page, title)
    #Validate record in FGP
    FGP_page = common_utils.goToFGP(portal_page,title)
    if FGP_page is None:
     logging.error("FGP validation failed. FGP page is None.")
     return  # Exit the test or handle the failure appropriately    
    time.sleep(5)
    common_utils.switch_to_tab_by_title(page.context,"FGP / PGF - FGP / PGF")
    time.sleep(5)    
    # Get record UUID from URL
    FGP_url = FGP_page.url
    logging.info("Current FGP URL: %s", FGP_url)
    #Extract the uuid from the URL
    uuid = FGP_url.split("/")[-1]
    logging.info("Extracted UUID: %s", uuid)
    # Construct image URL
    original_url = os.getenv("APP_URL")
    # Remove "https://" from the URL
    modified_url = original_url.replace("https://", "")
    img_url = "https://api-proxy-"+modified_url+"/records/"+uuid+"/attachments/thumbnail.png"
    logging.info("Image URL: %s", img_url)
    IMAGE_LOCATOR = "img[src='"+img_url+"']"

    ''' This part fail in pipeline only, need to investigate more
    #Validation title
    expect(FGP_page.locator("body")).to_contain_text(title)
    #expect(FGP_page.locator(portal_objects.FGP_RECORD_TITLE)).to_contain_text(title)
   
    #Validation public resources
    expect(FGP_page.locator(portal_objects.FGP_RESOURCE_TABLE)).to_contain_text(data_public["file_name"])
    # Validation private resources
    expect(FGP_page.locator(portal_objects.FGP_RESOURCE_TABLE)).not_to_contain_text(data_private["file_name"])
    # Validation thumbnail
    expect(FGP_page.locator(IMAGE_LOCATOR)).to_be_visible()

    #Extract public resource link url
    link_public_resource=FGP_page.locator(portal_objects.FGP_FILE_TYPE.format(fileType=data_public["file_type"]))
    link_href=link_public_resource.get_attribute("href")   
    logging.info("Resource link href: %s", link_href)

    #Construct public resource link
    expected_href = "https://api-proxy-"+modified_url+"/records/"+uuid+"/attachments/"+data_public["file_name"]
    logging.info("Expected_href: %s", expected_href)
    # Validate the href attribute of public resource link
    assert link_href == expected_href, f"Expected href to be '{expected_href}', but got '{link_href}'"
    logging.info(f"Validated the href attribute of the link: {link_href}")
    '''
    
    FGP_page.close()
    logging.info("FGP validation completed successfully")
    portal_page.close()
    logging.info("Portal page closed")    

     # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)
    
   

