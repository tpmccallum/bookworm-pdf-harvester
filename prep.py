from datetime import date, datetime
import json
import sys

fields_to_derive = []

def ParseFieldDescs():
    f = open('files/metadata/field_descriptions.json', 'r')
    try:
        fields = json.loads(f.read())
    except ValueError:
        raise ValueError("Error parsing JSON: Check to make sure that your field_descriptions.json file is valid?")
    f.close()

    derivedFile = open('files/metadata/field_descriptions_derived.json', 'w')
    output = []

    for field in fields:
        if field["datatype"] == "time":
            if "derived" in field:
                fields_to_derive.append(field)
            else:
                output.append(field)
        else:
            output.append(field)

    for field in fields_to_derive:
        for derive in field["derived"]:
            if "aggregate" in derive:
                tmp = dict(datatype="time", type="integer", unique=True)
                tmp["field"] = '_'.join([field["field"], derive["resolution"],
                                         derive["aggregate"]])
                output.append(tmp)
            else:
                tmp = dict(datatype="time", type="integer", unique=True)
                tmp["field"] = '_'.join([field["field"], derive["resolution"]])
                output.append(tmp)
    derivedFile.write(json.dumps(output))
    derivedFile.close()

ParseFieldDescs()
