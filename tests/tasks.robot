*** Settings ***
Library    RequestsLibrary
Library    String

*** Variables ***
${BASE_URL}    http://localhost/snowdog/api
&{CUSTOM_HEADER}    Authorization=0028b076-ca97-44c5-9603-bdfc38e2718e

*** Test Cases ***
Get Version from the api
    ${response} =    GET    ${BASE_URL}/version    headers=${CUSTOM_HEADER} 
    Should Be Equal As Strings    ${response.status_code}    200
    ${json} =    Decode Bytes To String    ${response.content}    ASCII    errors=ignore
    ${match}=    Get Regexp Matches    ${json}    {"version":"(.*)"}    1
    Log    message=${match}