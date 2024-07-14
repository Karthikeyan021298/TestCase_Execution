This GitHub workflow will invoke the APIs against TekVizion TAP to start the testCase (defined in the variable) and provide the final output of the         workflow.
Incase of errors the final out put will be marked as failure.
Customer workflow will trigger this workflow.
Based on the final output of this flow i.e. success or failure, customer can trigger their subsequent workflows.

Prerequisite :
1. Create a test case and ensure the test case can be executed manually.
2. Get the required devices name for executing test case
2. Copy the yml file to your GitHub repository
3. Ensure the TAP URL is accessible from public IP addresses.

Usage :

1. Update the values for the below variables in the file as per your environment.
   
  TAP_URL: "http://<ip_address>:8080/onPOINT"  # Replace IP address and user credentials with details of your respective environment.
  USERNAME: "<username>"    
  PASSWORD: "<password>"
  TEST_CASE_NAME: "<testCase_name>"  # Replace testCase_name with the actual name of the testCase.
  CHECK_COMPLETION_DELAY: "10" # Polling interval (in sec) for checking testCase completion.
  // Note Add device objects to array as required for your testCase execution the below one is the example
  DEVICES: JSON_BODY: |
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

      


  
2.Currently the workflow needs to be executed manually.
3.This workflow will perform multiple jobs like 
  identifyTestcase : list all the available testcases and get the testCase id for the defined testCase.
  executeTestCase    : start the testCase
  checkcompletion : Periodically check whether the testCase is completed or not.
  workflowstatus  : Based on the Test case execution result the flow will be marked as success or failure. 
4.Customer needs to invoke this workflow from their workflow
5.customer can trigger their subsequent workflows as per their requirement, based on the final out put of this workflow.
6.invoke the subsequent flows based on the output  "workflow_report:"  i.e success or failure, stored as ${{ steps.finalresult.outputs.workflow_report }}"


Note : 
Currently this workflow has to be invoked manually, and customer needs to update the event trigger accordingly to invoke this flow.
Align the time (CHECK_COMPLETION_DELAY)based on the test case completion time to avoid checking the completion status more frequently

