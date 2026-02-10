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
@pytest.mark.test_case_ids([246909])
def test_notification_testing_catalogue_only(page_setup) -> None:
    global title
    logging.info("Starting test_publish_record_to_FGP_withResources")
    page = page_setup    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "Notification_Testing_"
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
        "content_type_eng": "Application"
    }     
   # common_utils.add_online_resource(data_public)
            
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
   # common_utils.add_online_resource(data_private)
    
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
        "file_name": "thumbnail.png"        
    }
   # common_utils.add_thumbnail(data_thumbnail)

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
    # expect(page.locator("#main-content")).to_contain_text(data_public["file_name"])
    # expect(page.locator("#main-content")).to_contain_text(data_private["file_name"])
    common_utils.submit_for_review("Submit_for_reviewer ")
    common_utils.reject_approval_submission("Rejected_record")
    common_utils.submit_for_review("Submit_for_reviewer ")
    common_utils.approve_metadata("approved_record")
    
    common_utils.publishRecordInternally()
    common_utils.unpublish_record()
    common_utils.retire_metadata("Ahmed _retire_test")
    common_utils.restore_record_to_draft("Ahmed_REstore")

    logging.info("Completed full record workflow")
