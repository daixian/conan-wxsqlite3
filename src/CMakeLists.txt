cmake_minimum_required(VERSION 3.6)

project(wxSQLite3)

if (NOT DEFINED CONAN_BUILD_INFO_PATH)
    # 在有了project之后需要第一时间搞个conan设置吧
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
endif()

# 由conan控制
# option(STATIC_RUNTIME "link with c++ runtime statically" "ON")
# option(WXSQLITE3_BUILD_SHARED "Build wxSQLite3 as shared library" ON)
# option(BUILD_SHARED_LIBS "Link with shared wxWidgets library" ON)

# if((CMAKE_SIZEOF_VOID_P EQUAL 8) AND CMAKE_COMPILER_IS_GNUCC)
#     option(USE_32 "create 32 bit binaries" "OFF")
# endif()

option(SQLITE_DEBUG "enable SQLite debug" "OFF")
option(PEDANTIC_COMPILER_FLAGS "Enable additional checking for ill-formed code" "ON")
# if(MSVC)
#     option(CPP_EXCEPTIONS_ONLY "Catch only C++ exceptions(/EHsc) instead of catching all exceptions(/EHa)" "ON")
#     option(THREAD_SAVE_STATIC_INIT "Enable thread safe initialization of static variables" "OFF")
# endif(MSVC)
# option(RELEASE_DEBUG_SYMBOLS "Generate debugging symbols for optimized build" "OFF")

#这里下面不写配置了,写死CHACHA20
# set(SQLITE_CODEC_TYPE "DEFAULT" CACHE STRING "DB Codec(AES128, AES256, CHACHA20, DEFAULT)")

# set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE)

set(LIBRARY_SOURCES
    # "../include/wx/wxsqlite3_version.h"
    # "../include/wx/wxsqlite3def.h"
    # "../include/wx/wxsqlite3dyn.h"
    # "../include/wx/wxsqlite3opt.h"
    "./wxsqlite3/sqlite3secure/src/codec.h"
    "./wxsqlite3/sqlite3secure/src/fastpbkdf2.h"
    "./wxsqlite3/sqlite3secure/src/mystdint.h"   
    "./wxsqlite3/sqlite3secure/src/rijndael.h"
    "./wxsqlite3/sqlite3secure/src/sha1.h"
    "./wxsqlite3/sqlite3secure/src/sha2.h"
    "./wxsqlite3/sqlite3secure/src/sqlite3.h"
    "./wxsqlite3/sqlite3secure/src/sqlite3ext.h"
    "./wxsqlite3/sqlite3secure/src/sqlite3secure.h"
    "./wxsqlite3/sqlite3secure/src/sqlite3userauth.h"
    "./wxsqlite3/sqlite3secure/src/test_windirent.h"
    "./wxsqlite3/sqlite3secure/src/sqlite3secure.c"
    # "./wxsqlite3/src/wxsqlite3.cpp"
)

if(WIN32)
    set(LIBRARY_SOURCES
        ${LIBRARY_SOURCES}
        "./wxsqlite3/sqlite3secure/src/sqlite3.rc"
        "./wxsqlite3/sqlite3secure/src/sqlite3.def"
    )
endif(WIN32)

if(MSVC)
    add_compile_options(/Zi     # pdb
                        /W4     # warning level 4
                        /J      # use unsigned char
                        /Gd     # use cdecl
                        # /MP     # multiprocessor compilation
                        /utf-8  # utf-8 source
                        /GF     # eliminate duplicate strings
                        /wd4996 # disable 'The POSIX name for this item is deprecated ...'
    )
                        
    if(PEDANTIC_COMPILER_FLAGS)
        add_compile_options(# treat warnings as errors
                            /we4715 # not all control paths return a value
                            /we4828 # disallow invalid characters
                            # prinf-like functions: format mismatch
                            /we4473 # <function> : not enough arguments passed for format string 
                            /we4474 # <function> : too many arguments passed for format string 
                            /we4475 # <function> : length modifier <length> cannot be used with type field character <conversion-specifier> in format specifier 
                            /we4476 # <function> : unknown type field character <conversion-specifier> in format specifier 
                            /we4477 # <function> : format string <format-string> requires an argument of type <type>, but variadic argument <position> has type <type>
                            /we4478 # <function> : positional and non-positional placeholders cannot be mixed in the same format string 
                            /we4775 # nonstandard extension used in format string <format-string> of function <function>
                            /we4776 # %<conversion-specifier> is not allowed in the format string of function <function> 
                            /we4777 # <function> : format string <format-string> requires an argument of type <type>, but variadic argument <position> has type <type>
                            /we4778 # <function> : unterminated format string <format-string>
                            # macro arg mismatch
                            /we4002 # too many actual parameters for macro 'identifier'
                            /we4003 # not enough actual parameters for macro 'identifier'
        )
    endif(PEDANTIC_COMPILER_FLAGS)
    
    if(CPP_EXCEPTIONS_ONLY)
        add_compile_options(/EHsc) # exceptions: sync
    else()
        add_compile_options(/EHa) # exceptions: sync
    endif(CPP_EXCEPTIONS_ONLY)
    
    # if((NOT THREAD_SAVE_STATIC_INIT) AND (CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 19.00))
    #     add_compile_options(/Zc:threadSafeInit-) # https://connect.microsoft.com/VisualStudio/feedback/details/1789709/visual-c-2015-runtime-broken-on-windows-server-2003-c-11-magic-statics
    # endif()
    
    # set(CMAKE_CXX_FLAGS ${CMAKE_C_FLAGS})
    
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)

elseif(CMAKE_COMPILER_IS_GNUCC)
    add_compile_options(-pipe
                        -funsigned-char
                        -fno-rtti
                        -W
                        -Wall
                        )
                        
    if(PEDANTIC_COMPILER_FLAGS)
        add_compile_options(-Wextra
                            -Wwrite-strings
                            -Wframe-larger-than=16384
                            -Wstack-usage=16384
                            -fdiagnostics-show-option
                            -Wmissing-declarations
                            -Wredundant-decls
                            -Wcast-qual
                            -Wsuggest-attribute=noreturn
                            -Wunused-but-set-variable
                            -Wunused-but-set-parameter
                            
                            -Werror=return-type
                            -Werror=pointer-arith
                            -Werror=unused-value
                            -Werror=sizeof-pointer-memaccess
                            -Werror=implicit-function-declaration
                            
#                            -Werror=missing-declarations
#                            -Werror=missing-prototypes
                            -Werror=reorder
                            -Werror=declaration-after-statement
                            -Werror=stringop-overflow
        )
        
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror=delete-non-virtual-dtor")       
        set(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -Wimplicit-int -Werror=implicit-int")
    endif(PEDANTIC_COMPILER_FLAGS)

    # if(RELEASE_DEBUG_SYMBOLS)
    #     set(DBG_FLAG -g)
    # else()
    #     set(DBG_FLAG -s)
    # endif(RELEASE_DEBUG_SYMBOLS)

    # set(CMAKE_CXX_FLAGS_RELEASE  "-O2 ${DBG_FLAG} -DNDEBUG")
    # set(CMAKE_C_FLAGS_RELEASE    ${CMAKE_CXX_FLAGS_RELEASE})
    # set(CMAKE_CXX_FLAGS_DEBUG    "-O0 -g -D_DEBUG -D__DEBUG__ -DDEBUG_LEVEL=3 -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC")
    # set(CMAKE_C_FLAGS_DEBUG      ${CMAKE_CXX_FLAGS_DEBUG})
    
    # set(CMAKE_EXE_LINKER_FLAGS_DEBUG    "${CMAKE_EXE_LINKER_FLAGS} -g")
    # set(CMAKE_SHARED_LINKER_FLAGS_DEBUG "${CMAKE_SHARED_LINKER_FLAGS} -g")
    
    # set(CMAKE_EXE_LINKER_FLAGS_VALGRIND     "${CMAKE_EXE_LINKER_FLAGS} -g")
    # set(CMAKE_SHARED_LINKER_FLAGS_VALGRIND  "${CMAKE_SHARED_LINKER_FLAGS} -g")
    
    # set(CMAKE_EXE_LINKER_FLAGS_RELEASE    "${CMAKE_EXE_LINKER_FLAGS} ${DBG_FLAG}")
    # set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS} ${DBG_FLAG}")
    
    # if(USE_32)
    #     add_compile_options (-m32)
    #     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -m32")
    #     set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -m32")
    # endif(USE_32)
    
    # if(STATIC_RUNTIME)
    #     if(MINGW)
    #         set(STATIC_LINKER_FLAGS "-static -Wl,--allow-multiple-definition")
    #     else()
    #         set(STATIC_LINKER_FLAGS "-static-libgcc -static-libstdc++")
    #     endif(MINGW)
    #     set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${STATIC_LINKER_FLAGS}")
    #     set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} ${STATIC_LINKER_FLAGS}")
    # endif(STATIC_RUNTIME)
    # set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath,'$ORIGIN'" )
endif(MSVC)


add_library(
    sqlite3 SHARED
    ${LIBRARY_SOURCES}
)

if(SQLITE_DEBUG)
    set(SQLITE_DEBUG_MACRO "-DSQLITE_ENABLE_DEBUG=1")
endif(SQLITE_DEBUG)

# 在那个vs项目里有这些定义
# _WINDOWS
# WIN32
# _CRT_SECURE_NO_WARNINGS
# _CRT_SECURE_NO_DEPRECATE
# _CRT_NONSTDC_NO_DEPRECATE
# NDEBUG
# _USRDLL 
# SQLITE_DQS=0
# SQLITE_MAX_ATTACHED=10
# SQLITE_SOUNDEX
# SQLITE_ENABLE_COLUMN_METADATA
# SQLITE_HAS_CODEC=1
# CODEC_TYPE=CODEC_TYPE_CHACHA20
# SQLITE_SECURE_DELETE
# SQLITE_ENABLE_FTS3
# SQLITE_ENABLE_FTS3_PARENTHESIS
# SQLITE_ENABLE_FTS4
# SQLITE_ENABLE_FTS5
# SQLITE_ENABLE_JSON1
# SQLITE_ENABLE_RTREE
# SQLITE_ENABLE_GEOPOLY
# SQLITE_CORE
# SQLITE_ENABLE_EXTFUNC
# SQLITE_ENABLE_CSV
# SQLITE_ENABLE_SHA3
# SQLITE_ENABLE_CARRAY
# SQLITE_ENABLE_FILEIO
# SQLITE_ENABLE_SERIES
# SQLITE_ENABLE_UUID
# SQLITE_TEMP_STORE=2
# SQLITE_USE_URI
# SQLITE_USER_AUTHENTICATION
set_target_properties(sqlite3 PROPERTIES COMPILE_FLAGS    "-D_LIB \
                                                          -D${WXSQLITE3_MAKING_DEF} \
                                                          -DwxUSE_DYNAMIC_SQLITE3_LOAD=0 \
                                                          -DWXSQLITE3_HAVE_METADATA=1 \
                                                          -DWXSQLITE3_USER_AUTHENTICATION=1 \
                                                          -DWXSQLITE3_HAVE_CODEC=1 \
                                                          -DWXSQLITE3_HAVE_LOAD_EXTENSION=0 \
                                                          -DTHREADSAFE=1 \
                                                          -DSQLITE_DQS=0 \
                                                          -DSQLITE_MAX_ATTACHED=10 \
                                                          -DSQLITE_ENABLE_EXPLAIN_COMMENTS \
                                                          -DSQLITE_SOUNDEX \
                                                          -DSQLITE_ENABLE_COLUMN_METADATA \
                                                          -DSQLITE_HAS_CODEC=1 \
                                                          -DSQLITE_SECURE_DELETE \
                                                          -DSQLITE_ENABLE_FTS3 \
                                                          -DSQLITE_ENABLE_FTS3_PARENTHESIS \
                                                          -DSQLITE_ENABLE_FTS4 \
                                                          -DSQLITE_ENABLE_FTS5 \
                                                          -DSQLITE_ENABLE_JSON1 \
                                                          -DSQLITE_ENABLE_RTREE \
                                                          -DSQLITE_ENABLE_GEOPOLY \
                                                          -DSQLITE_CORE \
                                                          -DSQLITE_ENABLE_EXTFUNC \
                                                          -DSQLITE_ENABLE_CSV \
                                                          -DSQLITE_ENABLE_SHA3 \
                                                          -DSQLITE_ENABLE_CARRAY \
                                                          -DSQLITE_ENABLE_FILEIO \
                                                          -DSQLITE_ENABLE_SERIES \
                                                          -DSQLITE_ENABLE_UUID\
                                                          -DSQLITE_TEMP_STORE=2 \
                                                          -DSQLITE_USE_URI \
                                                          -DSQLITE_USER_AUTHENTICATION \
                                                          -DCODEC_TYPE=CODEC_TYPE_CHACHA20 \
                                                          ${SQLITE_DEBUG_MACRO}")



# set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT treeview)

target_include_directories(sqlite3 PRIVATE ${CMAKE_SOURCE_DIR})
target_link_libraries(sqlite3 PRIVATE ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT})

message("//===--- current configuration ---===//")

if(MSVC)
    set(COMPILER_SPECIFIC_OPTIONS  CPP_EXCEPTIONS_ONLY
                                   THREAD_SAVE_STATIC_INIT
    )
elseif(CMAKE_COMPILER_IS_GNUCC)
    set(COMPILER_SPECIFIC_OPTIONS  CPP_EXCEPTIONS_ONLY)
endif(MSVC)

option(SQLITE_DEBUG "enable SQLite debug" "OFF")
option(PEDANTIC_COMPILER_FLAGS "Enable additional checking for ill-formed code" "ON")
option(THREAD_SAVE_STATIC_INIT "Enable thread safe initialization of static variables" "OFF")
option(RELEASE_DEBUG_SYMBOLS "Generate debugging symbols for optimized build" "OFF")
# set(SQLITE_CODEC_TYPE "DEFAULT" CACHE STRING "DB Codec(AES128, AES256, CHACHA20, DEFAULT)")


foreach(V   ${COMPILER_SPECIFIC_OPTIONS}
            STATIC_RUNTIME
            SQLITE_DEBUG
            PEDANTIC_COMPILER_FLAGS
            THREAD_SAVE_STATIC_INIT
            RELEASE_DEBUG_SYMBOLS
            SQLITE_CODEC_TYPE
            WXSQLITE3_BUILD_SHARED
       )
    message("${V}: ${${V}}")
endforeach()


