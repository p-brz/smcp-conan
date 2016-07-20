from conans import ConanFile, CMake
import os
from shutil import copyfile

username = os.getenv("CONAN_USERNAME", "paulobrizolara")
channel = os.getenv("CONAN_CHANNEL", "testing")
version = "0.6.5-36-ge40a65f"

class SmcpConanTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "smcp/%s@%s/%s" % (version, username, channel)
    generators = "cmake"
    default_options = ""

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin") # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        #Make build dir
        build_dir = os.path.join(".", "build")
        self._try_make_dir(build_dir)

        #Copy
        build_info = "conanbuildinfo.cmake"
        copyfile(build_info, os.path.join(build_dir, build_info))

        #Change to build dir
        os.chdir(build_dir)

        cmake = CMake(self.settings)

        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run('cmake --build . %s' % cmake.build_config)

    def test(self):
        pass

    def _try_make_dir(self, dir):
        try:
            os.mkdir(dir)
        except OSError:
            #dir already exist
            pass
