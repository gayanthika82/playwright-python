import logging
import time
import pytest
from objects_repository import portal_objects
from playwright.sync_api import Page, expect
import os
from utils.common_utils import CommonUtils

 # Get the userId and username from environment variables   

username_editor_a = os.getenv("EDITOR_A_NAME")
title=None
@pytest.mark.test_case_ids([73299,74298,74658,78091,78667,78834,79060,85123,86159,86409])
@pytest.mark.dependency()
def test_api_registry_create(page_setup) -> None:
    global title
    # global test_status  # Use the shared state
    
    logging.info("Starting test_api_registry")
    page = page_setup
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")

    # try:    
    # Create record title
    common_utils = CommonUtils(page)
    # Generate a unique title for the record
    title = "API_Registry_"
    title = common_utils.createCatalogueRecordTitle(title)

    random_suffix = common_utils.createUniqueNumber()
    base_url = os.getenv("API_BASE_URL")
    onboarding_url= base_url + '/api-registry/onboarding'
    MINIMAL_API_SPEC = """{
            "openapi": "3.0.0",
            "info": {
                "title": "Test API",
                "version": "1.0.0"
            },
            "paths": {
                "/test": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful response"
                            }
                        }
                    }
                }
            }
        }"""

    if not  userId_editor_a :
        raise ValueError("Environment variables are not set")

    # Login
    common_utils.login(userId_editor_a)
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()
    # Select API Registry from Products menu
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.API_REGISTRY_OPTION).click()
    logging.info("Clicking on API Registry option in portal")
    portal_page.wait_for_load_state("networkidle")  # Wait for the network to be idle
    time.sleep(2)

    # Validate API Registry page
    expect(portal_page).to_have_title("API Registry - Dashboard")
    logging.info("Validated that the page title is 'API Registry - Dashboard'")
    time.sleep(3)
    # Go to onboarding page
    common_utils = CommonUtils(portal_page)
    common_utils.navigateToUrl(onboarding_url)
    logging.info("Go to API Registry onboarding page: %s", onboarding_url)
    time.sleep(3)
    expect(portal_page).to_have_title("API Registry - Onboarding form")

    # Fill the onboarding form
    portal_page.locator(portal_objects.API_REGISTRY_TITLE_ENG).fill(title)
    logging.info("Filling Title (eng) textbox with '%s'", title)
    portal_page.locator(portal_objects.API_REGISTRY_TITLE_FRA).fill("TEST-FRA")
    logging.info("Filling Title (fra) textbox with 'TEST-FRA'")
    portal_page.locator(portal_objects.API_REGISTRY_SENSITIVITY).select_option("Unclassified")
    logging.info("Selecting Sensitivity as 'Unclassified'")
    portal_page.locator(portal_objects.API_REGISTRY_PUBLICATION_LEVEL).select_option("Public")
    logging.info("Selecting Publication Level as 'Public'")
    portal_page.locator(portal_objects.API_REGISTRY_CONTACT_NAME).fill("Test1")
    logging.info("Filling Contact Name textbox with 'Test1'")
    portal_page.locator(portal_objects.API_REGISTRY_CONTACT_EMAIL).fill("agampodi.dezoysa@dfo-mpo.gc.ca")
    logging.info("Filling Contact Email textbox with 'Test1'")
    portal_page.locator(portal_objects.API_REGISTRY_CONTACT_NUMBER).fill("1234567890")
    logging.info("Filling Contact Number textbox with '1234567890'")
    portal_page.locator(portal_objects.API_REGISTRY_METADATA).fill("2801271f-ba74-4304-a643-94c1c8985997")
    logging.info("Filling Metadata textbox with '2801271f-ba74-4304-a643-94c1c8985997'")
    portal_page.locator(portal_objects.API_REGISTRY_AUTHORIZATION).check()
    logging.info("Checking Authorization checkbox")
    portal_page.locator(portal_objects.API_REGISTRY_OPENAPI_ENG).click()
    logging.info("Clicking on OpenAPI link (eng)")
    portal_page.locator(portal_objects.API_REGISTRY_OPENAPI_SPECIFICATION_ENG).fill(MINIMAL_API_SPEC)
    logging.info("Filling textbox with 'https://petstore.swagger.io/v2/swagger.json'")
    portal_page.locator(portal_objects.API_REGISTRY_OPENAPI_SUFFIX_ENG).fill(random_suffix)
    logging.info("Filling Suffix (eng) textbox with 'test'")
    portal_page.locator(portal_objects.API_REGISTRY_SERVICE_TEST_URL).fill("https://test.edh-cde.unclass.dfo-mpo.gc.ca/catalogue")
    logging.info("Filling Service Test URL textbox with 'https://test.edh-cde.unclass.dfo-mpo.gc.ca/catalogue'")
    time.sleep(2)
    portal_page.locator(portal_objects.API_REGISTRY_VALIDATE_BUTTON).click()    
    logging.info("Clicking on Validate button")
    time.sleep(2)
    expect(portal_page.locator(portal_objects.API_REGISTRY_VALIDATE_MESSAGE)).to_contain_text("Successfully validated the OpenAPI Specification(s).")
    portal_page.locator(portal_objects.API_REGISTRY_SAVE_BUTTON).click()
    time.sleep(2)
    logging.info("Clicking on Save button")
    expect(portal_page.locator(portal_objects.API_REGISTRY_VALIDATE_MESSAGE)).to_contain_text("Successfully saved draft.")
    logging.info("API record created successfully with title: %s", title)

    # Close the portal page
    portal_page.close()
    logging.info("Portal page closed")

    # Switch to catalogue tab
    common_utils = CommonUtils(page)
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")
    # Logout
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", username_editor_a)


@pytest.mark.dependency(depends=["test_api_registry_create"])
def test_api_registry_undraft(page_setup) -> None:
    global title    
    logging.info("Starting test_undraft_api_registry")
    page = page_setup
    userId_gn_admin = os.getenv("USERNAME_ADMIN")
    common_utils = CommonUtils(page)
   #Login as GIS Team 
    common_utils.login(userId_gn_admin)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.API_REGISTRY_OPTION).click()
    logging.info("Clicking on API Registry option in portal")
    time.sleep(2)
    portal_page.locator(portal_objects.API_REGISTRY_FILTER_ITEMS).fill(title)
    logging.info("Filling API Registry filter items with title: %s", title)
    time.sleep(2)    
    portal_page.locator(portal_objects.API_REGISTRY_EDIT_BUTTON.format(title=title)).click()
    logging.info("Clicking on Edit button for title: %s", title)
    portal_page.locator(portal_objects.API_REGISTRY_DRAFT_CHECKBOX).uncheck()
    logging.info("Unchecking Draft checkbox")
    time.sleep(2)
    portal_page.locator(portal_objects.API_REGISTRY_SAVE_BUTTON).click()
    logging.info("Clicking on Save button")
    time.sleep(2)
    expect(portal_page.locator(portal_objects.API_REGISTRY_VALIDATE_MESSAGE)).to_contain_text("Successfully saved draft.")
    logging.info("API record created successfully with title: %s", title)
    # Close the portal page
    portal_page.close()
    logging.info("Portal page closed")

    # Switch to catalogue tab
    common_utils.switch_to_tab_by_title(page.context,"Catalogue (Test)")
    # Logout
    common_utils.catalogueLogout()
    logging.info("User %s logged out successfully", userId_gn_admin)

@pytest.mark.dependency(depends=["test_api_registry_undraft"])
def test_api_registry_submit(page_setup) -> None:
    global title
    logging.info("test_submit_api_registry")
    page = page_setup
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    common_utils = CommonUtils(page)
    common_utils.login(userId_editor_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.API_REGISTRY_OPTION).click()
    logging.info("Clicking on API Registry option in portal")
    time.sleep(2)    
    portal_page.locator(portal_objects.API_REGISTRY_EDIT_BUTTON.format(title=title)).click()
    logging.info("Clicking on Edit button for title: %s", title)
    time.sleep(2)
    portal_page.locator(portal_objects.API_REGISTRY_SUBMIT_BUTTON).click()  
    logging.info("Clicking on Submit button")
    time.sleep(2)
    portal_page.locator(portal_objects.API_REGISTRY_REQUEST_DETAILS).fill("Testing API Registry")
    logging.info("Filling Request Details textbox with 'Testing API Registry'")
    time.sleep(1)
    portal_page.locator(portal_objects.API_REGISTRY_SUBMIT_REQUEST_BUTTON).click()
    logging.info("Clicking on Submit Request button")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

@pytest.mark.dependency(depends=["test_api_registry_submit"])
def test_api_registry_developer_accept(page_setup) -> None:
    global title
    logging.info("test_developer_accept_api_registry")
    page = page_setup
    userId_registeredUser_a = os.getenv("USERNAME_REGISTEREDUSER_B")
    common_utils = CommonUtils(page)
    common_utils.login(userId_registeredUser_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

    # Find the record and complete accept request
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"APIM Developer Accept Service Request\"')"
    portal_page.locator(button_locator).wait_for(state="visible", timeout=10000)
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Accept Service Request' button for title: {title}")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Accept Service Request", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Accept Service Request'")

    #Validate Accept Service Request Page
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_FORM)).to_contain_text("API")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_FORM)).to_contain_text("Testing API Registry")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Request Progress")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("APIM Developer Accept Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text(" Deploy to APIM Development")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Contributor Approval")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Accept Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Approval")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Production")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Test1")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("agampodi.dezoysa@dfo-mpo.gc.ca")


    #Accept Service Request
    portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_BUTTON).click()
    logging.info("Clicking on Accept Service Request button")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service(s) Details", timeout=60000)  # Timeout is 60 seconds
    logging.info("Service(s) Details")


    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("APIM Developer Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Test1")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("agampodi.dezoysa@dfo-mpo.gc.ca")


    portal_page.locator(portal_objects.SERVICE_REQUEST_DETAILS_TEXTAREA).fill("Service Request accepted successfully")
    logging.info("Filling Service Request details textarea with 'Service Request accepted successfully'")
    portal_page.locator(portal_objects.SEND_BUTTON).click()
    logging.info("Clicking on Send button to accept service request")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")


@pytest.mark.dependency(depends=["test_api_registry_developer_accept"])
def test_api_registry_contributor_approval(page_setup) -> None:
    global title
    logging.info("test_developer_accept_api_registry")
    page = page_setup
    userId_editor_a = os.getenv("USERNAME_EDITOR_A")
    common_utils = CommonUtils(page)
    common_utils.login(userId_editor_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

    # Find the record and complete accept request
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"API Contributor Approval\"')"
    portal_page.locator(button_locator).wait_for(state="visible", timeout=10000)
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Accept Service Request' button for title: {title}")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Review And Approve", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Review And Approve'")

    #Validate Accept Service Request Page
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("APIM Developer Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Development - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Contributor Approval")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Accept Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Approval")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Production")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Test1")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("agampodi.dezoysa@dfo-mpo.gc.ca")

    #Complete Requester approval
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_APPROVE_RADIO_BUTTON).click()
    logging.info("Selecting Approve radio button")
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_SUBMIT_BUTTON).click()
    logging.info("Clicking on Submit button to complete requester approval")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

@pytest.mark.dependency(depends=["test_api_registry_contributor_approval"])
def test_api_registry_apiReviewer_approval(page_setup) -> None:
    global title
    logging.info("Starting test_apiReviewer_approval_api_registry")
    page = page_setup
    userId_apireviewer = os.getenv("USERNAME_APIREVIEWER")
    common_utils = CommonUtils(page)
    common_utils.login(userId_apireviewer)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

    # Find the record and complete accept request
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"API Reviewer Accept Service Request\"')"
    portal_page.locator(button_locator).wait_for(state="visible", timeout=10000)
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Accept Service Request' button for title: {title}")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Accept Service Request", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Accept Service Request'")

    #Validate Accept Service Request Page
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("APIM Developer Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Development - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Contributor Approval - approved")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Accept Service Request")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Approval")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Production")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("API")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Testing API Registry")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Service Request accepted successfully")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Test1")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("agampodi.dezoysa@dfo-mpo.gc.ca")

    #Accept Service Request
    portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_BUTTON).click()
    logging.info("Clicking on Accept Service Request button")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Review And Approve", timeout=60000)  # Timeout is 60 seconds
    logging.info("Loading 'Review And Approve' page")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Accept Service Request - completed")
    
    
    #Complete Requester approval
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_APPROVE_RADIO_BUTTON).click()
    logging.info("Selecting Approve radio button")
    time.sleep(2)
    portal_page.locator(portal_objects.SERVICE_REQUEST_SUBMIT_BUTTON).click()
    logging.info("Clicking on Submit button to complete requester approval")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

@pytest.mark.dependency(depends=["test_api_registry_apiReviewer_approval"])
def test_api_registry_deployTo_APIM_Production(page_setup) -> None:
    global title
    logging.info("test_developer_accept_api_registry")
    page = page_setup
    userId_registeredUser_a = os.getenv("USERNAME_REGISTEREDUSER_B")
    common_utils = CommonUtils(page)
    common_utils.login(userId_registeredUser_a)
    
    # Go to portal
    portal_page = common_utils.goToPortalHomePage()

    # Go to Service request
    portal_page.locator(portal_objects.PRODUCTS_BUTTON).click()
    logging.info("Clicking on Products button in portal")
    portal_page.locator(portal_objects.SERVICE_REQUEST_OPTION).click()
    logging.info("Clicking on Service Request option in portal")
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")

    # Find the record and complete accept request
    row_locator = f"table#wb-auto-3 tr:has(td a:has-text('{title}'))"
    button_locator = f"{row_locator} a:has-text('Complete \"Deploy to APIM Production\"')"
    portal_page.locator(button_locator).wait_for(state="visible", timeout=10000)
    portal_page.locator(button_locator).click()
    logging.info(f"Clicked on 'Complete Accept Service Request' button for title: {title}")

    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Deploy to APIM Production", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Deploy to APIM Production'")

    #Validate Accept Service Request Page
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Request Progress")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("APIM Developer Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Development - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Contributor Approval - approved")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Accept Service Request - completed")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("API Reviewer Approval - approved")
    expect(portal_page.locator(portal_objects.SERVICE_REQUEST_PROGRESS_SECTION)).to_contain_text("Deploy to APIM Production")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text(title)
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("Test1")
    expect(portal_page.locator(portal_objects.ACCEPT_SERVICE_REQUEST_PAGE)).to_contain_text("agampodi.dezoysa@dfo-mpo.gc.ca")


    #Accept Service Request
    portal_page.locator(portal_objects.API_REGISTRY_COMPLETE_REQUEST_BUTTON).click()
    logging.info("Clicking on 'Complete Request' button")
   
    # wait for service request dashboard to load
    expect(portal_page).to_have_title("Service Requests - Dashboard", timeout=60000)  # Timeout is 60 seconds
    logging.info("Validated that the page title is 'Service Requests - Dashboard'")
