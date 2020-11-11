# """
# 08 June 2019
#
# Scythron
#
# This class is used to read and write to our data file used for any
# of our data storage requirements
#
# """
#
# import os
# import json
#
# import keys
#
#
# class DataRW:
#     def __init__(self, datafileName='data.file'):
#         """
#         Constructor
#
#         Parameters:
#         -----------
#         datafileName : String
#             The name of the file where the metadata is stored
#         """
#         # Create the class variables
#         self.datafileName = datafileName
#
#         # Create the data file if it doesn't already exist
#         if not os.path.exists(self.datafileName):
#             f = open(self.datafileName, 'w')
#             f.close()
#
#     def writeData(self, data):
#         """
#         This function is used to append metadata to the data file
#
#         Parameters:
#         -----------
#         data : dict
#             A dictionary object containing all of the metadata for
#             a particular code
#
#         Returns:
#         --------
#         """
#         # Need to know if there's data already written to the file
#         f = open(self.datafileName, 'r')
#         lines = f.readlines()
#         f.close()
#
#         # Newline logic
#         if len(lines) > 0:
#             if lines[0] == '':
#                 s = ''
#             else:
#                 s = '\n'
#         else:
#             s = ''
#
#         # Write dict to json string, then to file
#         f = open(self.datafileName, 'a')
#         s += json.dumps(data)
#         f.write(s)
#         f.close()
#
#     def comboExists(self, title, type):
#         """
#         Function used to identify whether a given title and type
#         combination is already stored in our data file
#
#         Parameters:
#         -----------
#         title : String
#             The outlet title
#         type : String
#             The type of outlet code (ON / OFF)
#
#         Returns:
#         --------
#         <value> : Boolean
#             True if the title-type combination already exists and
#             False otherwise
#         """
#         f = open(self.datafileName, 'r')
#         lines = f.readlines()
#         f.close()
#
#         for line in lines:
#             data = json.loads(line)
#
#             if data[keys.OUTLET_TITLE] == title and data[keys.TYPE] == type:
#                 return True
#
#         return False
#
#     def exists(self, title):
#         """
#         Function used to identify whether a given title is already
#         stored in our data file
#
#         Parameters:
#         -----------
#         title : String
#             The outlet title
#
#         Returns:
#         --------
#         <value> : Boolean
#             True if the title already exists and False otherwise
#         """
#         return self.comboExists(title, keys.TYPE_CODE_ON) | self.comboExists(title, keys.TYPE_CODE_OFF)
#
#     def remove(self, title):
#         """
#         Function used to remove a specific code from the data file
#
#         Parameters:
#         -----------
#         title : String
#             The outlet title
#
#         Returns:
#         --------
#         """
#         f = open(self.datafileName, 'r')
#         lines = f.readlines()
#         f.close()
#
#         out = []
#
#         for line in lines:
#             data = json.loads(line)
#
#             if data[keys.OUTLET_TITLE] != title:
#                 out.append(line)
#
#         f = open(self.datafileName, 'w')
#         f.writelines(out)
#         f.close()
#
#     def getTitles(self):
#         """
#         Function used to retrieve the list of titles, sorted
#         alphabetically
#
#         Parameters:
#         -----------
#
#         Returns:
#         --------
#         <value> : 1D list
#             Alphabetically sorted list of titles
#         """
#         f = open(self.datafileName, 'r')
#         lines = f.readlines()
#         f.close()
#
#         titles = []
#
#         for line in lines:
#             data = json.loads(line)
#
#             if data[keys.OUTLET_TITLE] not in titles:
#                 titles.append(data[keys.OUTLET_TITLE])
#
#         titles.sort()
#
#         return titles
#
#     def _getParameters(self, title, type):
#         """
#         Function used to get the list of parameters associated
#         with the specified title for the specified type
#
#         Parameters:
#         -----------
#         title : String
#             The string corresponding to the data's OUTLET_TITLE
#         type : String
#             The string corresponding to the data's TYPE
#
#         Returns:
#         --------
#         <data> : tuple
#             The CODE, ONE_HIGH_TIME, ONE_LOW_TIME, ZERO_HIGH_TIME,
#             ZERO_LOW_TIME, INTERVAL corresponding to the particular
#             title and type
#         """
#         f = open(self.datafileName, 'r')
#         lines = f.readlines()
#         f.close()
#
#         for line in lines:
#             data = json.loads(line)
#
#             if data[keys.OUTLET_TITLE] == title and data[keys.TYPE] == type:
#                 output = (data[keys.CODE], data[keys.ONE_HIGH_TIME],
#                           data[keys.ONE_LOW_TIME], data[keys.ZERO_HIGH_TIME],
#                           data[keys.ZERO_LOW_TIME], data[keys.INTERVAL])
#                 break
#
#         return output
#
#     def getOnParameters(self, title):
#         """
#         Function used to get the list of parameters associated
#         with the particular title for the ON code
#
#         Parameters:
#         -----------
#         title : String
#             The string corresponding to the data's OUTLET_TITLE
#
#         Returns:
#         --------
#         <data> : tuple
#             The CODE, ONE_HIGH_TIME, ONE_LOW_TIME, ZERO_HIGH_TIME,
#             ZERO_LOW_TIME, INTERVAL corresponding to the particular
#             title
#         """
#         return self._getParameters(title, keys.TYPE_CODE_ON)
#
#     def getOffParameters(self, title):
#         """
#         Function used to get the list of parameters associated
#         with the particular title for the ON code
#
#         Parameters:
#         -----------
#         title : String
#             The string corresponding to the data's OUTLET_TITLE
#
#         Returns:
#         --------
#         <data> : tuple
#             The CODE, ONE_HIGH_TIME, ONE_LOW_TIME, ZERO_HIGH_TIME,
#             ZERO_LOW_TIME, INTERVAL corresponding to the particular
#             title
#         """
#         return self._getParameters(title, keys.TYPE_CODE_OFF)
