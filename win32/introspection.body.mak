Pango-1.0.gir: Pango_1_0_gir_list 
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=Pango	\
	--nsversion=1.0	\
	--pkg=gobject-2.0 --pkg=cairo --pkg=glib-2.0	\
	--library=pango-1.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=GObject-2.0 --include=cairo-1.0	\
	--pkg-export=pango	\
  	\
	--cflags-begin	\
	-I.. -DG_LOG_DOMAIN="Pango" -DPANGO_ENABLE_BACKEND -DPANGO_ENABLE_ENGINE	\
	--cflags-end	\
	--c-include pango/pango.h	\
	--filelist=Pango_1_0_gir_list	\
	-o $@

Pango-1.0.typelib: Pango-1.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	Pango-1.0.gir	\
	-o $@

PangoCairo-1.0.gir: PangoCairo_1_0_gir_list Pango-1.0.gir
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=PangoCairo	\
	--nsversion=1.0	\
	--pkg=gobject-2.0 --pkg=cairo	\
	--library=pango-1.0 --library=pangocairo-1.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=GObject-2.0 --include=cairo-1.0 --include=win32-1.0	\
	--pkg-export=pangocairo	\
  	\
	--cflags-begin	\
	-I.. -DG_LOG_DOMAIN="Pango" -DPANGO_ENABLE_BACKEND -DPANGO_ENABLE_ENGINE	\
	--cflags-end	\
	--include-uninstalled=./Pango-1.0.gir --c-include pango/pangocairo.h	\
	--filelist=PangoCairo_1_0_gir_list	\
	-o $@

PangoCairo-1.0.typelib: PangoCairo-1.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	PangoCairo-1.0.gir	\
	-o $@

