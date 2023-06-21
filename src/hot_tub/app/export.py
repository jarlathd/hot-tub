"""
Builds TDAU xml setup file
"""

from lxml import etree as ET

def add_TDAU_subelement(root, interval, samples):
    ET.SubElement(root, 'FirmwareVersion', condition='GREATER_EQUAL').text = '1.16'
    ET.SubElement(root, 'Operations').text = 'MARK_READ'
    ET.SubElement(root, 'MarkReadDelay').text = '10'
    ET.SubElement(root, 'StatisticType').text = 'MIN MAX AVG LAST'
    ET.SubElement(root, 'NumberOfDataPoints').text = '1'
    ET.SubElement(root, 'SamplingInterval').text = '20'
    ET.SubElement(root, 'TriggerDelayTime').text = '0'
    ET.SubElement(root, 'BaseVoltageOffset').text = '0'
    ET.SubElement(root, 'TriggerDelayActive').text = 'false'
    ET.SubElement(root, 'AutoCalOnFailingEdge').text = 'false'
    ET.SubElement(root, 'HardwareTrigger').text = 'true'
    ET.SubElement(root, 'SoftwareTrigger').text = 'true'
    ET.SubElement(root, 'LogAveragedTemperature').text = 'false'
    ET.SubElement(root, 'ContinuousRead').text = 'true'
    ET.SubElement(root, 'EnableLogBuffer').text = 'true'
    ET.SubElement(root, 'LeakageCurrentRangeChecking').text = 'false'
    ET.SubElement(root, 'BaseCurrentRangeChecking').text = 'false'
    ET.SubElement(root, 'BJTTemperatureRangeChecking').text = 'false'
    ET.SubElement(root, 'SCOCActive').text = 'true'
    ET.SubElement(root, 'SCOCAutoStartConv').text = 'true'
    ET.SubElement(root, 'SCOCSamplingInterval').text = interval
    ET.SubElement(root, 'SCOCNumberOfSamples').text = samples
    ET.SubElement(root, 'TDAUMeasurementIntegrityActive').text = 'true'
    ET.SubElement(root, 'TDAUMeasurementIntegrityLow').text = '127'
    ET.SubElement(root, 'TDAUMeasurementIntegrityHigh').text = '200'
    ET.SubElement(root, 'DumpAllParametricData').text = 'false'
    return root

def add_CARD_subelement(root):
    card_setup_vec = ET.SubElement(root, 'CardSetupVec')
    card = ET.SubElement(card_setup_vec, 'Card')
    ET.SubElement(card, 'SlaveAddress').text = '0x6E,0x6F'
    diode_setup_vec = ET.SubElement(card, 'DiodesSetupVec')
    return diode_setup_vec

def add_DIODE_subelement(root, data_dict):
    nroot = ET.SubElement(root, 'Diode')
    ET.SubElement(nroot, 'DiodeName').text = str(data_dict['tdau'])
    ET.SubElement(nroot, 'UpperTolerance').text = '99.0'
    ET.SubElement(nroot, 'LowerTolerance').text = '99.0'
    ET.SubElement(nroot, 'Channel').text = str(data_dict['channel'])
    ET.SubElement(nroot, 'Ideality').text = str(data_dict['ideality'])
    ET.SubElement(nroot, 'EarlyVoltage').text = '0'
    ET.SubElement(nroot, 'TemperatureOffset').text = '0'
    ET.SubElement(nroot, 'BaseVoltageOffset').text = '0'

    ncurrents = data_dict['current']

    for idx, current in enumerate(ncurrents):
        ET.SubElement(nroot, f'EmitterCurrent{idx+1}').text = str(current)

    ET.SubElement(nroot, 'EquationSelectBits').text = 'false'
    ET.SubElement(nroot, 'ExtendedEquationSelectBits').text = 'true'
    ET.SubElement(nroot, 'BaseLeakageCompensation').text = 'true'
    ET.SubElement(nroot, 'EquationSlope').text = str(data_dict['slope'])
    return root

def write_setup_file(product_name, tdau_list):
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance'
    xsi = ET.QName(xsi_ns, 'noNamespaceSchemaLocation')
    root = ET.Element(ET.QName(None, 'setups'), attrib={xsi: 'GEN_TDAU_HDMTG2_tt.xsd'}, nsmap={'xsi': xsi_ns})

    interval = '20'
    samples = '20'

    tdau_cold = ET.SubElement(root, 'TDAU', name = 'COLD')
    add_TDAU_subelement(tdau_cold, interval, samples)
    card_setup_cold = add_CARD_subelement(tdau_cold)

    tdau_hot = ET.SubElement(root, 'TDAU', name = 'HOT')
    add_TDAU_subelement(tdau_hot, interval, samples)
    card_setup_hot = add_CARD_subelement(tdau_hot)

    for dict in tdau_list:
        if int(dict['temp']) <= 0:
            add_DIODE_subelement(card_setup_cold, dict)
        else:
            add_DIODE_subelement(card_setup_hot, dict)

    xml_doc = ET.ElementTree(root)
    return xml_doc.write(f'{product_name}_sort_tdau_input.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)