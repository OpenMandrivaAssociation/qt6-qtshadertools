%define beta beta5
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtshadertools
Version:	6.0.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtshadertools-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtshadertools-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Shader Tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Qml-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}QmlModels-devel
BuildRequires:	%{_lib}Qt%{major}QmlQuick-devel
BuildRequires:	%{_lib}Qt%{major}QmlQuickWidgets-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} shader tools

%prep
%autosetup -p1 -n qtshadertools%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DFEATURE_cxx2a:BOOL=ON \
	-DFEATURE_dynamicgl:BOOL=ON \
	-DFEATURE_ftp:BOOL=ON \
	-DFEATURE_opengl_dynamic:BOOL=ON \
	-DFEATURE_use_lld_linker:BOOL=ON \
	-DFEATURE_xcb_native_painting:BOOL=ON \
	-DFEATURE_openssl:BOOL=ON \
	-DFEATURE_openssl_linked:BOOL=ON \
	-DFEATURE_system_sqlite:BOOL=ON \
	-DINPUT_sqlite=system \
	-DQT_WILL_INSTALL:BOOL=ON \
	-D_OPENGL_LIB_PATH=%{_libdir} \
	-DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
	-DOPENGL_glu_LIBRARY=%{_libdir}/libGLU.so \
	-DOPENGL_glx_LIBRARY=%{_libdir}/libGLX.so \
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Static helper lib without headers -- useless
rm -f %{buildroot}%{_libdir}/qt6/%{_lib}/libpnp_basictools.a
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/cmake
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
for i in %{buildroot}%{_qtdir}/lib/cmake/*; do
	[ "$(basename ${i})" = "Qt6BuildInternals" ] && continue
	ln -s ../qt%{major}/lib/cmake/$(basename ${i}) %{buildroot}%{_libdir}/cmake/
done

%files
%{_libdir}/cmake/Qt6ShaderTools
%{_libdir}/cmake/Qt6ShaderToolsTools
%{_libdir}/libQt6ShaderTools.so
%{_libdir}/libQt6ShaderTools.so.*
%{_qtdir}/bin/qsb
%{_qtdir}/include/QtShaderTools
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtShaderToolsTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt6ShaderTools
%{_qtdir}/lib/cmake/Qt6ShaderToolsTools
%{_qtdir}/lib/libQt6ShaderTools.prl
%{_qtdir}/lib/libQt6ShaderTools.so
%{_qtdir}/lib/libQt6ShaderTools.so.*
%{_qtdir}/mkspecs/modules/qt_ext_glslang_glslang.pri
%{_qtdir}/mkspecs/modules/qt_ext_glslang_oglcompiler.pri
%{_qtdir}/mkspecs/modules/qt_ext_glslang_osdependent.pri
%{_qtdir}/mkspecs/modules/qt_ext_glslang_spirv.pri
%{_qtdir}/mkspecs/modules/qt_ext_spirv_cross.pri
%{_qtdir}/mkspecs/modules/qt_lib_shadertools.pri
%{_qtdir}/mkspecs/modules/qt_lib_shadertools_private.pri
%{_qtdir}/modules/ShaderTools.json
