import requests
import json
import time


def postRequest(url, bearer_token, request_body=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }
    if request_body:
        response = requests.post(url, headers=headers, data=json.dumps(request_body))
    else:
        response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def login(url, request_body):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def getRequest(url, bearer_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_test_case_id_by_name(test_cases, name):
    for test_case in test_cases:
        if test_case['name'] == name:
            return test_case
    return None

def main():

    try:
        hostname = input("Please enter the TAP hostname or IP Address..")
        username = input("Enter the TAP username..")
        password = input("Enter the TAP password..")

        req_body = {"username":username,"password":password}
        response = login("http://"+hostname+":8080/onPOINT/api/login",req_body)
        print(response)
        bearer_token = response["response"]["accessToken"]

        # Get ALl Test Cases
        response1 = getRequest("http://"+hostname+":8080/onPOINT/v1/testCases/", bearer_token)
    
        # Parse response1 to get data for the next API call
        test_cases = response1["response"]["testCases"]

        for test_case in test_cases:
            print(f"  {test_case['name']}")

        test_case_to_execute = input("Please enter the name of the Test Case which you want to execute: ")

        test_case = get_test_case_id_by_name(test_cases,test_case_to_execute)
        testCase_id = test_case['id']
        response2 = getRequest("http://"+hostname+":8080/onPOINT/v1/testCases/"+testCase_id+"/requiredResource", bearer_token)

        print(f" Choose the Devices required to execute the Test case : ")
        resources = response2["response"]["resources"]
        #resources_to_use = resources
        for resource in resources:
            print(" ")
            print(f"Tag Name    : {resource['name']}")
            print(f"Device Type : {resource['type']}")
            print(f"Vendor      : {resource['vendor']}")
            print(f"Model       : {resource['model']}")
            time.sleep(1)
            print("    Available Devices:")
            for device in resource["availableDevices"]:
                print(f"        {device}")
            time.sleep(1)
            deviceToUse = input(f"  Choose the device you want to use {resource['name']}: ")
            resource["deviceToUse"] = deviceToUse
            del resource["availableDevices"]
            
        time.sleep(3)
        print("")
        print("***************************************************************")
        print("")
        
        # Execute the test case
        response3 = postRequest("http://"+hostname+":8080/onPOINT/v1/testCases/" + testCase_id + "/execute", bearer_token,resources)

        # Check execution status and wait for completion
        if response3['success'] == True:
            print(f"Test case - {test_case_to_execute} started successfully")
            print(f"Execution will take a maximum of {test_case['estimatedTime']} seconds to complete. Please wait....")
            iterations = 0
            wait_time = 5
            while iterations < test_case['estimatedTime']:
                time.sleep(wait_time)
                iterations += 5
                response4 = getRequest("http://"+hostname+":8080/onPOINT/v1/testCases/" + testCase_id + "/status",
                                       bearer_token)
                if response4['response']['status'] == "COMPLETED":
                    response5 = getRequest("http://"+hostname+":8080/onPOINT/v1/testCases/" + testCase_id + "/result",
                                           bearer_token)
                    print("")
                    print(f"Test case - {test_case_to_execute} execution completed")
                    print(f"Result : {response5['response']['subResult']['status']}")
                    print("")
                    print(f"{'Action':<20} | {'Result':<10}")
                    print("")
                    for result in response5['response']['subResult']['actionReportDtos']:
                        action = result['action']
                        result_status = result['result']
                        print(f"{action:<20} | {result_status:<10}")
                    break

        else:
            print(response3['response']['message'])
    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")

if __name__ == "__main__":
    main()
