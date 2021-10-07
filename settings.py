from argparse import ArgumentParser


class ArgParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self, allow_abbrev=True)

        # with default
        self.add_argument("-c", "--config", help="configuration file to be read",
                          default='etc/config.conf', required=False)
        self.add_argument("-i", "--input_folder", help="input folder to look for the files",
                          default='data',required=False)
        self.add_argument("-o", "--output_folder",
                          default='data',help="Output Folder", required=False)
        self.add_argument("-t", "--cloud-target", help="cloud provider, google is gcp, aws is aws",
                          default='gcp', required=False)
        self.add_argument("-a", "--cloud-address", help="url of cloud bucket e.g. https://gs:my-bucket/",
                          default='gs://my-bucket', required=False)

