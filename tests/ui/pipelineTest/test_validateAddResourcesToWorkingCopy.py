import logging
import time
import pytest
from objects_repository import catalogue_objects, portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

title=None
editTitle=None

@pytest.mark.test_case_ids([88125])
def test_validateAddResourcesToWorkingCopy(page_setup) -> None:
    logging.info("Starting test_validateAddResourcesToWorkingCopy")
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
    time.sleep(5)
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

    # Search record in editor board
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details")   
    page.get_by_role("link", name="Edit").click()
    logging.info("Clicking on edit record button")
    time.sleep(2)

    # Add public resource    
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
    common_utils.add_online_resource(data_public)
    
    # Add thumbnail  
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
    common_utils.add_thumbnail(data_thumbnail)    
    
    
    page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
    logging.info("Clearing title textbox")
    page.locator(catalogue_objects.TITLE_TEXTBOX).fill(editTitle)
    logging.info("Clicking on add title button")
    page.locator(catalogue_objects.VALIDATE_BUTTON).click()
    logging.info("Clicking validate button")
    page.locator(catalogue_objects.SAVE_AND_CLOSE_BUTTON).click()
    logging.info("Clicking save and close button")

    # Search the original record in editor board
    common_utils.searchRecordInEditorBoard(title)

    # Go to record details
    page.locator(catalogue_objects.RECORD_LINK_BY_TITLE.format(title=title)).click()
    logging.info("Clicking on record title link to go to record details") 

    # Validate no resource and thumbnail
    expect(page.locator("#main-content")).to_contain_text(title)  
    expect(page.locator("#main-content")).not_to_contain_text(data_public["resource_name_eng"])
    expect(page.locator(catalogue_objects.THUMBNAIL_IMAGE)).not_to_be_visible()
    logging.info("Validated the presence of the thumbnail image with alt='thumbnail_en.png'")

    # Go to working copy
    page.locator(catalogue_objects.WORKING_COPY_LINK).click()
    logging.info("Working copy record is opened successfully")
    
    #Validate no resource and thumbnail
    expect(page.locator("#main-content")).to_contain_text(editTitle+" Draft")  
    expect(page.locator("#main-content")).to_contain_text(data_public["resource_name_eng"])
    expect(page.locator(catalogue_objects.THUMBNAIL_IMAGE)).to_be_visible()
    logging.info("Validated the presence of the thumbnail image with alt='thumbnail_en.png'")

    # Logout from catalogue
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_reviewer_a)

