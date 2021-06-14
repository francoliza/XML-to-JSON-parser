#!/home/franco/anaconda3/bin/python


"""
PLEASE READ CAREFULLY

I use xml AND json tools INDEPENDENTLY to make the work more easier

I DO NOT use xml TO json librabry such as xmltodict, pandas, beautiful soup, etc

I make two funtions, one for the seatmap1.xml file and the other one for the seatmap2.xml.

FOR SEATMAP1.XML
For the solution the properties that I choose are: SeatID, Price, the currency type, cabin lass, and availability   


FOR SEATMAP2.XML
For this one I choose: seatID, position, currencyType, price, serviceID and description 

Please run this script with python3 and if do not run pease check the first line and change this directory for your directory which is install python3 in your personal computer

"""

import json
import xml.etree.ElementTree as ET
import sys

def getInformation1(argv):
    root = ET.parse(argv).getroot()

    """
    Desire output:
    {
        "SeatID": "",
        "Availability": "",
        "CabinClass": "",
        "CurrencyType": "",
        "Price": "",
        "Features": ""
    }
    """

    allData = list()

    """
    First I gor the seatID, Features, Availability and CabinClass
    """

    for elem in root.findall('.//'):
        if elem.tag.split('}', 1)[1] == "RowInfo":
            for subElem in elem.findall('.//'):
                if subElem.tag.split('}', 1)[1] == "Summary":
                    data = dict()
                    data["SeatID"] = subElem.attrib["SeatNumber"]
                    data["Availability"] = subElem.attrib["AvailableInd"]
                    data["CabinClass"] = elem.attrib["CabinType"]
                    data["CurrencyCode"] = "No data"
                    data["Price"] = "No data"
                    allData.append(data)
                if subElem.tag.split('}', 1)[1] == "Features":
                    data["Features"] = subElem.text
    counter = 0

    """
    Second, I got the CurrencyType and the Price, that I can't get in the first for loop
    """

    for elem in root.findall('.//'):
        if elem.tag.split("}", 1)[1] == "SeatInfo":
            for subElem in elem.findall('.//'):
                if "Fee" == subElem.tag.split("}", 1)[1]:
                    allData[counter]["CurrencyCode"] = subElem.attrib["CurrencyCode"]
                    allData[counter]["Price"] = subElem.attrib["Amount"]
            counter += 1

    return allData

def getPositions(argv):
    """
        Search for the positions for all Seats
    """
    root = ET.parse(argv).getroot()
    positions = dict()

    for elem in root.findall(".//"):
        if elem.tag.split("}", 1)[1] == "Columns":
            positions[elem.attrib["Position"]] = elem.text

    return positions

def getSeatDefinitions(argv):
    root = ET.parse(argv).getroot()
    definitions = dict()
    """
        Search for the definions of every Seat
    """

    for elem in root.findall('.//'):
        if elem.tag.split("}", 1)[1] == "SeatDefinition":
            for subElem in elem.findall('.//'):
                if subElem.tag.split("}", 1)[1] == "Text":
                    definitions[elem.attrib["SeatDefinitionID"]] = subElem.text
            "WINDOW",
            "AVAILABLE",
            "SEAT_NOT_SUITABLE_FOR_CHILD",
            "SEAT_NOT_ALLOWED_FOR_INFANT",
            "WING",
            "SEAT_NOT_ALLOWED_FOR_MEDICAL",
            "EXIT",
            "LEG_SPACE_SEAT"
 
    return definitions

def getOfferItemID(argv):
    """
        This functions search, the serviceID, the currency code and the price
    """
    root = ET.parse(argv).getroot()
    offers = dict()

    for elem in root.findall('.//'):
        if elem.tag.split("}", 1)[1] == "ALaCarteOfferItem":
            for subElem in elem.findall(".//"):
                if subElem.tag.split("}", 1)[1] == "SimpleCurrencyPrice":
                    data = dict()
                    data["Currency"] = subElem.attrib["Code"]
                    data["Price"] = subElem.text
                    offers[elem.attrib["OfferItemID"]] = data
                if subElem.tag.split("}", 1)[1] == "Service":
                    data["Service"] = subElem.attrib["ServiceID"]

    return offers

def getInformation2(argv):
    root = ET.parse(argv).getroot()
    """
        Output example
        "SeatID": "",
        "Position": "",
        "CurrencyCode": "",
        "Price": "",
        "ServiceID": "",
        "Description": []
    """

    
    allData = list()
    seatPositions = getPositions(argv)
    seatDescriptions = getSeatDefinitions(argv)
    offersAndItems = getOfferItemID(argv)


    for elem in root.findall('.//'):
        if elem.tag.split("}", 1)[1] == "Row":
            for subElem in elem.findall('.//'):
                if subElem.tag.split("}", 1)[1] == "Column":
                    data = dict()
                    data["SeatID"] = elem[0].text + subElem.text
                    data["Position"] = seatPositions[subElem.text]
                    data["CurrencyCode"] = "No data"
                    data["Price"] = "No data"
                    data["ServiceID"] = "No data"
                    data["Description"] = list()
                    allData.append(data)
                if subElem.tag.split("}", 1)[1] == "SeatDefinitionRef" :
                    data["Description"].append(seatDescriptions[subElem.text])
                if subElem.tag.split("}", 1)[1] == "OfferItemRefs":
                    data["CurrencyCode"] = offersAndItems[subElem.text]["Currency"]
                    data["Price"] = offersAndItems[subElem.text]["Price"]
                    data["ServiceID"] = offersAndItems[subElem.text]["Service"]

                    

    return allData

def main():
    allTheData = list()

    if sys.argv[1] == "seatmap1.xml":
        allTheData = getInformation1(sys.argv[1])
        
        with open(sys.argv[1] + "_parsed.json", "w") as outfile:
            json.dump(allTheData, outfile, indent=4) 

    elif sys.argv[1] == "seatmap2.xml":
        allTheData = getInformation2(sys.argv[1])
        with open(sys.argv[1] + "_parsed.json", "w") as outfile:
            json.dump(allTheData, outfile, indent=4)


if __name__ == "__main__":
    main()