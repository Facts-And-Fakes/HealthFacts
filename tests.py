import json

country = "serbia"
print("country:", country)
doc_type = "national_id"
isStatewise = "True"
input_length = 2
path_modules = r"E:\demo3\modules"
json_path = r"countryDictionary.json"


def createDict(country_list, json_path):
    countryDictionary = {
                            "country": country,
                            "documents": [
                                {
                                    "doc_type": doc_type,
                                    "isStatewise": isStatewise
                                }
                            ]
                        },

    country_list.extend(countryDictionary)
    with open(json_path, "w") as f:
        return json.dump(country_list, f, indent=4)


def extendDocument(doc, country_list):
    print("doc", doc)
    new_doc = {
        "doc_type": f"{doc_type}",
        "isStatewise": f"{isStatewise}"
    }

    doc["documents"].append(new_doc.copy())

    with open(json_path, "w") as f:
        return json.dump(country_list, f, indent=4)


def Read(json_path):
    with open(json_path, "r") as file:
        country_list = json.load(file)
        print("country_list1:", country_list)
    return country_list


def checkValueInJson(country_list, json_path):
    print("inside checkValueInJson")
    json_file = Read(json_path)
    print("json_file", json_file)

    for obj in country_list:
        print("country2 : ", country)
        print("country_list2:", country_list)

        if country_list == country:

            print(f"{country} exists in json")

            # check doc_type exists or not method
            for doc in obj["documents"]:

                if doc["doc_type"] == f"{doc_type}":
                    print(f"{doc_type} found in {country}")
                    break
                    # break
                # print("Doctype found")

                else:
                    print(f"{doc_type} does not found for {country}")
                    # if country exist and document does not exit then it will add document
                    return extendDocument(obj, country_list)


        else:
            print(f"{country} does not exist in json1")
            return createDict(country_list, json_path)
            break


    else:
        print(f"{country} does not exist in json2")


checkValueInJson(country, json_path)