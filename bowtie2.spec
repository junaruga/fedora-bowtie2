Name: bowtie2
Version: 2.4.1
Release: 1%{?dist}
Summary: An ultrafast and memory-efficient read aligner
# bowtie2: GPLv3+
# tinythread.{h,cpp}: zlib
# fast_mutex.h: zlib
License: GPLv3+ and zlib
URL: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml
Source0: https://downloads.sourceforge.net/project/bowtie-bio/%{name}/%{version}/%{name}-%{version}-source.zip
# git clone https://github.com/BenLangmead/bowtie2.git
# cd bowtie2 && git checkout v2.4.1
# tar czvf bowtie2-2.4.1-tests.tgz scripts/test/
Source1: bowtie2-2.4.1-tests.tgz
Requires: perl
Requires: python3
BuildRequires: gcc-c++
BuildRequires: perl
BuildRequires: python3
BuildRequires: tbb-devel
BuildRequires: zlib-devel
# 32-bit CPU architectures are not supported. See Makefile.
ExcludeArch: i686 armv7hl

# TinyThread++
# https://tinythreadpp.bitsnbites.eu/
# https://gitorious.org/tinythread/tinythreadpp
Provides: bundled(tiny-thread) = 1.1
# TODO: fast_mutex
Provides: bundled(fast-mutex)


%description

Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing
reads to long reference sequences. It is particularly good at aligning reads
of about 50 up to 100s or 1,000s of characters, and particularly good at
aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the
genome with an FM Index to keep its memory footprint small: for the human
genome, its memory footprint is typically around 3.2 GB. Bowtie 2 supports
gapped, local, and paired-end alignment modes.

%prep
%setup -q

# Remove the directory to avoid building bowtie with bundled libraries.
rm -rf third_party


%build
# Set flags considering the upstream testing cases for each architecture.
# https://github.com/BenLangmead/bowtie2/blob/master/.travis.yml
%ifnarch x86_64
export POPCNT_CAPABILITY=0
export NO_TBB=1
%endif

%make_build allall


%install
%make_install prefix="%{_usr}" DESTDIR="%{buildroot}"

# Install bowtie-*-debug commands used by `bowtie --debug`.
# Install bowtie-*-sanitized commands used by `bowtie --sanitized`.
for cmd in bowtie-*-{debug,sanitized}; do
  cp -p "${cmd}" %{buildroot}/%{_bindir}/
done


%check
ASAN_OPTIONS="halt_on_error=1" \
UBSAN_OPTIONS="halt_on_error=1" \
scripts/test/simple_tests.pl \
  --bowtie2=./bowtie2 \
  --bowtie2-build=./bowtie2-build \
  --compressed


%files
%license LICENSE
%{_bindir}/bowtie2
%{_bindir}/bowtie2-align-l
%{_bindir}/bowtie2-align-l-debug
%{_bindir}/bowtie2-align-l-sanitized
%{_bindir}/bowtie2-align-s
%{_bindir}/bowtie2-align-s-debug
%{_bindir}/bowtie2-align-s-sanitized
%{_bindir}/bowtie2-build
%{_bindir}/bowtie2-build-l
%{_bindir}/bowtie2-build-l-debug
%{_bindir}/bowtie2-build-l-sanitized
%{_bindir}/bowtie2-build-s
%{_bindir}/bowtie2-build-s-debug
%{_bindir}/bowtie2-build-s-sanitized
%{_bindir}/bowtie2-inspect
%{_bindir}/bowtie2-inspect-l
%{_bindir}/bowtie2-inspect-l-debug
%{_bindir}/bowtie2-inspect-l-sanitized
%{_bindir}/bowtie2-inspect-s
%{_bindir}/bowtie2-inspect-s-debug
%{_bindir}/bowtie2-inspect-s-sanitized


%changelog
