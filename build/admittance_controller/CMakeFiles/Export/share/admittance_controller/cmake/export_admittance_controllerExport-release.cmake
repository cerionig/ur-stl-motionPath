#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "admittance_controller::admittance_controller" for configuration "Release"
set_property(TARGET admittance_controller::admittance_controller APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(admittance_controller::admittance_controller PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libadmittance_controller.so"
  IMPORTED_SONAME_RELEASE "libadmittance_controller.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS admittance_controller::admittance_controller )
list(APPEND _IMPORT_CHECK_FILES_FOR_admittance_controller::admittance_controller "${_IMPORT_PREFIX}/lib/libadmittance_controller.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
