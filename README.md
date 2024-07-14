## GitHub Workflow: Automate TekVizion TAP Test Case Execution

This GitHub workflow automates the execution of a test case on TekVizion TAP and provides the final workflow output. If errors occur during execution, the workflow will be marked as failed. Customers can trigger subsequent workflows based on the success or failure of this workflow.

### Prerequisites

1. Create a test case and ensure it can be executed manually on TekVizion TAP.
2. Obtain the required device names necessary for executing the test case.
3. Copy the provided YAML file into your GitHub repository.
4. Ensure that the TAP URL is accessible from public IP addresses.

### Usage

1. Update the values for the following variables in the YAML file according to your environment:

   ```yaml
   TAP_URL: "http://<ip_address>:8080/onPOINT"  # Replace IP address and user credentials with your environment details.
   USERNAME: "<username>"
   PASSWORD: "<password>"
   TEST_CASE_NAME: "<testCase_name>"  # Replace with the actual name of your test case.
   CHECK_COMPLETION_DELAY: "10"  # Polling interval (in seconds) for checking test case completion.
   DEVICES: |
     [
       {
         "name": "W1",
         "type": "Phone",
         "vendor": "Cisco",
         "model": "WEBEX-TEAMS",
         "submodel": "",
         "deviceToUse": "Webex 40"
       },
       {
         "name": "U1",
         "type": "User",
         "vendor": "",
         "model": "",
         "submodel": "",
         "deviceToUse": "QA-user33"
       }
     ]
Note: Add device objects to the array as required for your specific test case execution.

Manually execute this workflow for now.

This workflow consists of the following jobs:

identifyTestcase: Lists all available test cases and retrieves the test case ID for the specified test case.
executeTestCase: Starts the specified test case execution.
checkcompletion: Periodically checks whether the test case execution is completed.
workflowstatus: Marks the workflow as success or failure based on the test case execution result.
Customers should trigger this workflow from their own workflow.

Based on the outcome (workflow_report), customers can trigger subsequent workflows as needed.

Invoke subsequent workflows based on the output stored as ${{ steps.finalresult.outputs.workflow_report }}.

Note
Currently, this workflow needs to be manually invoked.
Customers should update the event trigger to automate the workflow invocation.
Adjust the CHECK_COMPLETION_DELAY based on the expected completion time of your test case to optimize status checking intervals.
