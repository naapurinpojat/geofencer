*** Settings ***
Library     RequestsLibrary
Library     String
Library     DateTime
Library     Collections
Library     OperatingSystem


*** Variables ***
${ROBOT_RUN_ID}     1234
${BASE_URL}         http://localhost/snowdog
&{CUSTOM_HEADER}    Authorization=0028b076-ca97-44c5-9603-bdfc38e2718e    Content-Type=application/json


*** Test Cases ***
Setup the test environment
    Run Keyword And Ignore Error    Setup Test

Generate Random ROBOT_RUN_ID ID for POST data
    ${rnd} =    Generate Random String    5-10    # Generates a string 5 to 10 characters long
    Set Global Variable    ${ROBOT_RUN_ID}    ${rnd}

Get Version from the api
    ${current_date} =    Get Current Date
    ${response} =    GET    ${BASE_URL}/api/version    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json_string} =    Decode Bytes To String    ${response.content}    ASCII    errors=ignore
    ${match} =    Get Regexp Matches    ${json_string}    {"version":"(.*)"}    1
    Log    message=API Version ${match[0]}

Get Last online from the api
    ${response} =    GET    ${BASE_URL}/api/lastonline    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}
    ${json} =    Decode Bytes To String    ${response.content}    ASCII    errors=ignore
    ${match} =    Get Regexp Matches    ${json}    {"online":"(.*)"}    1
    Log    message=Last online ${match[0]}

Get geojson from the api
    ${response} =    GET    ${BASE_URL}/api/geojson    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}

Download fences
    ${response} =    GET    ${BASE_URL}/map.geojson    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}

Get last known location
    ${response} =    GET    ${BASE_URL}/api/lastlocation    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    Log    ${response.content}

Post location to the api
    ${current_date} =    Get Current Date
    ${formatted_date} =    Convert Date    ${current_date}    result_format=%Y-%m-%dT%H:%M:%S.000Z
    ${dummydata} =    Create Dictionary
    ...    lat=62.8059224833
    ...    lon=22.9163893333
    ...    alt=44.2
    ...    speed=0
    ...    ts=${formatted_date}
    ...    in_area=${ROBOT_RUN_ID}
    ${response} =    POST    ${BASE_URL}/api/location    headers=${CUSTOM_HEADER}    json=${dummydata}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json_string} =    Decode Bytes To String    ${response.content}    ASCII    errors=ignore
    ${match} =    Get Regexp Matches    ${json_string}    {"status":"Ok"}

Check that ROBOT_RUN_ID exists in the API
    ${response} =    GET    ${BASE_URL}/api/geojson    headers=${CUSTOM_HEADER}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json} =    Decode Bytes To String    ${response.content}    ASCII    errors=ignore
    ${match} =    Get Regexp Matches    ${json}    .+(${ROBOT_RUN_ID}).+    1
    Log    ${match}


*** Keywords ***
Setup Test
    Environment Variable Should Be Set    SERVER_ADDR
    ${value} =    Get Environment Variable    SERVER_ADDR
    Set Global Variable    ${BASE_URL}    http://${value}/snowdog
    # Implement any setup steps here
