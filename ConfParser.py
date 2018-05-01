# -*- coding: utf-8 -*-

import lxml.etree as le
import shutil
import glob
from datetime import datetime

template_search = 'InformationRegister*.xml';
dir_search = 'C:\\Users\\Denis\\Dropbox\\OenScript\\ConfParser\\utap_02\\';
log_file_name = 'C:\\Users\\Denis\\Dropbox\\OenScript\\ConfParser\\Conf\\log.txt'
listExpr = [{
                'exp': '//ns:Resource/ns:Properties/ns:Type/v8:StringQualifiers/v8:Length|//ns:Dimension/ns:Properties/ns:Type/v8:StringQualifiers/v8:Length',
                'ns': {'ns': 'http://v8.1c.ru/8.3/MDClasses', 'v8': 'http://v8.1c.ru/8.1/data/core'},
                'validation_value': None, 'value': '10'},
            {
                'exp': '//ns:Resource/ns:Properties/ns:Type/v8:StringQualifiers/v8:Length/parent::*/parent::*/parent::*/ns:Indexing|//ns:Dimension/ns:Properties/ns:Type/v8:StringQualifiers/v8:Length/parent::*/parent::*/parent::*/ns:Indexing',
                'ns': {'ns': 'http://v8.1c.ru/8.3/MDClasses', 'v8': 'http://v8.1c.ru/8.1/data/core'},
                'validation_value': 'Index', 'value': 'DontIndex'}]

def getRoot(xmlFile):
    try:
        return le.parse(xmlFile)
    except:
        log('Ошибка открытия файла: ' + xmlFile)
        return None

def xPathExecute(expr, ns, root, xmlFile):
    try:
        return root.xpath(expr, namespaces=ns)
    except:
        log('Ошибка исполнения выражения XPath: ' + xmlFile)
        return None

def copyFile(xmlFile):
    try:
        current_time = datetime.strftime(datetime.now(), "%Y-%m-%dT%H-%M-%S")
        shutil.copyfile(xmlFile, xmlFile + '.back_' + current_time)
        return True
    except:
        log('Ошибка создания резервной копии файла: ' + xmlFile)
        return False

def xml_write(root, xmlFile):
    obj_xml = le.tostring(root, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    with open(xmlFile, 'wb', ) as fobj:
        fobj.write(obj_xml)

def parseXML(xmlFile):

    root = getRoot(xmlFile)
    if root == None:
        pass

    file_modified = False
    for itemExpr in listExpr:
        res = xPathExecute(itemExpr['exp'], itemExpr['ns'], root, xmlFile)
        for item in res:
            if itemExpr['validation_value'] != None and item.text != itemExpr['value']:
                continue
            else:
                item.text = itemExpr['value']
                file_modified = True

    if file_modified:
        if copyFile(xmlFile):
            xml_write(root, xmlFile)
        else:
            log('Файл не перезаписан: ' + xmlFile)

def getFileList():
    return glob.glob(dir_search + template_search)

def log(msg):
    line = '[ '+datetime.strftime(datetime.now(), "%Y-%m-%dT%H-%M-%S")+' ]: '+msg
    f = open(log_file_name, 'w')
    f.write(line + '\n')

if __name__ == "__main__":
    #git
    fileList = getFileList()
    for item in fileList:
        print(item)
        log('Обработка файла: ' + item)
        parseXML(item)
