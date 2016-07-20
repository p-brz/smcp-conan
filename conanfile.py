from conans import ConanFile, ConfigureEnvironment
from conans.util.log import logger
import os
from os import path

class SmcpConan(ConanFile):
    name = "smcp"
    version = "0.6.5-36-ge40a65f" # from git describe
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        # Define DEBUG_VERBOSE to make smcp print debug messages during runtime
        "verbose" : [True, False]
    } 
    default_options = "verbose=False"
     
    #Url of package
    url="https://github.com/paulobrizolara/smcp-conan.git"

    #The smcp repository
    #REPO = "https://github.com/darconeous/smcp/"
    REPO = "https://github.com/paulobrizolara/smcp/" #Using fork

    #Point on repository history
    COMMIT = "e40a65ff1"

    #Name of install directory
    INSTALL_DIR = 'install_dir'

    def config(self):
        #TODO: allow to use more options from the configure script

        configs = []
                    
        if self.settings.build_type == "Debug":
            configs.append("--enable-debug")
        
        if self.options.verbose:
            self.deps_cpp_info.cflags.append("-DVERBOSE_DEBUG")
            #configs.append("-DVERBOSE_DEBUG")
                
        self.configs = configs


    def source(self):
        # Clone the repository
        self.run("git clone %s" % self.REPO)

        #Checkout history point of current version
        os.chdir("smcp")
        self.run("git checkout %s" % self.COMMIT)

        if not path.exists("configure"):
            self.run(path.join(".", "bootstrap.sh"))

    def build(self):
        if not hasattr(self, 'configs'):
            self.config()

        # This the directory where make will install the built library
        install_path = self._make_install_path()
        self.configs.append("--prefix=%s" % install_path)

        # Build the project
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        env_cmd = env.command_line

        configure_path = path.join(".", "smcp", "configure")

        self.run("%s %s %s"         % (env_cmd, configure_path, " ".join(self.configs)))
        self.run("%s make"          % env_cmd)
        self.run("%s make install"  % env_cmd)

    def package(self):
        #Copy all install dir content to the package directory
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = ["smcp"]


    def _make_install_path(self):
        install_path = os.path.join(os.getcwd(), self.INSTALL_DIR)
        try:
            os.mkdir(install_path)
        except OSError:
            print("install dir already exist")
            pass

        return install_path
