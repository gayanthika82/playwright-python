import datetime
import time
from playwright.sync_api import Page, expect
import logging
from dotenv import load_dotenv
import os

from objects_repository import catalogue_objects, login_objects, portal_objects

class CommonUtils:
    """Common utility functions for tests"""
    def __init__(self, page: Page):
        self.page = page        
        self.password = os.getenv("TEST_USER_PASSWORD")

    def login(self, username: str):
        self.page.locator(login_objects.USERNAME_INPUT).click()
        self.page.locator(login_objects.USERNAME_INPUT).fill(username)
        logging.info("Entering username: %s", username)
        self.page.locator(login_objects.PASSWORD_INPUT).click()
        self.page.locator(login_objects.PASSWORD_INPUT).fill(self.password)
        logging.info("Entering password for user: %s", username)
        self.page.locator(login_objects.SIGN_IN_BUTTON).click()
        logging.info("Clicking sign in button")
        self.page.locator(login_objects.ACCEPT_BUTTON).click()
        logging.info("Clicking accept button")            
        expect(self.page).to_have_title("Catalogue (Test)")
        logging.info("Login is successful for user: %s", username)

    # Catalogue login function without accept button
    def loginwithoutAcceptButton(self, username: str):
        self.page.locator(login_objects.USERNAME_INPUT).click()
        self.page.locator(login_objects.USERNAME_INPUT).fill(username)
        logging.info("Entering username: %s", username)
        self.page.locator(login_objects.PASSWORD_INPUT).click()
        self.page.locator(login_objects.PASSWORD_INPUT).fill(self.password)
        logging.info("Entering password for user: %s", username)
        self.page.locator(login_objects.SIGN_IN_BUTTON).click()
        logging.info("Clicking sign in button")
        expect(self.page).to_have_title("Catalogue (Test)")
        logging.info("Login is successful for user: %s", username)

    # Catalogue logout function
    def catalogueLogout(self):
        time.sleep(3)
        self.page.locator(catalogue_objects.USER_INFO_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(catalogue_objects.USER_INFO_BUTTON).click()
        logging.info("Clicking user info button")
        time.sleep(3)
        self.page.locator(catalogue_objects.SIGN_OUT_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(catalogue_objects.SIGN_OUT_BUTTON).click()
        logging.info("Clicking sign out button")
        time.sleep(2)
    
    # Create catalogue record title
    def createCatalogueRecordTitle(self, title: str):
        now = datetime.datetime.now()
        updatedTitle = title + now.strftime("%Y-%m-%d %H:%M:%S")
        return updatedTitle
    
    # Create unique number
    def createUniqueNumber(self):
        now = datetime.datetime.now()
        uniqueNumber = now.strftime("%Y%m%d%H%M%S")
        return uniqueNumber
    

    # Add spatial record function
    def createNewSpatialRecord(self, title: str):    
        self.page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        logging.info("Clicking contribute menu")
        self.page.locator(catalogue_objects.ADD_NEW_RECORD_OPTION).click()
        logging.info("Clicking add new record option")
        self.page.locator(catalogue_objects.DATASET).click()
        logging.info("Clicking dataset option")
        self.page.locator(catalogue_objects.TEMPLATE_A).click()
        logging.info("Clicking template A option")
        self.page.locator(catalogue_objects.GROUP_DDL_A_OPTION).select_option("a")
        logging.info("Selecting group option a")
        self.page.locator(catalogue_objects.CREATE_BUTTON).click()
        logging.info("Clicking create button")
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).fill(title)
        logging.info("Entering title: %s", title)

    # Add none spatial record function
    def createNewNoneSpatialRecord(self, title: str):
        self.page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        logging.info("Clicking contribute menu")
        self.page.locator(catalogue_objects.ADD_NEW_RECORD_OPTION).click()
        logging.info("Clicking add new record option")
        self.page.locator(catalogue_objects.NON_GEOGRAPHIC_DATASET).click()
        logging.info("Clicking dataset option")
        self.page.locator(catalogue_objects.TEMPLATE_B).click()
        logging.info("Clicking template A option")
        self.page.locator(catalogue_objects.GROUP_DDL_A_OPTION).select_option("a")
        logging.info("Selecting group option a")
        self.page.locator(catalogue_objects.CREATE_BUTTON).click()
        logging.info("Clicking create button")
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).fill(title)
        logging.info("Entering title: %s", title)
    

    # Add none spatial record function
    def createNewNoneSpatialRecord(self, title: str):
        self.page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        logging.info("Clicking contribute menu")
        self.page.locator(catalogue_objects.ADD_NEW_RECORD_OPTION).click()
        logging.info("Clicking add new record option")
        self.page.locator(catalogue_objects.NON_GEOGRAPHIC_DATASET).click()
        logging.info("Clicking dataset option")
        self.page.locator(catalogue_objects.TEMPLATE_B).click()
        logging.info("Clicking template A option")
        self.page.locator(catalogue_objects.GROUP_DDL_A_OPTION).select_option("a")
        logging.info("Selecting group option a")
        self.page.locator(catalogue_objects.CREATE_BUTTON).click()
        logging.info("Clicking create button")
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).clear()
        self.page.locator(catalogue_objects.TITLE_TEXTBOX).fill(title)
        logging.info("Entering title: %s", title)
    
    # Search the record in editor board
    def searchRecordInEditorBoard(self, title: str):
        self.page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        logging.info("Clicking on contribute menu")
        self.page.locator(catalogue_objects.EDITOR_BOARD_OPTION).click()
        logging.info("Navigating to Editor Board")
        self.page.get_by_role("textbox", name="Search").click()
        logging.info("Clicking search textbox")
        self.page.get_by_role("textbox", name="Search").fill(title)            
        logging.info("Filling search textbox with title: %s", title)
        time.sleep(1)
        self.page.locator(catalogue_objects.SEARCH_BUTTON).click()
        logging.info("Clicking search button")
        time.sleep(3)  # Wait for search results to load
    
    # Approve the record directly
    def dirrectApproveRecord(self, title: str):
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        logging.info("Clicking manage record button")
        time.sleep(2)
        self.page.locator(catalogue_objects.DIRECT_APPROVE_OPTION).click()
        logging.info("Clicking directly approve option")
        time.sleep(2)
        self.page.locator(catalogue_objects.DIRECTLY_APPROVE_MESSAGE_TEXTBOX).fill("Approve record")
        logging.info("Filling approval message textbox")
        time.sleep(2)
        self.page.locator(catalogue_objects.DIRECT_APPROVE_BUTTON).click()
        logging.info("Clicking approve button")
        time.sleep(2)

    # Publish the record internally
    def publishRecordInternally(self):
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).wait_for(state="visible", timeout=10000)
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        logging.info("Clicking manage record button")
        time.sleep(2)
        self.page.locator(catalogue_objects.PUBLISH_OPTION).click()
        logging.info("Clicking publish option")
        time.sleep(2)

    def unpublish_record(self):
        """Unpublish the record"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.UNPUBLISH_LINK).click()
        time.sleep(2)
        logging.info("Unpublished record")
    
    def retire_metadata(self, message: str):
        """Retire metadata with a message"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.RETIRE_METADATA_LINK).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).fill(message)
        self.page.locator(catalogue_objects.RETIRE_BUTTON).click()
        logging.info(f"Retired metadata with message: {message}")
    
    def restore_record_to_draft(self, message: str):
        """Restore record to draft with a message"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.RESTORE_TO_DRAFT_LINK).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).fill(message)
        self.page.locator(catalogue_objects.SUBMIT_BUTTON).click()
        logging.info(f"Restored record to draft with message: {message}")
    
    def submit_for_review(self, message: str):
        """Submit record for review with a message"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.SUBMIT_FOR_REVIEW_OPTION).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).fill(message)
        self.page.locator(catalogue_objects.SUBMIT_BUTTON).click()
        logging.info(f"Submitted for review with message: {message}")
    
    def reject_approval_submission(self, message: str):
        """Reject approval submission with a message"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.REJECT_APPROVAL_SPAN).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).fill(message)
        self.page.locator(catalogue_objects.SUBMIT_BUTTON).click()
        logging.info(f"Rejected approval submission with message: {message}")
    
    def approve_metadata(self, message: str):
        """Approve metadata with a message"""
        self.page.locator(catalogue_objects.MANAGE_RECORD_BUTTON).click()
        time.sleep(2)
        self.page.locator(catalogue_objects.APPROVE_METADATA_SPAN).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).click()
        self.page.locator(catalogue_objects.MESSAGE_TEXTBOX).fill(message)
        self.page.locator(catalogue_objects.DIRECT_APPROVE_BUTTON).click()
        logging.info(f"Approved metadata with message: {message}")
    

    # Go to portal home page
    def goToPortalHomePage(self):
        time.sleep(2)
        with self.page.expect_popup() as page_info:
            self.page.locator(catalogue_objects.PORTAL_HOME_BUTTON).click()               
            portal_page = page_info.value
        logging.info("Opening portal home page in a new tab")
        portal_page.locator(portal_objects.HELP_BUTTON).wait_for(state="visible", timeout=90000)
        expect(portal_page).to_have_title("Home - EDH Portal")
        return portal_page

    # Approve record in portal
    def approveRecordInPortal(self, page, title: str):
        page.locator(portal_objects.PRODUCTS_BUTTON).wait_for(state="visible", timeout=90000)
        page.locator(portal_objects.PRODUCTS_BUTTON).click()
        logging.info("Clicking on Products button")
        page.locator(portal_objects.DATA_PUBLISHING_OPTION).wait_for(state="visible", timeout=180000) 
        page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
        logging.info("Clicking on Data Publishing option")
        # Wait for the page to load completely     
        time.sleep(20)         
        expect(page).to_have_title("EDH Publishing - Dashboard", timeout=180000)  # Timeout is 180 seconds
        logging.info("Validated that the page title is 'EDH Publishing - Dashboard'")
        time.sleep(2)
        row_locator = page.locator(f'tr:has(td.force-wrap:has-text("{title}"))') 
        row_locator.locator('td:nth-child(1) a').click()
        page.locator(portal_objects.APPROVE_RADIO_BUTTON).wait_for(state="visible", timeout=90000)
        time.sleep(2)
        page.locator(portal_objects.APPROVE_RADIO_BUTTON).click()
        logging.info("Clicking on Approve radio button to approve the record")
        time.sleep(4)
        page.locator(portal_objects.SUBMIT_BUTTON).wait_for(state="visible", timeout=90000)
        page.locator(portal_objects.SUBMIT_BUTTON).click()
        time.sleep(10)
        logging.info("Clicking on Submit button to approve the record")
        page.locator(portal_objects.EXPORT_BUTTON).nth(1).wait_for(state="visible", timeout=90000)
       
        #time.sleep(5)

    def add_online_resource(self,data: dict):
        # Click the "+ Add" button
        self.page.locator(catalogue_objects.ADD_RESOURCE_BUTTON).wait_for(state="visible", timeout=60000)
        self.page.locator(catalogue_objects.ADD_RESOURCE_BUTTON).click()
        logging.info("Clicking on add resource button")
        
        time.sleep(2)
        # Upload the file
        self.page.locator(catalogue_objects.FILE_INPUT).wait_for(state="visible", timeout=60000)
        self.page.locator(catalogue_objects.FILE_INPUT).set_input_files(data["file_path"])
        logging.info(f"Setting input files: {data['file_path']}")
        # Handle popup
        with self.page.expect_popup(timeout=90000) as popup_info:  # Increase timeout to 60 seconds
           # self.file_cell_link.click()
            self.page.locator(catalogue_objects.FILE_CELL_LINK).click()
        logging.info("File cell link clicked to open popup")
        popup_page = popup_info.value
        
        time.sleep(3)  # Wait for popup to load
        logging.info("Filling popup details")
        popup_page.locator(catalogue_objects.RESOURCE_DESCRIPTION_TEXTBOX).fill(data["description"])
        logging.info(f"Filling description: {data['description']}")
        popup_page.locator(catalogue_objects.RESOURCE_DESCRIPTION_FRENCH_TEXTBOX).fill(data["description_french"])  
        logging.info(f"Filling French description: {data['description_french']}")
        time.sleep(2)
        popup_page.locator(catalogue_objects.DISPOSITION_POLICY_LINK).click()
        logging.info("Navigating to Disposition Policy tab")
        popup_page.locator(catalogue_objects.DISPOSITION_PERIOD_COUNT_INPUT).fill(data["disposition_period_count"])
        logging.info(f"Filling disposition period count: {data['disposition_period_count']}")
        popup_page.locator(catalogue_objects.DISPOSITION_ACTION_DROPDOWN).select_option(data["disposition_action"])
        logging.info(f"Selecting disposition action: {data['disposition_action']}")
        popup_page.locator(catalogue_objects.DISPOSITION_PERIOD_TYPE_DROPDOWN).select_option(data["disposition_period_type"])
        logging.info(f"Selecting disposition period type: {data['disposition_period_type']}")
        popup_page.locator(catalogue_objects.DISPOSITION_CONTACT_EMAIL_INPUT).fill(data["disposition_contact_email"])
        logging.info(f"Filling disposition contact email: {data['disposition_contact_email']}")
        popup_page.locator(catalogue_objects.BASIC_PROPERTIES_LINK).click()
        logging.info("Navigating to Basic Properties tab")
        popup_page.locator(catalogue_objects.RESOURCE_SENSITIVITY_DROPDOWN).select_option(data["sensitivity"])
        logging.info(f"Selecting sensitivity: {data['sensitivity']}")
        popup_page.locator(catalogue_objects.PUBLICATION_LEVEL_DROPDOWN).select_option(data["publication_level"])
        logging.info(f"Selecting publication level: {data['publication_level']}")
        popup_page.locator(catalogue_objects.RESOURCE_VALIDATE_BUTTON).wait_for(state="visible", timeout=60000)
        popup_page.locator(catalogue_objects.RESOURCE_VALIDATE_BUTTON).click()
        logging.info("Clicking validate button")
        time.sleep(3)  # Wait for validation to complete
        #Validate success
        if data["warningMessage"] == False:
         expect(popup_page.locator(catalogue_objects.VALIDATION_MESSAGE)).to_contain_text("No business validation errors")
         logging.info("Validation successful")
        else:
         expect(popup_page.locator(catalogue_objects.VALIDATION_MESSAGE)).to_contain_text("Business validation warnings found")
         logging.info("Validation with warning messages")

        popup_page.locator(catalogue_objects.RESOURCE_SAVE_AND_CLOSE_BUTTON).click()
        logging.info("Clicking save and close button")
        popup_page.close()
        logging.info("Popup closed successfully")
        time.sleep(5)
        
        # Select the file link
        resource_locator = catalogue_objects.RESOURCE_LINK_BY_TITLE.format(resource_name=data["file_name"])
        self.page.locator(resource_locator).click()
        logging.info(f"Selecting file link: {data['file_name']}")
        time.sleep(2)
       
        self.page.locator(catalogue_objects.PROTOCOL_LIST).select_option(data["protocol"])
        logging.info(f"Selecting protocol: {data['protocol']}")

        #================ Create issue for autofill the resource name - 223483

        if data["required_All_links"] == True:
            self.page.locator("#gn-addonlinesrc-name-multilingual-row").get_by_role("link", name="All").click()
            logging.info("Clicking on resource name all link")
            
        self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_ENG).fill(data["resource_name_eng"])
        logging.info(f"Filling resource name: {data['resource_name_eng']}")
        time.sleep(2)
        self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_FRA).fill(data["resource_name_fra"])
        logging.info(f"Filling resource name French: {data['resource_name_fra']}")       
 
        self.page.locator(catalogue_objects.CONTENT_TYPE_INPUT_ENG).fill(data["content_type_eng"])
        contentTypeOption=catalogue_objects.CONTENT_TYPE_OPTION_ENG.format(option=data["content_type_eng"])
        self.page.locator(contentTypeOption).click()
        logging.info("Enter data for content type under Description")

        self.page.locator(catalogue_objects.FORMAT_INPUT_ENG).fill(data["file_type"])
        formatOption=catalogue_objects.FORMAT_OPTION_ENG.format(option=data["file_type"])
        self.page.locator(formatOption).first.click()
        logging.info("Enter data for format under Description")
        
        
        self.page.locator(catalogue_objects.LANGUAGE_INPUT_ENG).fill(data["language"])
        languageOption=catalogue_objects.LANGUAGE_OPTION_ENG.format(option=data["language"])
        self.page.locator(languageOption).first.click()
        logging.info("Enter data for language under Description")
        time.sleep(2)
        
        self.page.locator(catalogue_objects.FUNCTION_LIST).select_option(data["function"])
        logging.info(f"Selecting function: {data['function']}")
        time.sleep(3)
        # Add the online resource
        self.page.screenshot(path="screenshot_resource.png")
        self.page.locator(catalogue_objects.ADD_ONLINE_RESOURCE_BUTTON).click()
        logging.info("Clicking on add online resource button")
        time.sleep(3)


    def add_thumbnail(self,data: dict):
        # Click the "Add Resource" button
        self.page.locator(catalogue_objects.ADD_RESOURCE_BUTTON).click()
        logging.info("Clicking on add resource button")        
        time.sleep(2)

        # click the thumbnail button
        #self.page.get_by_role("radio", name="   Add a thumbnail").check()
        self.page.locator(catalogue_objects.ADD_THUMBNAIL_RADIO_BUTTON).check()
        logging.info("Selecting Add a thumbnail option")
        time.sleep(2)
        # Upload the file
        self.page.locator(catalogue_objects.FILE_INPUT).set_input_files(data["file_path"])
        logging.info(f"Setting input files: {data['file_path']}")

        
        # Handle popup
        with self.page.expect_popup(timeout=60000) as popup_info:  # Increase timeout to 60 seconds
             self.page.locator(catalogue_objects.FILE_CELL_LINK).click()
             logging.info("File cell link clicked to open popup")
             popup_page = popup_info.value
        
        time.sleep(3)  # Wait for popup to load
        logging.info("Filling popup details")
        popup_page.locator(catalogue_objects.RESOURCE_DESCRIPTION_TEXTBOX).fill(data["description"])
        logging.info(f"Filling description: {data['description']}")
        popup_page.locator(catalogue_objects.RESOURCE_DESCRIPTION_FRENCH_TEXTBOX).fill(data["description_french"])  
        logging.info(f"Filling French description: {data['description_french']}")
        time.sleep(2)
        popup_page.locator(catalogue_objects.DISPOSITION_POLICY_LINK).click()
        logging.info("Navigating to Disposition Policy tab")
        popup_page.locator(catalogue_objects.DISPOSITION_PERIOD_COUNT_INPUT).fill(data["disposition_period_count"])
        logging.info(f"Filling disposition period count: {data['disposition_period_count']}")
        popup_page.locator(catalogue_objects.DISPOSITION_ACTION_DROPDOWN).select_option(data["disposition_action"])
        logging.info(f"Selecting disposition action: {data['disposition_action']}")
        popup_page.locator(catalogue_objects.DISPOSITION_PERIOD_TYPE_DROPDOWN).select_option(data["disposition_period_type"])
        logging.info(f"Selecting disposition period type: {data['disposition_period_type']}")
        popup_page.locator(catalogue_objects.DISPOSITION_CONTACT_EMAIL_INPUT).fill(data["disposition_contact_email"])
        logging.info(f"Filling disposition contact email: {data['disposition_contact_email']}")
        popup_page.locator(catalogue_objects.BASIC_PROPERTIES_LINK).click()
        logging.info("Navigating to Basic Properties tab")
        popup_page.locator(catalogue_objects.RESOURCE_SENSITIVITY_DROPDOWN).select_option(data["sensitivity"])
        logging.info(f"Selecting sensitivity: {data['sensitivity']}")
        popup_page.locator(catalogue_objects.PUBLICATION_LEVEL_DROPDOWN).select_option(data["publication_level"])
        logging.info(f"Selecting publication level: {data['publication_level']}")
        popup_page.locator(catalogue_objects.RESOURCE_VALIDATE_BUTTON).click()
        logging.info("Clicking validate button")
        time.sleep(3)  # Wait for validation to complete
        expect(popup_page.locator(catalogue_objects.VALIDATION_MESSAGE)).to_contain_text("No business validation errors")
        logging.info("Validation successful")
        popup_page.locator(catalogue_objects.RESOURCE_SAVE_AND_CLOSE_BUTTON).click()
        logging.info("Clicking save and close button")
        popup_page.close()
        logging.info("Popup closed successfully")
        time.sleep(5)        
        # Select the file link
        resource_locator = catalogue_objects.RESOURCE_LINK_BY_TITLE.format(resource_name=data["file_name"])
        self.page.locator(resource_locator).click()
        logging.info(f"Selecting file link: {data['file_name']}")
        time.sleep(2)
        # Add Resource name
        self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_ENG).fill(data["resource_name_eng"])
        logging.info(f"Filling resource name: {data['resource_name_eng']}")
        time.sleep(2)
        self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_FRA).fill(data["resource_name_fra"])
        logging.info(f"Filling resource name French: {data['resource_name_fra']}") 
        # Add the online resource
        self.page.locator(catalogue_objects.ADD_ONLINE_RESOURCE_BUTTON).click()
        logging.info("Clicking on add online resource button")
        time.sleep(3) 


    def add_online_resource_map(self,data: dict):
            # Click the "+ Add" button
            self.page.locator(catalogue_objects.ADD_RESOURCE_BUTTON).click()
            logging.info("Clicking on add resource button")            
            # Click "Link an online resource"
            self.page.locator(catalogue_objects.LINK_ONLINE_RESOURCE).click()
            logging.info("Clicking on link online resource")       
            time.sleep(2)      
            
            self.page.locator(catalogue_objects.PROTOCOL_LIST).select_option(data["protocol"])
            logging.info(f"Selecting protocol: {data['protocol']}")
            self.page.locator(catalogue_objects.URL_INPUT_FIELD).fill(data["url"])
            time.sleep(3)
            logging.info(f"Entering URL: {data['url']}")
            map_path_locator=self.page.locator(catalogue_objects.URL_LINK.format(map_path=data["map_path"]))
            map_path_locator.dblclick()
            logging.info(f"Selecting map path: {data['map_path']}")
            time.sleep(3)

            if data["required_All_links"] == True:
                self.page.locator("#gn-addonlinesrc-name-multilingual-row").get_by_role("link", name="All").click()
                logging.info("Clicking on resource name all link")
            
            self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_ENG).fill(data["resource_name_eng"])
            logging.info(f"Filling resource name: {data['resource_name_eng']}")
            time.sleep(2)
            self.page.locator(catalogue_objects.RESOURCE_NAME_INPUT_FRA).fill(data["resource_name_fra"])
            logging.info(f"Filling resource name French: {data['resource_name_fra']}")                
            self.page.locator(catalogue_objects.CONTENT_TYPE_INPUT_ENG).fill(data["content_type"])
            contentTypeOption=catalogue_objects.CONTENT_TYPE_OPTION_ENG.format(option=data["content_type"])
            self.page.locator(contentTypeOption).click()
            logging.info("Enter data for content type under Description")
            self.page.locator(catalogue_objects.FORMAT_INPUT_ENG).fill(data["format"])
            formatOption=catalogue_objects.FORMAT_OPTION_ENG.format(option=data["format"])
            self.page.locator(formatOption).first.click()
            logging.info("Enter data for format under Description")    
            self.page.locator(catalogue_objects.LANGUAGE_INPUT_ENG).fill(data["language"])
            languageOption=catalogue_objects.LANGUAGE_OPTION_ENG.format(option=data["language"])
            self.page.locator(languageOption).first.click()
            logging.info("Enter data for language under Description")
            time.sleep(2)         
            self.page.locator(catalogue_objects.FUNCTION_LIST).select_option(data["function"])
            logging.info(f"Selecting function: {data['function']}")
            time.sleep(3)
            # Add the online resource
            self.page.locator(catalogue_objects.ADD_ONLINE_RESOURCE_BUTTON).click()
            logging.info("Clicking on add online resource button")
            time.sleep(3)

#*******************Portal related functions**********************
    
    # Search record in portal
    def searchRecordInPortal(self, page, title: str):
        time.sleep(2)
        page.locator(portal_objects.KEYWORDS_TEXTBOX).clear()
        page.locator(portal_objects.KEYWORDS_TEXTBOX).fill(title)
        logging.info("Filling keywords textbox with title: %s", title)
        page.locator(portal_objects.LAUNCH_SEARCH_BUTTON).click()
        logging.info("Clicking launch search button")         

    # Select publication channel
    def selectPublicationChannel(self, page, channel: str):
        page.locator(portal_objects.PUBLISH_TO_CHANNEL_BUTTON).wait_for(state="visible", timeout=60000)
        page.locator(portal_objects.PUBLISH_TO_CHANNEL_BUTTON).click()
        logging.info("Clicking publish channel button")
        with page.expect_popup() as page_info:
            page.locator(portal_objects.PUBLICATION_CHANNEL_MENUITEM.format(channel=channel)).click()
        publish_page = page_info.value
        logging.info(f"Selecting publication channel: {channel}")
        return publish_page

    # Abandon the publication process
    def abandonPublicationProcess(self, page):            
        time.sleep(5)
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator(portal_objects.ABANDON_PUBLICATION_BUTTON).click()
        logging.info("Clicking abandon publication button")
        time.sleep(3)
        page.locator(portal_objects.SUCCESS_MESSAGE_ALERT).wait_for(state="visible", timeout=300000)
        expect(page.locator(portal_objects.SUCCESS_MESSAGE_ALERT)).to_contain_text("The publication was successfully abandoned.")
        logging.info("Publication process successfully abandoned")

    # Confirm details in publication process
    def confirmDetailsInPublicationProcess(self, page):
        page.get_by_label("Business Data Trustee").select_option("98d3e659-1405-4ddb-a4de-8703aee6cae6")
        logging.info("Selecting Business Data Trustee option")
        page.get_by_label("Chief Digital Officer").select_option("d6778bbc-8451-4d28-a44a-75cf43be72c7")
        logging.info("Selecting Chief Digital Officer option")
        page.get_by_role("button", name="Confirm and Initiate").click()
        logging.info("Clicking confirm and initiate button")           

    # Release process
    def releaseProcess(self, page):        
        page.locator(portal_objects.RELEASE_CRITERIA_0_0).select_option("true")
        logging.info("Checking release criteria 0.0")
        page.locator(portal_objects.RELEASE_CRITERIA_1_0).select_option("true")
        logging.info("Checking release criteria 1.0")
        page.locator(portal_objects.RELEASE_CRITERIA_2_0).select_option("true")
        logging.info("Checking release criteria 2.0")
        page.locator(portal_objects.RELEASE_CRITERIA_3_0).select_option("true")
        logging.info("Checking release criteria 3.0")
        page.locator(portal_objects.RELEASE_CRITERIA_3_1).select_option("true")
        logging.info("Checking release criteria 3.1")
        page.locator(portal_objects.RELEASE_CRITERIA_4_0).select_option("true")
        logging.info("Checking release criteria 4.0")
        page.locator(portal_objects.RELEASE_CRITERIA_5_0).select_option("true")
        logging.info("Checking release criteria 5.0")
        page.locator(portal_objects.RELEASE_CRITERIA_5_1).select_option("true")
        logging.info("Checking release criteria 5.1")
        page.locator(portal_objects.RELEASE_CRITERIA_6_0).select_option("true")
        logging.info("Checking release criteria 6.0")
        page.locator(portal_objects.RELEASE_CRITERIA_7_0).select_option("true")
        logging.info("Checking release criteria 7.0")
        page.locator(portal_objects.CONFIRM_BUTTON).click()
        logging.info("Clicking confirm button")

    def approveRecord(self, page, username: str, title: str):
        """Approve the record in the portal"""
        page.locator(portal_objects.PRODUCTS_BUTTON).click()
        logging.info("Clicking on Products button")
        page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
        logging.info("Clicking on Data Publishing option")
        time.sleep(3)
        row_locator = page.locator(portal_objects.ROW_LOCATOR_TEMPLATE.format(title=title))
        row_locator.locator('td:nth-child(1) a').click()
        logging.info(f"Clicking on record link for title: {title}")
        time.sleep(3)
        logging.info("Waiting for the page to load after clicking on record link")
        page.locator(portal_objects.APPROVE_RADIO_BUTTON).click()
        logging.info("Clicking on Approve radio button to approve the record")
        page.locator(portal_objects.SUBMIT_BUTTON).click()
        logging.info("Clicking on Submit button to approve the record")
        logging.info(f"Record '{title}' approved by {username}")
    
    def notApproveRecord(self, page, username: str, title: str):
        """Approve the record in the portal"""
        page.locator(portal_objects.PRODUCTS_BUTTON).click()
        logging.info("Clicking on Products button")
        time.sleep(2)
        page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
        logging.info("Clicking on Data Publishing option")
        time.sleep(5)
        logging.info("Waiting for the page to load")
        row_locator = page.locator(portal_objects.ROW_LOCATOR_TEMPLATE.format(title=title))
        row_locator.locator('td:nth-child(1) a').click()
        logging.info(f"Clicking on record link for title: {title}")
        time.sleep(3)
        page.locator(portal_objects.NOT_APPROVED_RADIO_BUTTON).click()
        logging.info("Clicking on Not Approved radio button to not approve the record")        
        page.locator(portal_objects.REJECT_REASON_TEXTBOX).clear()
        page.locator(portal_objects.REJECT_REASON_TEXTBOX).fill("Not approved by "+ username)
        page.locator(portal_objects.REJECT_REASON_TEXTBOX).press("End")
        logging.info("Filling reject reason textbox with: Not approved by " + username)
        time.sleep(2)
        page.locator(portal_objects.SUBMIT_BUTTON).click()
        logging.info("Clicking on Submit button")
        logging.info(f"Record '{title}' not approved by {username}")

    def finalReview(self, page, title: str):
        page.locator(portal_objects.PRODUCTS_BUTTON).wait_for(state="visible", timeout=90000)
        page.locator(portal_objects.PRODUCTS_BUTTON).click()
        logging.info("Clicking on Products button")
        time.sleep(2) 
        page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
        logging.info("Clicking on Data Publishing option")
        time.sleep(20)
        expect(page).to_have_title("EDH Publishing - Dashboard", timeout=180000)  # Timeout is 180 seconds
        logging.info("Validated that the page title is 'EDH Publishing - Dashboard'")
        row_locator = page.locator(f'tr:has(td.force-wrap:has-text("{title}"))')   
        #row_locator.wait_for(state="visible", timeout=150000) 
        row_locator.locator('td:nth-child(1) a').click()
        logging.info(f"Clicking on record link for title: {title}")
        time.sleep(5)
        page.get_by_role("button", name="Complete Publication").click()
        logging.info("Clicking on Complete Publication button")          
        page.locator("#loader").wait_for(state="hidden")
        print("Spinner has disappeared.")
        time.sleep(1.5)

    def goToFGP(self, page, title: str):
        time.sleep(5)
        expect(page.locator(portal_objects.VIEW_ON_FGP_BUTTON)).to_be_visible()
        with page.expect_popup() as page_info:
            page.locator(portal_objects.VIEW_ON_FGP_BUTTON).click()
        logging.info("Opening FGP in a new tab")
        new_page = page_info.value
        time.sleep(3)
        return new_page

   
    def searchPublication(self,page, title: str):
        """Search for a publication by title"""
        # page.locator(portal_objects.PRODUCTS_BUTTON).click()
        # logging.info("Clicking on Products button")
        # page.locator(portal_objects.DATA_PUBLISHING_OPTION).click()
        # logging.info("Clicking on Data Publishing option")
        # time.sleep(10)
        # page.locator(portal_objects.SEARCH_PUBLICATION_OPTION).click()
        # logging.info("Clicking on Search Publication option")
        
        page.locator(portal_objects.SEARCH_PUBLICATION_TEXTBOX).fill(title)
        logging.info(f"Filling keywords textbox with title: {title}")
        page.locator(portal_objects.SEARCH_PUBLICATION_TEXTBOX).press("Enter")
        time.sleep(3)

    def createServiceRequest(self,page,title: str):
        time.sleep(2)
        with page.expect_popup() as page_info:
         page.locator(catalogue_objects.MAP_SERVICE_REQUEST_OPTION).click()
         logging.info("Clicking map service request option")              
        service_page = page_info.value
        service_page.locator(portal_objects.SERVICE_REQUEST_DETAILS_TEXTAREA).fill("Service Request")
        logging.info("Filling service request title input")
        service_page.locator(portal_objects.SUBMIT_REQUEST_BUTTON).click()
        logging.info("Clicking submit request button")
        service_page.locator(portal_objects.PENDING_REQUEST_INPUT_FIELD).fill(title)
        logging.info(f"Filling search input field with title: {title}")
        service_page.locator(portal_objects.PENDING_REQUEST_INPUT_FIELD).press("Enter")
        logging.info("Pressing Enter to search for the service request")
        time.sleep(3)
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_be_visible()
        logging.info("Service request pending table is visible")
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text(title)
        logging.info(f"Service request with title '{title}' is present in the pending table")
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text('Pending "Accept Service Request"')
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text("0")
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text("Mapping")
        expect(service_page.locator(portal_objects.SERVICE_REQUEST_PENDING_TABLE)).to_contain_text("GIS Team")
        return service_page




#********************************Common functions***************************
    # Switch to tab by title
    def switch_to_tab_by_title(self, context, title: str):
        logging.info(f"Switching to tab with title: {title}")
        for page in context.pages:
            if page.title() == title:
                page.bring_to_front()
                return page           

    # Navigate to a specific URL
    def navigateToUrl(self, url: str):        
        logging.info(f"Navigating to URL: {url}")
        time.sleep(2)
        self.page.goto(url,timeout=90000)
        time.sleep(3)         
        logging.info(f"Successfully navigated to {url}")


    def import_record(self, file1_path: str):
        self.page.locator(catalogue_objects.CONTRIBUTE_MENU).click()
        logging.info("Clicking contribute menu")
        self.page.locator(catalogue_objects.IMPORT_NEW_RECORD_OPTION).click()
        time.sleep(2)
        # Upload  file
        #self.page.locator(catalogue_objects.CHOOSE_FILE_BUTTON).click()
        self.page.locator(catalogue_objects.CHOOSE_FILE_BUTTON).set_input_files(file1_path)
        time.sleep(2)    
        self.page.locator(catalogue_objects.GENERATE_UUID_CHECKBOX).click()
        logging.info("Checking generate UUID checkbox")
        # Click upload button (empty name button)
        self.page.locator(catalogue_objects.IMPORT_BUTTON).click()
        time.sleep(3)
        self.page.locator(catalogue_objects.EDIT_RECORD_LINK).click()