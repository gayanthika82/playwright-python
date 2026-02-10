import pytest
from playwright.sync_api import Page
import os
from utils.common_utils import CommonUtils

@pytest.mark.test_case_ids([73299,74298,74658,78091,78667,78834,79060,85123,86159,86409])
def test_login(page_setup) -> None:
    page= page_setup
    userId = os.getenv("USERNAME_REVIEWER_A")
    if not userId:
        raise ValueError("USERNAME_REVIEWER_A environment variable is not set")
    common_utils = CommonUtils(page)
    common_utils.login(userId)
   
