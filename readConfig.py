from settings import ArgParser


def metadata_creator():
    '''
    Use the aforementioned function to read the config file and create a proper metadata from that can be used from all other functions later.

    Returns
    -------
    metadata : TYPE
        DESCRIPTION.

    '''

    Input = ArgParser()
    # Config_Address="config/params.conf"
    Config_Address = Input.parse_args().config
    InputFolder_Address = Input.parse_args().input_folder
    OutputFolder_Address = Input.parse_args().output_folder
    Cloud_Target = Input.parse_args().cloud_target
    Cloud_Address = Input.parse_args().cloud_address
    if Cloud_Target == "gc":
        prefix = "gs://"
    elif Cloud_Target == "aws":
        prefix = "aws: TODO"
        raise Exception("AWS functionality not available at this time")
    if Cloud_Address:
        InputFolder_Address = prefix + Cloud_Address + InputFolder_Address
        OutputFolder_Address = prefix + Cloud_Address + OutputFolder_Address

    meta_list = [Config_Address, InputFolder_Address, OutputFolder_Address]
    return meta_list
