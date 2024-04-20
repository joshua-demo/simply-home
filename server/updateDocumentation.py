def updateDocumentation(apiEndpoint: str, bio: str, parameters: list[str], parameterBios: str, apiType="POST", returns="", returnBio=""):
    with open("documentation.txt", "a") as file:
        file.write(f"\n{apiType} /{apiEndpoint}\n")
        file.write(f"{bio}\n")
        file.write("Parameters:\n")
        for i in range(len(parameters)):
            file.write(f"{parameters[i]}: {parameterBios[i]}\n")
        
        if apiType == "GET":
            file.write("Returns:\n")
            file.write(f"{returns}: {returnBio}\n")