# Navigation Menu
PORTAL_HOME_BUTTON = "role=link[name='EDH Portal']"
CATALOGUE_HOME_MENU = "role=link[name='Logo Catalogue (Test)']"
SEARCH_MENU = "role=menuitem[name=' Search'] >> role=link"
MAP_MENU = "role=link[name='Map']"
CONTRIBUTE_MENU = "role=button[name=' Contribute']"
ADMIN_CONSOLE = "span.ng-scope:has-text('Admin console')"

# Contribute Submenu
EDITOR_BOARD_OPTION = "role=link[name=' Editor board']"
ADD_NEW_RECORD_OPTION = "role=menuitem[name='+  Add new record'] >> role=link"
IMPORT_NEW_RECORD_OPTION = "span.ng-scope:has-text('Import new records')"
MANAGE_DIRECTORY_OPTION = "role=link[name=' Manage directory']"
MAP_SERVICE_REQUEST_OPTION= "a:has-text('Map Service Request')"
SUMMARY_MENU_ITEM = "a:has-text('Summary')"
METADATA_AND_TEMPLATE_MENU_ITEM = "a:has-text('Metadata and templates')"



# User Menu
USER_NAME = "role=link[name='Avatar groupa reviewer']"
USER_NAME_A = "role=link[name='Avatar groupa reviewer']"
USER_NAME_B = "role=link[name='Avatar groupb reviewer']"
USER_NAME_CDO = "role=link[name='Avatar cdo groupa Editor']"
USER_PROFILE = "role=link[name='groupa reviewer']"
SIGN_OUT = "role=link[name=' Sign out']"

# Admin console locators
# Locator for the "Total number of records visible to you" header
SUMMARY_MENU_ITEM_VALIDATION= "h2.ng-binding[title='Total number of records visible to you.']"
METADATA_AND_TEMPLATE_MENU_ITEM_VALIDATION = "div.panel-heading.ng-scope:has-text('Load samples and templates for metadata standards')"

# Content Locators
MAIN_CONTENT = "#main-content"
NAVBAR = "#navbar"
LOGIN_DROPDOWN = "#gn-login-dropdown"
INFO_TABSET = "#info-tabset"
DIRECTORY_CONTAINER = "#gn-directory-container"
THUMBNAIL_IMAGE = "img.img-thumbnail[alt='thumbnail_en.png'][title='thumbnail_en.png']"

# Signout Locators
USER_INFO_BUTTON = "xpath=//*[@class='gn-user-info hidden-sm hidden-md']"
SIGN_OUT_BUTTON = "xpath=//*[@title='Sign out']"


# Create record in Catalogue
ADD_NEW_RECORD_OPTION = "role=link[name='+  Add new record']"

# Locator for the "Dataset" link
DATASET = "a.list-group-item.ng-scope.active[data-ng-click*='getTemplateNamesByType']:has(p:has-text('Dataset'))"
TEMPLATE_A = "role=link[name='Template A']"
GROUP_DDL_A_OPTION = "role=combobox"
# Locator for the "Dropdown Toggle" button
CREATE_TOGGLE_BUTTON = "button.btn.btn-success.dropdown-toggle[data-ng-disabled*='!activeTpl']"
PUBLISH_FOR_GROUP_EDITORS_CHECKBOX = "input[type='checkbox'][data-ng-model='publishForGroupEditors']"
CREATE_BUTTON = "role=button[name='+ Create']"
NON_GEOGRAPHIC_DATASET = "role=link[name=' Non geographic dataset']"
TEMPLATE_B = "role=link[name='Template_B']"

# Catalogue record create window locators
# These locators are used in the Catalogue record creation process
TITLE_TEXTBOX = "role=textbox[name='Title *']"
VALIDATE_BUTTON = "role=button[name=' Validate']"
SAVE_AND_CLOSE_BUTTON = "role=button[name='Save & close']"

# Catalogue Editor Board Locators
SEARCH_TEXTBOX = "role=textbox[name='Search']"
SEARCH_BUTTON = "role=button[name=' Search']"
WORKING_COPY_BUTTON = "role=link[name=' Working copy']"
RECORD_LINK_BY_TITLE = "role=link[name='{title}']" # Dynamic locator for record link by title

# Catalogue Record Detail Locators
MANAGE_RECORD_BUTTON = "role=button[name='Manage record']"
DIRECT_APPROVE_OPTION = "role=link[name='   Directly approve metadata']"
DIRECTLY_APPROVE_MESSAGE_TEXTBOX = "role=textbox[name='Message']"
DIRECT_APPROVE_BUTTON = "role=button[name='Approve']"
PUBLISH_OPTION = "role=link[name='   Publish']"
# Navigation Menu 
UNPUBLISH_LINK = "span:has-text('Unpublish')"
RESTORE_TO_DRAFT_LINK = "a:has(span.ng-binding:has-text('Restore record to draft status'))"
SUBMIT_FOR_REVIEW_LINK = "role=link[name='   Submit for review']"
REJECT_APPROVAL_SPAN = "span.ng-binding:has-text('Reject approval submission')"
APPROVE_METADATA_SPAN = "//*[text()='Approve metadata']"
MESSAGE_TEXTBOX = "role=textbox[name='Message']"
RETIRE_METADATA_LINK = "a:has(span.ng-binding:has-text('Retire metadata'))"
RETIRE_BUTTON = "button.btn.btn-default.ng-binding:has-text('Retire')"
SUBMIT_BUTTON = "role=button[name='Submit']"
RECORD_CARD = ".row.gn-card"


PUBLISH_EXTERNAL_OPTION = "role=link[name='   External Publishing']"
SUBMIT_FOR_REVIEW_OPTION = "role=link[name='   Submit for review']"
SUBMIT_BUTTON = "role=button[name='Submit']"
DELETE_RECORD_BUTTON = "role=link[name=' Delete']"
CLOSE_DELETE_POPUP_BUTTON = "role=button[name='Close']"
#EDIT_RECORD_BUTTON = "role=link[name='Edit']"
EDIT_RECORD_BUTTON = "a.btn.btn-default.gn-md-edit-btn[title='Edit']"
WORKING_COPY_LINK = "role=link[name=' This record has a working copy version. Click here to see it. ']"
CANCEL_WORKING_COPY_BUTTON = "role=link[name=' Cancel working copy']"
DELETE_RECORD_BUTTON = "role=link[name=' Delete']"
CLOSE_DELETE_POPUP_BUTTON = "role=button[name='Close']"

# Catalogue Resorce Detail Locators
#ADD_RESOURCE_BUTTON = "button.btn.btn-default.btn-block.dropdown-toggle[data-toggle='dropdown']"
LINK_ONLINE_RESOURCE = "role=link[name='   Link an online resource']"
# Locator for the "Add online resource" button
ADD_RESOURCE_BUTTON = "a.btn.btn-default.btn-xs[title='addOnlinesrc-help'][data-ng-click*='onOpenPopup']:has(span:has-text('Add online resource'))"

# File resource popup window locators
RESOURCE_DESCRIPTION_TEXTBOX = "#description_english"
RESOURCE_DESCRIPTION_FRENCH_TEXTBOX = "#description_french"
RESOURCE_SENSITIVITY_DROPDOWN = "#sensitivity"
DISPOSITION_POLICY_LINK = "role=link[name='Disposition Policy']"
DISPOSITION_PERIOD_COUNT_INPUT = "#dispositionperiodcount"
DISPOSITION_ACTION_DROPDOWN = "#dispositionaction"
DISPOSITION_PERIOD_TYPE_DROPDOWN = "#dispositionperiodtype"
DISPOSITION_CONTACT_EMAIL_INPUT = "#dispositioncontactemail"
BASIC_PROPERTIES_LINK = "role=link[name='Basic Properties']"

PUBLICATION_LEVEL_DROPDOWN = "#publicationlevel"
RESOURCE_VALIDATE_BUTTON = "role=button[name=' Validate']" 
VALIDATION_MESSAGE = "#validation_message"
RESOURCE_SAVE_AND_CLOSE_BUTTON = "#submit_button"

# Import New Records Locators (add these to your existing file)
CHOOSE_FILE_BUTTON = "role=button[name='Choose File']"
UPLOAD_BUTTON = "role=button[name='']"
GENERATE_UUID_CHECKBOX = "span.ng-scope:has-text('Generate UUID for inserted metadata')"
IMPORT_BUTTON = "button#gn-import-buttons-import"
EDIT_RECORD_LINK = "a[title='Edit']:has(i.fa.fa-fw.fa-pencil)"


#Add resource file locators
#FILE_INPUT = "input[name='file']"
# Locator for the file input field
FILE_INPUT = "input[type='file'][name='file'][multiple][accept='*.*']"
FILE_CELL_LINK = "xpath=//*[@class='fa external-resource-validation-status-incomplete']"
# Locator for Resource Link by Title
RESOURCE_LINK_BY_TITLE = "a[title='Click to select this resource']:has-text('{resource_name}')"

PROTOCOL_LIST = "#gn-addonlinesrc-protocol-list"

URL_INPUT_FIELD = "input#gn-addonlinesrc-url-list-single-input[placeholder='https://...']"
URL_LINK = "a.truncate.ng-binding[title='{map_path}'][data-ng-click*='addLayer']"

RESOURCE_NAME_INPUT_ENG = "input#gn-addonlinesrc-name-multilingual-eng[lang='eng'][data-ng-model='params.name[val]']"
RESOURCE_NAME_INPUT_FRA = "input#gn-addonlinesrc-name-multilingual-fra[lang='fra'][data-ng-model='params.name[val]']"

LANGUAGE_SWITCH_FR = "role=link[name='Français']"

RESOURCE_NAME_ALL_LINK = "#gn-addonlinesrc-name-multilingual-row a[role='link'][name='All']"
# Locator for Content Type Input Field (English)
CONTENT_TYPE_INPUT_ENG = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_ContentTypes'][lang='eng'][placeholder='Type or search ...']"
CONTENT_TYPE_OPTION_ENG = "strong.tt-highlight:has-text('{option}')"

# Locator for Content Type Input Field (French)
CONTENT_TYPE_INPUT_FRA = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_ContentTypes'][lang='fra'][placeholder='Type or search ...']"

# Locator for Format Input Field (English)
FORMAT_INPUT_ENG = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_Formats'][lang='eng'][placeholder='Type or search ...']"
FORMAT_OPTION_ENG = "strong.tt-highlight:has-text('{option}')"
# Locator for Format Input Field (French)
FORMAT_INPUT_FRA = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_Formats'][lang='fra'][placeholder='Type or search ...']"

# Locator for Language Input Field (English)
LANGUAGE_INPUT_ENG = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_Languages'][lang='eng'][placeholder='Type or search ...']"
LANGUAGE_OPTION_ENG = "strong.tt-highlight:has-text('{option}')"
# Locator for Language Input Field (French)
LANGUAGE_INPUT_FRA = "input[data-gn-keyword-picker][data-thesaurus-key='external.theme.GC_Resource_Languages'][lang='fra'][placeholder='Type or search ...']"


FUNCTION_LIST = "#gn-addonlinesrc-function-list"
#ADD_ONLINE_RESOURCE_BUTTON = "role=button[name='   Add online resource']"
ADD_ONLINE_RESOURCE_BUTTON = "#gn-addonlinesrc-add-button"

# Locator for "Add a Thumbnail" Radio Button
ADD_THUMBNAIL_RADIO_BUTTON = "label.radio-inline:has-text('Add a thumbnail') input[type='radio'][name='linkType']"