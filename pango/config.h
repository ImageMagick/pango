/*
 * Autogenerated by the Meson build system.
 * Do not edit, your changes will be lost.
 */

#pragma once

#define DLL_EXPORT

#define HAVE_CAIRO 1

#define HAVE_CAIRO_PDF 1

#define HAVE_CAIRO_PS 1

#define HAVE_CAIRO_WIN32 1

#define PANGO_BINARY_AGE 4502

#define PANGO_INTERFACE_AGE 0

#define PANGO_VERSION_MAJOR 1

#define PANGO_VERSION_MICRO 2

#define PANGO_VERSION_MINOR 45

#if defined(_DLL)
#  if defined(PANGO_COMPILATION)
#    define _PANGO_EXTERN __declspec(dllexport)
#  else
#    define _PANGO_EXTERN __declspec(dllimport)
#  endif
#endif

