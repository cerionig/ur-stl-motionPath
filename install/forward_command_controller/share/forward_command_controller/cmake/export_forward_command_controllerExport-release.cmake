#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "forward_command_controller::forward_command_controller" for configuration "Release"
set_property(TARGET forward_command_controller::forward_command_controller APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(forward_command_controller::forward_command_controller PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libforward_command_controller.so"
  IMPORTED_SONAME_RELEASE "libforward_command_controller.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS forward_command_controller::forward_command_controller )
list(APPEND _IMPORT_CHECK_FILES_FOR_forward_command_controller::forward_command_controller "${_IMPORT_PREFIX}/lib/libforward_command_controller.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
