#!/usr/bin/env python3
# coding=utf-8
from conans import ConanFile, CMake, tools

import os
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')

os.system("chcp 65001")


class wxsqlite3Conan(ConanFile):
    name = "wxsqlite3"
    version = "4.6.0"
    license = "<Put the package license here>"
    author = "daixian<amano_tooko@qq.com>"
    url = "https://github.com/daixian/conan-wxsqlite3"
    description = ""
    topics = ("daixian")
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    generators = "cmake"
    exports_sources = "src/*"

    def source(self):
        # 这里下载这个zip等于从github上的https://github.com/utelle/wxsqlite3
        # 目前对应的版本是4.6.0
        tools.get("https://home.xuexuesoft.com:8010/files/src/wxsqlite3.zip")
        # os.rename('wxsqlite3' , self._source_subfolder)

    def _configure_cmake(self):
        '''
        转换python的设置到CMake
        '''
        cmake = CMake(self)
        # cmake.definitions["CALIB_BUILD_SHARED"] = self.options.shared
        # cmake.definitions["CALIB_BUILD_TESTS"] = self.options.build_test
        return cmake

    def build(self):
        print("进入了build...")
        cmake = self._configure_cmake()
        cmake.configure(source_folder="src")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        # self.copy("*.exe", dst="bin", keep_path=False)

        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.out", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sqlite3"]
