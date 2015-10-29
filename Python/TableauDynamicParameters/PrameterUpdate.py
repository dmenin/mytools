__author__ = 'Diego Menin'

import ConfigParser
from xml.etree.ElementTree import Element
from xml.etree import ElementTree
from pkg_resources import resource_filename


"""
Updates the values parameter called MyParameter
based on a list returned by __getNewParameterlist()

Args:
    envname: Environment the code is running - not relevant to this example .
    dashboardname: The Dashboard to replace the parameter.

Returns:
    Nothing - outputs one twb file.

Raises:
    Nothing:

TO DO: add popper exception handling
       parameter name should be a parameter on the function

"""
def ParameterUpdate(envname, dashboardname):
    #the 5 lines bellow are optional. It can be used if the Source\Destination Dashboards are expected to be on a
    #different path than the one the python file is executing, which is often the case, but not for this example:
    configfile = resource_filename(__name__, 'tableau.ini')
    config = ConfigParser.ConfigParser()
    config.read(configfile)
    inputdir = config.get(envname, "InputDirectory")
    outputdir = config.get(envname, "OutputDirectory")

    #reads the twb file
    tableaufile = ElementTree.parse('{0}/{1}.twb'.format(inputdir, dashboardname))

    #gets a list with the new parameters
    new_parameter_list = __getNewParameterlist()

    #gets the root XML
    fileroot = tableaufile.getroot()

    #finds the parameter called "MyParameter"
    xmlsection = fileroot.find("datasources/datasource/column[@caption='{0}']/members".format("MyParameter"))

    #Inject the new list into the XML file
    __injectParameters(xmlsection, new_parameter_list)

    newxmlfile = ElementTree.tostring(fileroot, encoding='UTF-8', method='xml')

    filelocation = '{0}/{1}.twb'.format(outputdir, "Output")
    with open(filelocation, 'w') as text_file:
         text_file.write(newxmlfile)


"""
Returns a list of parameters

Returns:
    List
"""
def __getNewParameterlist():
    params = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    return params


"""
Clears the current parameters values (expect for the "None" value)
Appends the new values in "new_par_list" to the parameter

Args:
    xml_section: The dashboard XML Section
    new_par_list: The list of new parameters.

"""
def __injectParameters(xml_section, new_par_list):
    for member in xml_section.findall('member'):
        if member.attrib['value'] != '"None"':
            xml_section.remove(member)

    for new_par in new_par_list:
        new_par = '"' + new_par + '"'
        xml_section.append(Element('member', {'value': new_par}))





if __name__ == '__main__':
    ParameterUpdate('PROD','Original')


