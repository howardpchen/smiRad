#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET, uuid, os

## Make Cerv spine XR XML
uuid_oid = "2.25."+ str(uuid.uuid5(uuid.NAMESPACE_OID, "test").int)    
studyUID = str(uuid.uuid5(uuid.NAMESPACE_OID,"test2").int)
dicom_xml = """<?xml version="1.0" encoding="UTF-8"?>
<NativeDicomModel xml:space="preserve">
    <DicomAttribute keyword="FileMetaInformationVersion" tag="00020001" vr="OB">
        <InlineBinary>AAE=</InlineBinary>
    </DicomAttribute>
    <DicomAttribute keyword="TransferSyntaxUID" tag="00020010" vr="UI">
        <Value number="1">1.2.840.10008.1.2.4.81</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SpecificCharacterSet" tag="00080005" vr="CS">
        <Value number="1">ISO_IR 100</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceCreationDate" tag="00080012" vr="DA">
        <Value number="1">20160701</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceCreationTime" tag="00080013" vr="TM">
        <Value number="1">195131</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SOPClassUID" tag="00080016" vr="UI">
        <Value number="1">1.2.840.10008.5.1.4.1.1.7</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SOPInstanceUID" tag="00080018" vr="UI">
        <Value number="1">""" + uuid_oid + """</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyDate" tag="00080020" vr="DA">
        <Value number="1">20160701</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesDate" tag="00080021" vr="DA">
        <Value number="1">20160701</Value>
    </DicomAttribute>
    <DicomAttribute keyword="AcquisitionDate" tag="00080022" vr="DA"/>
    <DicomAttribute keyword="ContentDate" tag="00080023" vr="DA">
        <Value number="1">20160701</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyTime" tag="00080030" vr="TM">
        <Value number="1">111738</Value>
    </DicomAttribute>
    <DicomAttribute keyword="ContentTime" tag="00080033" vr="TM"/>
    <DicomAttribute keyword="AccessionNumber" tag="00080050" vr="SH">
        <Value number="1">654321</Value>
    </DicomAttribute>
    <DicomAttribute keyword="Modality" tag="00080060" vr="CS">
        <Value number="1">XR</Value>
    </DicomAttribute>
        <DicomAttribute keyword="BodyPartExamined" tag="00180015" vr="CS">
        <Value number="1">CERVICAL SPINE</Value>
    </DicomAttribute>

    <DicomAttribute keyword="Manufacturer" tag="00080070" vr="LO"/>
    <DicomAttribute keyword="StudyDescription" tag="00081030" vr="LO">
        <Value number="1">EMERGENCY DEPT</Value>
    </DicomAttribute>
    <DicomAttribute keyword="InstanceNumber" tag="00200013" vr="IS">
        <Value number="1">1</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesInstanceUID" tag="0020000E" vr="UI">
        <Value number="1">1.235</Value>
    </DicomAttribute>
    <DicomAttribute keyword="SeriesNumber" tag="00200011" vr="IS">
        <Value number="1">1</Value>
    </DicomAttribute>    
    <DicomAttribute keyword="SeriesDescription" tag="0008103E" vr="LO">
        <Value number="1">CERV SPINE</Value>
    </DicomAttribute>
    <DicomAttribute keyword="StudyInstanceUID" tag="0020000D" vr="UI">
        <Value number="1">""" + studyUID + """</Value>
    </DicomAttribute>    
    <DicomAttribute keyword="PatientName" tag="00100010" vr="PN">
        <PersonName number="1">
            <Alphabetic>
                <FamilyName>Tough</FamilyName>
                <GivenName>Guy</GivenName>
            </Alphabetic>
        </PersonName>
    </DicomAttribute>
    <DicomAttribute keyword="PatientID" tag="00100020" vr="LO">
        <Value number="1">13579135</Value>
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

f = open("cerv.xml", "w")
f.write(dicom_xml)
f.close()
os.system('jpg2dcm -c cerv.xml cervical.jpg testupload.dcm')
os.system('curl -H "apikey:0f493fc6-c3f9-4099-9b9c-5abc6f8f8bfd" -H "Content-Type: multipart/related;type=application/dicom" -F "file=@testupload.dcm;type=application/dicom" http://api.hackathon.siim.org/dicom-web/studies/ -v')

