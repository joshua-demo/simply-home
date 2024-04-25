def updateDocumentation(apiEndpoint: str, bio: str, parameters: list[str], apiType="POST", returns=""):
    """
    Updates the documentation file with the new API endpoint
    apiEndpoint is the name that the API endpoint will have
    bio is a brief description of what the API endpoint does
    parameters is a list of strings in the format of "type name: description"
    apiType is the type of API endpoint, either GET or POST
    returns is the type of data that the API endpoint returns if it is a GET request in the format of "{responseJSON} : description"
    """

    with open("documentation.txt", "a") as file:
        file.write(f"\n{apiType} /{apiEndpoint}\n")
        file.write(f"{bio}\n")
        file.write("Parameters:\n")
        for parameter in parameters:
            file.write(f"{parameter}\n")
        
        if apiType == "GET":
            file.write("Returns:\n")
            file.write(f"{returns}:\n")

if __name__ == "__main__":
    updateDocumentation("test", "This is a test", ["String test1: this is a test", "int test2: this is a test 2"],  apiType="GET", returns="{test3} : this is a test response")