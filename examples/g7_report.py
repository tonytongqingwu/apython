"""
This is pseudocode designed to illustrate how the call TestRail endpoints
"""

from testrail_common import TestRailApi

# Configuration
testrail = TestRailApi('https://dexcom.testrail.io/', 'projectid', 'suite')


""" Fetch all appropriate test cases from specified test suite TestRail """
# testrail.testrail_get_all_cases_from_suite()

""" Fet a single test case from TestRail"""
# Case id is a number found in the test suites ex: C1234
# TestRail API only requires the number portion of the case id ex: 1234
case_id = 671384   # g7
# testrail.testrail_get_case(case_id)

""" Get active test run in TestRail """
# Will return test run ID and run name
act_runs = testrail.testrail_get_active_run()
print(act_runs)

""" Create a test run in TestRail """
# Milestone is optional
run_name = "Test Run"
description = "Test run description"
case = testrail.testrail_get_case(case_id)
testrail.testrail_create_run_from_case_list(run_name, description, [case])

act_runs_new = testrail.testrail_get_active_run()
print(act_runs_new)

new_run = new_list = [run for run in act_runs_new if run not in act_runs]

print(new_run[0]['id'])

""" Send bulk results in TestRail """
results = [{
    "case_id": 671384,
    "status_id": 5,
    "comment": "Result comments"
},
]

testrail.testrail_add_bulk_results(int(new_run[0]['id']), results)

# """ Close an active test run in Testrail """
# run_id = 671384
# testrail.testrail_close_active_run(run_id)
