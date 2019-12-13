from readConfig import *

def login_cookies():
    result = requests.post(url=loginurl, data=logindata)
    resultData = json.loads(result.text)
    return resultData, result.cookies

# login_cookies()
# login_Sesson()
# print(login_cookies())
# response, cook = login_cookies()
# print(cook)
# print_json_multi_row(response)
# print("66", response)
# aa = response["responseData"]["roleList"]
# print(aa)
# for i in aa:
#     print(i)
# print_json_multi_row(response)
# userId = response["responseData"]["userId"]
# idToken = response["responseData"]["roleList"][0]["idToken"]
# authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 用户的id
# authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]  # 用户的token值
# hospitalCode = response["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
# orgName = response["responseData"]["roleList"][0]["orgName"]        # 用户所属的科室
# orgId = response["responseData"]["roleList"][0]["orgId"]
# userName = response["responseData"]["userName"]
# mobile = response["responseData"]["mobileTelephone"]
# hospital = response["responseData"]["platformList"][0]["platformName"]  # 获取医院的名字
# itemOrgId = response["responseData"]["itemOrgId"]
# roleName = response["responseData"]["roleList"][0]["roleName"]  # 获取角色
# print(userId, authUserId, authToken, hospitalCode, orgId, userName, mobile, hospital, itemOrgId)
