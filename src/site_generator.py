import os, shutil

def copy_static(source, destination):
    if not os.path.exists(source):
        raise Exception("Invalid source directory path")
    
    destination_object_list = os.listdir(destination)
    if destination_object_list:
        shutil.rmtree(destination)
        os.mkdir(destination)

    source_object_list = os.listdir(source)

    for object in source_object_list:
        if os.path.isfile(os.path.join(source, object)):
            file = os.path.join(source, object)
            shutil.copy(file, destination)
        else:
            target_directory = os.path.join(destination, object)
            os.mkdir(target_directory)
            nested_directory = os.path.join(source, object)
            copy_static(nested_directory, target_directory)
