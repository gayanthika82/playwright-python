#Main Menu Locators
PRODUCTS_BUTTON = "role=button[name='Products']"
HELP_BUTTON = "div.mat-badge:has-text('Help')"
USER_NAME = "role=button[name='{userName}']"

#Sub Menu Locators
DATA_PUBLISHING_OPTION = "role=menuitem[name='Data Publishing']"
SERVICE_REQUEST_OPTION = "role=menuitem[name='Service Request']"
USER_REGISTRY_OPTION = "role=menuitem[name='User Registry']"
EDH_CATALOGUE_OPTION = "role=menuitem[name='EDH Catalogue']"
DATA_VISUALIZATION_OPTION = "role=menuitem[name='Data Visualization']"
DOCUMENTATION = "role=menuitem[name='Documentation']"
CONTACT_US = "role=menuitem[name='Contact Us']"
FEEDBACK = "role=menuitem[name='Feedback']"
API_REGISTRY_OPTION = "role=menuitem[name='API Registry']"

#Portal
PORTAL_HOME = "role=menuitem[name='Home']"
PORTAL_HOME_LINK = "role=link[name='Home']"
PORTAL_DASHBOARD = "role=menuitem[name='Dashboard']"
PORTAL_USER = "role=menuitem[name='{userName}']"


# Search Record Locators
KEYWORDS_TEXTBOX = "#mat-input-0"
LAUNCH_SEARCH_BUTTON = "role=button[name='Launch Search']"
RECORD_LINK_BY_TITLE = "role=link[name='{title}']"  # Dynamic locator for record link by title

# Publication Process Locators
PUBLISH_TO_CHANNEL_BUTTON = "role=button[name='Publish to Channel']"
ABANDON_PUBLICATION_BUTTON = "role=button[name=' Abandon Publication']"
PUBLICATION_CHANNEL_MENUITEM = "role=menuitem[name='{channel}']" # Dynamic locator for publication channel menu item
# Success Message Alert Locator
SUCCESS_MESSAGE_ALERT = "#success-message-alert"
INITIAL_SERVICE_REQUEST_BUTTON = "role=button[name='Initiate Service Request']"
MAP_SERVICE_REQUEST_OPTION = "span.mat-mdc-menu-item-text:has-text('Mapping')"
SERVICE_REQUEST_MESSAGE_TEXTAREA = "#mat-input-2"
SUBMIT_SERVICE_REQUEST_BUTTON = "span.mdc-button__label:has-text('Submit')"

# Publication Approval Locators
BUSINESS_DATA_TRUSTEE_DROPDOWN = "label=Business Data Trustee"
CHIEF_DIGITAL_OFFICER_DROPDOWN = "label=Chief Digital Officer"
CONFIRM_AND_INITIATE_BUTTON = "#btnConfirm"

# Confirm and Continue Button Locator
CONFIRM_AND_CONTINUE_BUTTON = "role=button[name='Confirm and Continue Publication Process']"

# Release Criteria Locators
RELEASE_CRITERIA_0_0 = "[id='releaseCriteria0\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_1_0 = "[id='releaseCriteria1\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_2_0 = "[id='releaseCriteria2\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_3_0 = "[id='releaseCriteria3\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_3_1 = "[id='releaseCriteria3\\.sectionQuestionList1\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_4_0 = "[id='releaseCriteria4\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_5_0 = "[id='releaseCriteria5\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_5_1 = "[id='releaseCriteria5\\.sectionQuestionList1\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_6_0 = "[id='releaseCriteria6\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
RELEASE_CRITERIA_7_0 = "[id='releaseCriteria7\\.sectionQuestionList0\\.releaseCriteriaAnswer']"
CONFIRM_BUTTON = "role=button[name='I Confirm']"

# Start Validation and Draft Upload Button Locator
START_VALIDATION_BUTTON = "#btnValidate"
# Locator for the "Export" button
EXPORT_BUTTON = "role=button[name='Export']"
# Approval Locators
CATALOGUE_MODIFIED_WARNING = "div.alert.alert-warning:has-text('The catalogue entry has been modified since the publication process began.')"
APPROVE_RADIO_BUTTON = "role=radio[name='I approve the release of the catalogue entry']"
NOT_APPROVED_RADIO_BUTTON = "role=radio[name='I do not approve the release of the catalogue entry']"
REJECT_REASON_TEXTBOX = "role=textbox[name='Reason']"
SUBMIT_BUTTON = "role=button[name='Submit']"
COMPLETE_PUBLICATION_BUTTON = "#btnComplete"
VIEW_ON_FGP_BUTTON = "role=link[name=' View on Federal Geospatial Platform']"
COMPLETE_FINAL_PUBLICATION = "text='Complete Final Publication'"
COMPLETE_DECIDE_PUBLICATION_PROCESS = "a.btn.btn-default:has-text('Complete \"Decide to continue or abandon the publication process\"')"
COMPLETE_FGP_VALIDATION_AND_DRAFT_UPLOAD = "a.btn.btn-default:has-text('Complete \"FGP Validation and Draft Upload\"')"
COMPLETE_VERIFY_PUBLISHED_RECORD = "a.btn.btn-default:has-text('Complete \"Verify Published Record\"')"



# Locators for Catalogue Add Resource Page
# ADD_BUTTON = "role=button[name='+ Add']"
# LINK_ONLINE_RESOURCE = "role=link[name='   Link an online resource']"
# FILE_INPUT = "input[name='file']"
# FILE_CELL_LINK = "xpath=//*[@class='fa external-resource-validation-status-incomplete']"
# PROTOCOL_LIST = "#gn-addonlinesrc-protocol-list"

# DESCRIPTION_ROW_TEXTBOX = "#gn-addonlinesrc-description-row >> role=textbox[name='Type or search']"
# DESCRIPTION_ROW_DATASET = "#gn-addonlinesrc-description-row >> text='Dataset'"
# DESCRIPTION_ROW_LANGUAGE = "#gn-addonlinesrc-description-row >> role=textbox[name='Type or search']:nth(2)"
# FUNCTION_LIST = "#gn-addonlinesrc-function-list"
# ADD_ONLINE_RESOURCE_BUTTON = "role=button[name='   Add online resource']"

# # Locators for Popup Page
# POPUP_DESCRIPTION_INPUT = "label=Description"
# POPUP_DESCRIPTION_FRENCH_INPUT = "#description_french"

# # Locators for Popup Page - Disposition Policy and Basic Properties
# DISPOSITION_POLICY_LINK = "role=link[name='Disposition Policy']"
# DISPOSITION_PERIOD_COUNT_INPUT = "#dispositionperiodcount"
# DISPOSITION_ACTION_SELECT = "label=Disposition Action"
# DISPOSITION_PERIOD_TYPE_SELECT = "label=Disposition Period Type"
# DISPOSITION_CONTACT_EMAIL_INPUT = "#dispositioncontactemail"
# BASIC_PROPERTIES_LINK = "role=link[name='Basic Properties']"
# SENSITIVITY_SELECT = "label=Sensitivity"
# PUBLICATION_LEVEL_SELECT = "label=Publication Level"
# VALIDATE_BUTTON = "role=button[name=' Validate']"
# SAVE_AND_CLOSE_BUTTON = "role=button[name=' Save & close']"

# Publish verification Locators
RETURN_TO_DASHBOARD_BUTTON = "role=link[name=' Return to Dashboard ']"
DASHBOARD_LINK = "role=link[name='Dashboard']"
ROW_LOCATOR_TEMPLATE = 'tr:has(td.force-wrap:has-text("{title}"))'
VERIFY_PUBLICATION_PAGE_HEADER = "#pageHeader"
VERIFY_PUBLICATION_PAGE_P1 = "#pnlSubmit"
VERIFY_PUBLICATION_BUTTON = "role=button[name=' Verify Publication']"
VERIFY_PUBLICATION_VERIFICATION = "#validationMsg"

#Restart Publication
RESTART_PUBLICATION_BUTTON = "role=button[name='Restart Publication Process ']"

# Search Publication Locators
SEARCH_PUBLICATION_OPTION = "role=link[name='Search Publications']"
SEARCH_PUBLICATION_TEXTBOX = "role=searchbox[name='Filter items']"
SEARCH_DROPDOWN_PAGES = "role=combobox[name='Show entries']"
EXPORT_BUTTON = "role=button[name='Export']"

# Locators for Skip Approvals and Amendment Details
SKIP_APPROVALS_CHECKBOX = "role=checkbox[name='Skip Approvals']"
AMENDMENT_DETAILS_TEXTBOX = "role=textbox[name='Amendment Details']"

# Service Request
SERVICE_REQUEST_DETAILS_TEXTAREA = "#txtDetails"
SUBMIT_REQUEST_BUTTON = "#btnConfirm"
PENDING_REQUEST_INPUT_FIELD = "input[type='search'][aria-controls='wb-auto-4']"
COMPLETED_REQUEST_INPUT_FIELD = "input[type='search'][aria-controls='wb-auto-5']"
SERVICE_REQUEST_PENDING_TABLE = "#wb-auto-4"
SERVICE_REQUEST_COMPLETED_TABLE = "#wb-auto-5"
ACCEPT_SERVICE_REQUEST_FORM = "#acceptRequestForm"
ACCEPT_SERVICE_REQUEST_BUTTON = "#btnAccept"
SERVICE_REQUEST_PROGRESS_SECTION = "#divProcess"
ACCEPT_SERVICE_REQUEST_PAGE = "main[property='mainContentOfPage']"
SEND_BUTTON = "#btnSend"
COMPLETE_REQUESTER_APPROVAL_BUTTON = "a.btn.btn-default:has-text('Complete \"Requester approval\"')"
SERVICE_REQUEST_APPROVE_RADIO_BUTTON = "#optApprove"
SERVICE_REQUEST_SUBMIT_BUTTON = "#btnSubmit"
ABANDON_SERVICE_REQUEST_BUTTON = "#btnCancel"


# Locator for Service Request Link by Title
#SERVICE_REQUEST_LINK_BY_TITLE = "a:has-text('{title}')"

# Locator for Status Section
STATUS_SECTION = "div.col-sm-7 div.well:has-text('Status:')"

# Locator for Service Request Type
SERVICE_REQUEST_TYPE = "div.col-sm-7 div.well:has-text('Service Request Type:')"

# Locator for Catalogue Entry Title
CATALOGUE_ENTRY_TITLE = "div.col-sm-7 div.well:has-text('Catalogue Entry Title:')"

# Locator for Catalogue Entry Abstract
CATALOGUE_ENTRY_ABSTRACT = "div.col-sm-7 div.well:has-text('Catalogue Entry Abstract:')"

# Locator for Metadata XML Code
METADATA_XML_CODE = "#txtMetadataXml"

# Locator for Copy Metadata XML Button
COPY_METADATA_XML_BUTTON = "#btnCopyMetadataXml"

# Locator for Copied Metadata XML Message
COPIED_METADATA_XML_MESSAGE = "#msgCopiedMetadataXml"

# Locator for Full Service Request History
FULL_SERVICE_REQUEST_HISTORY = "details:has(summary:has-text('View Full Service Request History'))"

# Locator for Individual History Items
SERVICE_REQUEST_HISTORY_ITEMS = "details:has(summary:has-text('View Full Service Request History')) ul.list-unstyled li"

#FGP Locators
FGP_RESOURCE_TABLE = "table#wb-auto-6"
FGP_RECORD_TITLE = "#wb-cont"
FGP_FILE_TYPE = 'role=link[name="{fileType}"]'

#API Registry Locators
API_REGISTRY_ONBOARDING_BUTTON = "role=menuitem[name='Onboarding']"

# API Registry Locators
#API_REGISTRY_ONBOARDING_BUTTON = "a.item[role='menuitem'][href='/api-registry/onboarding']:has-text('Onboarding')"
API_REGISTRY_OPTION = "role=menuitem[name='API Registry']"
API_REGISTRY_TITLE_ENG = "#titleEn"
API_REGISTRY_TITLE_FRA = "#titleFr"
API_REGISTRY_SENSITIVITY = "#sensitivityLevel"
API_REGISTRY_PUBLICATION_LEVEL = "#publicationLevel"
API_REGISTRY_CONTACT_NAME = "#contactName"
API_REGISTRY_CONTACT_EMAIL = "#contactEmail"
API_REGISTRY_CONTACT_NUMBER = "#contactPhoneNum"
API_REGISTRY_METADATA = "#catalogMetadataId"
API_REGISTRY_AUTHORIZATION = "#interimAuthOperate1"
API_REGISTRY_OPENAPI_ENG = "summary:has-text('OpenAPI (English)')"
API_REGISTRY_OPENAPI_SPECIFICATION_ENG = "#openApiSpecificationEn"
API_REGISTRY_OPENAPI_SUFFIX_ENG = "#suffixEn"
API_REGISTRY_SERVICE_TEST_URL = "#serviceUrlEnList1\\.serviceUrl"
API_REGISTRY_VALIDATE_BUTTON = "#validate"
API_REGISTRY_VALIDATE_MESSAGE = "#alert-success"
API_REGISTRY_SAVE_BUTTON = "#save"
API_REGISTRY_FILTER_ITEMS = "input[aria-controls='wb-auto-3'][type='search']"
API_REGISTRY_EDIT_BUTTON = "tr:has(td.force-wrap:has-text('{title}')) a:has-text('Edit')"
API_REGISTRY_SUBMIT_BUTTON = "#submit"
API_REGISTRY_REQUEST_DETAILS = "#txtDetails"
API_REGISTRY_SUBMIT_REQUEST_BUTTON = "#btnConfirm"
API_REGISTRY_DRAFT_CHECKBOX = "#chkIsDraft"  # Locator for the Draft checkbox
#API_REGISTRY_MESSAGE = "#apiRegistryMessage"  # Locator for the message displayed after saving
API_REGISTRY_COMPLETE_REQUEST_BUTTON = "#btnCompleteRequest"  # Locator for the Complete Request button