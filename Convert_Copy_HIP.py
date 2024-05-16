# This is shelf tool for houdini that will find nodes with file paths that are absolute.
# It will have a button to show absolute file paths.
# A button that will show the relative paths #HIP and #HOME.  
# The tool will have a button that will then copy them to the relevent folders and convert the file paths to the relative $HIP directory.
# It will list the files converted and copied.


import os
import re
import shutil
from PySide2 import QtCore, QtWidgets

import hou

hipdir = hou.getenv("HIP")
homedir = hou.getenv("HOME")

def getHoudiniMainWindow():
    return hou.ui.mainQtWindow()

class ConvertHIP(QtWidgets.QWidget):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ConvertHIP()
        return cls._instance
    
    def __init__(self):
        parent = getHoudiniMainWindow()
        super(ConvertHIP, self).__init__(parent)
        self.setObjectName('ConvertHIP')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Convert to HIP')
        layout = QtWidgets.QVBoxLayout()

        # Obtaining file paths 
        find_abspath_button = QtWidgets.QPushButton('Find Absolute Paths')
        find_relpath_button = QtWidgets.QPushButton('Find Relative Path')
        
        layout.addWidget(find_abspath_button)
        layout.addWidget(find_relpath_button)

        #Show Paths found
        self.data_label = QtWidgets.QLabel()
        layout.addWidget(self.data_label)

        # Action
        self.apply_buttons = QtWidgets.QPushButton('Copy and Convert')
        layout.addWidget(self.apply_buttons)

        self.setLayout(layout)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        #Connect buttons to functions
        find_abspath_button.clicked.connect(self.find_non_relative_paths)
        find_relpath_button.clicked.connect(self.find_relative_path)
        self.apply_buttons.clicked.connect(self.Copy_and_Convert)

    def find_non_relative_paths(self):
        non_relative_paths = []
        excluded_extensions = ('.cl',) # Add other extensions to exclude as needed

        fileRefs = hou.fileReferences()
        for parm, path in fileRefs:
            if not (path.startswith("$JOB") or path.startswith("$HIP")):
                #Check if path has excluded extension
                if not path.lower().endswith(excluded_extensions):
                    non_relative_paths.append(path)
                
        # Display absolute paths        
        self.data_label.setText("\n".join(non_relative_paths))

    def find_relative_path(self):

        #Display relative project path
        self.data_label.setText(f"HIP directory: {hipdir}\nHome directory: {homedir}")

    def Copy_and_Convert(self, paths):

        texture_extensions = ('.jpeg', '.jpg', '.png', '.exr', '.hdr', '.tif', '.targa')
        geometry_extensions = ('.obj', '.fbx', '.abc')
        cache_extensions = ('.bgeo', '.bgeo.sc', '.geo', '.vdb')

        existing_tex_files = []
        existing_geo_files = []
        existing_cache_files = []

        filesRefs = hou.fileReferences()
        for parm, path in filesRefs:
            if (path.lower().endswith(texture_extensions) or
                path.lower().endswith(geometry_extensions) or
                path.lower().endswith(cache_extensions)):
                
                parmName = parm.name()
                parmPath = parm.path()
                filePath = path
                selNode = parm.node()

                #Skip files that endwith the extension but dont start with the path.
                if not os.path.isfile(filePath):
                    print(f"File {filePath} does not exist. Skipping...")
                    continue

                if not (path.startswith("$JOB") or path.startswith("$HIP")):

                    #Obtain file name with extension
                    file_name_with_extensions = os.path.basename(path)

                    if path.lower().endswith(texture_extensions):
                        base_folder = 'tex'
                        existing_files = existing_tex_files
                    elif path.lower().endswith(geometry_extensions):
                        base_folder = 'geo'
                        existing_files = existing_geo_files
                    elif path.lower().endswith(cache_extensions):
                        base_folder = 'geo'
                        existing_files = existing_cache_files

                        subfolder = parmPath.split('/')[3]

                        # re-remove '_' and extension

                        subfolder = re.sub(r'_\d+', '', subfolder)

                        base_folder = os.path.join('geo', subfolder)

                    else:
                        base_folder = ''
                    
                    if path.startswith("$HOME"):
                        filePath = path.replace("$HOME", homedir)
                        filePath = os.path.abspath(filePath)

                    #create sub-folder

                    path_folder = os.path.join(hipdir, base_folder)

                    if not os.path.exists(path_folder):
                        os.makedirs(path_folder)

                    # New file path
                    fileAppend = os.path.join(path_folder, file_name_with_extensions)

                    #Check if file already exists
                    if os.path.exists(fileAppend):
                        existing_files.append(fileAppend)
                    else:
                        try:
                            if not os.path.abspath(filePath) == os.path.abspath(fileAppend):

                                shutil.copyfile(filePath, fileAppend) #Copy single file
                                existing_files.append(fileAppend) #Append the copied file/folder
                        except IOError as e:
                            print(f"Error copying: {e}")

                    if path.lower().endswith(cache_extensions):
                        relativePath = os.path.join("$HIP", base_folder)
                    else:
                        relativePath = os.path.join("$HIP", base_folder, file_name_with_extensions)

                    # Set the parm to the new path
                        selNode.parm(parmName).set(relativePath)

            self.data_label.setText("All files converted and copied successfully")


def close_existing_window(object_name):
    main_window = getHoudiniMainWindow()
    for widget in main_window.findChildren(QtWidgets.QWidget, object_name):
        widget.close()
        widget.deleteLater()

def run():
    close_existing_window("Convert to HIP")
    win = ConvertHIP.get_instance()
    win.show()

run()