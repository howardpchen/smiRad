#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
    url = sys.argv[1]
    framerate = sys.argv[2]
    examdate = sys.argv[3]
    patientLast = sys.argv[4]
    patientFirst = sys.argv[5]
    MRN = str(sys.argv[6])
except IndexError:
    print("")
    print("""
               .____________             .___
  ______ _____ |__\______   \_____     __| _/
 /  ___//     \|  ||       _/\__  \   / __ | 
 \___ \|  Y Y  \  ||    |   \ / __ \_/ /_/ | 
/____  >__|_|  /__||____|_  /(____  /\____ | 
     \/      \/           \/      \/      \/ 
""")
    print("Social Media Image Capture for Radiology - upload social media to dicomweb server.")
    print("Usage: smirad.py [url] [framerate] [exam date yyyymmdd] [pt last] [pt first] [mrn]")
    print("")
    exit(1);

# url = "https://vine.co/v/he75ht5j75w"
# framerate = 15
# patientLast = 'Tough'
# patientFirst = 'Guy'
# mrn = '13579135'

from subprocess import check_output

import pycurl, io
pyc = pycurl.Curl()
buf = io.BytesIO()
pyc.setopt(pycurl.SSL_VERIFYPEER, 0)
pyc.setopt(pycurl.SSL_VERIFYHOST, 0)
pyc.setopt(pyc.URL, url)
pyc.setopt(pyc.WRITEFUNCTION, buf.write)
pyc.perform()
content = str(buf.getvalue())
content2 = content.split("\\n")

# extract the mp4 URL

mp4url = ''
for line in content2:
    if "contentUrl" in line:
        mp4url = line.split('" : "')[1].strip()[:-2]

pyc.setopt(pyc.URL, mp4url)

# now get the mp4

mp4filesave = open("temp.mp4", "wb")
pyc.setopt(pyc.WRITEFUNCTION, mp4filesave.write)
pyc.perform()
pyc.close()
mp4filesave.close()

print ('download complete')


import xml.etree.cElementTree as ET, uuid
def makeXML(filename, num):
    uuid_oid = "2.25."+ str(uuid.uuid4().int)    
    dicom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<NativeDicomModel xml:space="preserve">
    <DicomAttribute keyword="FileMetaInformationVersion" tag="00020001" vr="OB">
        <InlineBinary>AAE=</InlineBinary>
    </DicomAttribute>
    <DicomAttribute keyword="TransferSyntaxUID" tag="00020010" vr="UI">
        <Value number="1">1.2.840.10008.1.2.4.50</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SpecificCharacterSet" tag="00080005" vr="CS">
        <Value number="1">ISO_IR 100</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceCreationDate" tag="00080012" vr="DA">
        <Value number="1">20160629</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceCreationTime" tag="00080013" vr="TM">
        <Value number="1">195131</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceNumber" tag="00200013" vr="IS">
        <Value number="1">""" + num.split(".")[0] + """</Value>
    </DicomAttribute>

    <DicomAttribute keyword="SOPClassUID" tag="00080016" vr="UI">
        <Value number="1">1.2.840.10008.5.1.4.1.1.7</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SOPInstanceUID" tag="00080018" vr="UI">
        <Value number="1">""" + uuid_oid + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyDate" tag="00080020" vr="DA">
        <Value number="1">""" + examdate + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesDate" tag="00080021" vr="DA">
        <Value number="1">""" + examdate + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="AcquisitionDate" tag="00080022" vr="DA"/>
    <DicomAttribute keyword="ContentDate" tag="00080023" vr="DA">
        <Value number="1">""" + examdate + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyTime" tag="00080030" vr="TM">
        <Value number="1">111738</Value>
    </DicomAttribute>
    <DicomAttribute keyword="ContentTime" tag="00080033" vr="TM"/>
    <DicomAttribute keyword="AccessionNumber" tag="00080050" vr="SH">
        <Value number="1">1234567</Value>
    </DicomAttribute>
    <DicomAttribute keyword="Modality" tag="00080060" vr="CS">
        <Value number="1">NA</Value>
    </DicomAttribute>
    <DicomAttribute keyword="Manufacturer" tag="00080070" vr="LO"/>
    <DicomAttribute keyword="StudyDescription" tag="00081030" vr="LO">
        <Value number="1">Clinical SoMe</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesInstanceUID" tag="0020000E" vr="UI">
        <Value number="1">1.235</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesNumber" tag="00200011" vr="IS">
        <Value number="1">1</Value>
    </DicomAttribute>    
    <DicomAttribute keyword="SeriesDescription" tag="0008103E" vr="LO">
        <Value number="1">Vine Video</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyInstanceUID" tag="0020000D" vr="UI">
        <Value number="1">2.25.15891845865671282328660651175984383651</Value>
    </DicomAttribute>    
    <DicomAttribute keyword="PatientName" tag="00100010" vr="PN">
        <PersonName number="1">
            <Alphabetic>
                <FamilyName>""" + patientLast + """</FamilyName>
                <GivenName>""" + patientFirst + """</GivenName>
            </Alphabetic>
        </PersonName>
    </DicomAttribute>
    <DicomAttribute keyword="PatientID" tag="00100020" vr="LO">
        <Value number="1">""" + MRN + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PatientBirthDate" tag="00100030" vr="DA">
        <Value number="1">20000630</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PatientSex" tag="00100040" vr="CS">
        <Value number="1">O</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PatientAge" tag="00101010" vr="AS">
        <Value number="1">000D</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PatientIdentityRemoved" tag="00120062" vr="CS">
        <Value number="1">YES</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PixelAspectRatio" tag="00280034" vr="IS">
        <Value number="1">1</Value>
        <Value number="2">1</Value>
    </DicomAttribute>
    <DicomAttribute keyword="BitsAllocated" tag="00280100" vr="US">
        <Value number="1">8</Value>
    </DicomAttribute>
    <DicomAttribute keyword="BitsStored" tag="00280101" vr="US">
        <Value number="1">8</Value>
    </DicomAttribute>
    <DicomAttribute keyword="HighBit" tag="00280102" vr="US">
        <Value number="1">7</Value>
    </DicomAttribute>
    <DicomAttribute keyword="PixelRepresentation" tag="00280103" vr="US">
        <Value number="1">0</Value>
    </DicomAttribute>
    <DicomAttribute keyword="ReasonForStudy" tag="00321030" vr="LO">
        <Value number="1">N/A</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyComments" tag="00324000" vr="LT"/>
</NativeDicomModel>
    """

    f = open(filename, "w")
    f.write(dicom_xml)
    f.close()


import os
from os.path import isfile, join

path = '/home/howard/ownCloud/Documents/Radiology/SIIMHack16/'
os.system('rm -f imgs/*')
os.system('rm -f dcm/*')
print("processing video...")
os.system('ffmpeg -i temp.mp4 -r ' + str(framerate) + ' -s 800x800 imgs/%03d.jpg > /dev/null 2>&1')

allimg = sorted([f for f in os.listdir('imgs/') if isfile(join('imgs/', f))])

print("making DICOMs")

for i in allimg:
    makeXML("temp4.xml", i)
    cmd = 'jpg2dcm -c temp4.xml imgs/' + i + ' dcm/' + i + '.dcm > /dev/null 2>&1'
    os.system(cmd)
    print("Processed", i.split('.')[0], "of", len(allimg))
print("uploading...")

alldicom = sorted([f for f in os.listdir('dcm/') if isfile(join('dcm/', f))])

for i in alldicom:
    cmd = 'curl -H "apikey:0f493fc6-c3f9-4099-9b9c-5abc6f8f8bfd" -H "Content-Type: multipart/related;type=application/dicom" -F "file=@dcm/'+ i + ';type=application/dicom" http://api.hackathon.siim.org/dicom-web/studies/ > /dev/null 2>&1'
    os.system(cmd)

print("done")


