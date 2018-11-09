Note that all this is rather experimental.

Please do not compile Pango in a path with spaces to avoid potential
problems during the build and/or during the usage of the Pango
library.

Please refer to the following GNOME Live! page for more detailed
instructions on building Pango and its dependencies with Visual C++:

https://live.gnome.org/GTK%2B/Win32/MSVCCompilationOfGTKStack

This VS15 solution and the projects it includes are intented to be used
in a Pango source tree unpacked from a tarball. In a git checkout you
first need to use some Unix-like environment or manual work to expand
files as needed, for instance the .vcxprojin/vcxproj.filtersin files
here into .vcxproj/.vcxproj.filters files.

It is recommended that GLib is compiled with VS15 to compile Pango.
External dependencies are at least Cairo,  zlib, libpng,
gettext-runtime; optional dependencies include fontconfig, freetype,
and expat.  Please see the build\win32\vs15\README.txt file in glib
for details where to unpack them.

Decide first whether you would want to use fontconfig (which also includes
freetype) prior to starting this build-Cairo needs to be built with freetype
*and* fontconfig support before building Pango.  You will need fontconfig
support if you plan on building GIMP, or if you need support for complex
language scripts via fontconfig.

It is recommended that one builds the dependencies with VS15 as far as
possible, especially those from and using the GTK+ stack (i.e. GLib and
Cairo, [Cairo if one is planning to use GTK+ 3.x]), so that crashes
caused by mixing calls to different CRTs can be kept at a minimum.
zlib, libpng, and Cairo do contain support for compiling under VS15
using VS project files and/or makefiles at this time of writing.
For GLib, VS15 project files are available under
$(srcroot)\vs15 in the case of GLib (stable/unstable).

There is no known official VS15 build support for fontconfig
(along with freetype and expat which will work with the pre-compiled
fontconfig binary on ftp.gnome.org) and gettext-runtime, so please use
the binaries from:

ftp://ftp.gnome.org/pub/GNOME/binaries/win32/dependencies/ (32 bit)
ftp://ftp.gnome.org/pub/GNOME/binaries/win64/dependencies/ (64 bit)

Set up the source tree as follows under some arbitrary top folder
<root>:

<root>\<this-pango-source-tree>
<root>\vs15\<PlatformName>

Unzip the binaries obtained from ftp.gnome.org in <root>\vs15\<PlatformName>,
and build the following, if not already done so: 

Note: put the resulting zlib, libpng, pcre and Cairo files as follows:
 .dll files: <root>\vs15\<PlatformName>\bin
 .lib files: <root>\vs15\<PlatformName>\lib
 .h files: <root>\vs15\<PlatformName>\include

The recommended build order for these dependencies:
(first unzip any dependent binaries downloaded from the ftp.gnome.org
 as described in the README.txt file in the build\win32\vs15 folder)
-zlib
-libpng
-(optional for GLib) PCRE (version 8.12 or later, use of CMake to
  build PCRE is recommended-see build\win32\vs15\README.txt of GLib)
-GLib (put the sources in <root>\<GLib-Source-Tree>, and build it from
       there with VS15)
-Cairo (inclusive of Cairo-GObject-if using GTK+-3.x)

Use the *_fc configs if the usage of fontconfig is desired; otherwise
use the configs that do not end with _fc.

*this* file you are now reading is thus located at
<root>\<this-pango-source-tree>\win32\vs15\README.txt.

<PlatformName> is either Win32 or x64, as in VS15 project files.

You should unpack the glib-dev zip file into
<root>\vs15\<PlatformName>, so that for instance glib.h ends up at
<root>\vs15\<PlatformName>\include\glib-2.0\glib.h.

The "install" project will copy build results and headers into their
appropriate location under <root>\vs15\<PlatformName>. For instance,
built DLLs go into <root>\vs15\<PlatformName>\bin, built LIBs into
<root>\vs15\<PlatformName>\lib and headers into
<root>\vs15\<PlatformName>\include\pangpo-1.0. This is then from where
project files higher in the stack are supposed to look for them, not
from a specific Pango source tree like this one. It is important to
keep separate the concept of a "source tree", where also non-public
headers are present, and an "install tree" where only public headers
are present.

There is now a "pango-introspect" project that is used to build the
introspection files.  In order for this to work, check that the paths for
PythonDir (32-bit builds) and PythonDirX64 (x64 builds) are correct for your
system.  Note that it must be the same Python installation that was used to
build GObject-Introspection (G-I), and a complete G-I build/installation
needs to be found in <root>\vs15\<PlatformName>\.  Note also that this is not
built by default, so you will need to right-click on the project to build it,
which will build and "install" the other projects that are normally built, if
those were not yet built.  The introspection files that are built will be
"installed" to <root>\vs15\<PlatformName>\share\gir-1.0 (the .gir file(s)) and
<root>\vs15\<PlatformName>\lib\girepository-1.0 (the .typelib files(s)) upon
successful build.  for building this in a different configuration, therefore,
you will need to clean this project specifically and then rebuild.  Note that
this is currently supported only for the non _FC (i.e. where PangoFT2 is not
built) configurations

--Tor Lillqvist <tml@iki.fi>
--Updated by Fan, Chun-wei <fanc999@yahoo.com.tw>
