from conans import ConanFile, ConfigureEnvironment
import os

class SmcpConan(ConanFile):
    name = "smcp"
    version = "0.6.5"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"

    #Url of package
    url="https://github.com/paulobrizolara/smcp-conan.git"

    #The smcp repository
    REPO = "https://github.com/darconeous/smcp/"
    #Release tag on repository
    RELEASE = "0.6.5-release"

    #Name of install directory
    INSTALL_DIR = 'install_dir'

    def source(self):
        # Clone the repository
        self.run("git clone %s" % self.REPO)

        #Move to the release tag on the cloned project
        os.chdir("./smcp")
        self.run("git checkout %s" % self.RELEASE)

    def build(self):
        # This the where make will install the built library
        install_path = self._make_install_path()

        #TODO: allow use more options from the configure script
        configs = "--prefix=%s" % install_path

        # Build the project
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        self.run("%s ./smcp/configure %s" % (env.command_line, configs))
        self.run("%s make" % env.command_line)
        self.run("%s make install" % env.command_line)

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
