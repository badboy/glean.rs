# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# We use this specific version because our decision task also runs on this one.
# We also use that same version in decisionlib.py
FROM ubuntu:bionic-20180821

MAINTAINER Jan-Erik Rediger "janerik@mozilla.com"

RUN echo "trigger rebuild"

# Add worker user

RUN mkdir /builds && \
    useradd -d /builds/worker -s /bin/bash -m worker && \
    chown worker:worker /builds/worker && \
    mkdir /builds/worker/artifacts && \
    chown worker:worker /builds/worker/artifacts

WORKDIR /builds/worker/

# Configuration

ENV ANDROID_BUILD_TOOLS "28.0.3"
ENV ANDROID_SDK_VERSION "3859397"
ENV ANDROID_PLATFORM_VERSION "28"

# Set up the language variables to avoid problems (we run locale-gen later).
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Do not use fancy output on taskcluster
ENV TERM dumb

ENV GRADLE_OPTS -Xmx4096m -Dorg.gradle.daemon=false

# Used to detect in scripts whether we are running on taskcluster
ENV CI_TASKCLUSTER true

ENV \
    # Some APT packages like 'tzdata' wait for user input on install by default.
    # https://stackoverflow.com/questions/44331836/apt-get-install-tzdata-noninteractive
    DEBIAN_FRONTEND=noninteractive

# System.

RUN apt-get update -qq \
    && apt-get install -qy --no-install-recommends \
        # To compile Android stuff.
        openjdk-8-jdk \
        git \
        curl \
        # Required by symbolstore.py.
        file \
        # Will set up the timezone to UTC (?).
        tzdata \
        # To install UTF-8 locales.
        locales \
        # For `cc` crates; see https://github.com/jwilm/alacritty/issues/1440.
        # <TODO: Is this still true?>.
        g++ \
        # <TODO: Explain why we have this dependency>.
        clang \
        python3 \
        python3-pip \
        # taskcluster > mohawk > setuptools.
        python3-setuptools \
        # Required to extract the Android SDK/NDK.
        unzip \
        # Required by tooltool to extract tar.xz archives.
        xz-utils \
        # Required to unpack compiler
        zstd \
        # Required to build libs/.
        make \
        # Required to build sqlcipher.
        tclsh \
        # Required in libs/ by some scripts patching the source they download.
        patch \
        # For windows cross-compilation.
        mingw-w64 \
        ## NSS build dependencies
        gyp \
        ninja-build \
        zlib1g-dev \
        # <TODO: Delete p7zip once NSS windows is actually compiled instead of downloaded>.
        p7zip-full \
        ## End of NSS build dependencies
        rsync \
    && apt-get clean

RUN pip3 install --upgrade pip
RUN pip3 install \
    'taskcluster>=4,<5' \
    pyyaml

# Compile the UTF-8 english locale files (required by Python).
RUN locale-gen en_US.UTF-8

# Android SDK

RUN mkdir -p /builds/worker/android-sdk
WORKDIR /builds/worker

ENV ANDROID_HOME /builds/worker/android-sdk
ENV ANDROID_SDK_HOME /builds/worker/android-sdk
ENV PATH ${PATH}:${ANDROID_SDK_HOME}/tools:${ANDROID_SDK_HOME}/tools/bin:${ANDROID_SDK_HOME}/platform-tools:/opt/tools:${ANDROID_SDK_HOME}/build-tools/${ANDROID_BUILD_TOOLS}

RUN curl -sfSL --retry 5 --retry-delay 10 https://dl.google.com/android/repository/sdk-tools-linux-${ANDROID_SDK_VERSION}.zip > sdk.zip \
    && unzip -q sdk.zip -d ${ANDROID_SDK_HOME} \
    && rm sdk.zip \
    && mkdir -p /builds/worker/android-sdk/.android/ \
    && touch /builds/worker/android-sdk/.android/repositories.cfg \
    && yes | sdkmanager --licenses \
    && sdkmanager --verbose "platform-tools" \
        "platforms;android-${ANDROID_PLATFORM_VERSION}" \
        "build-tools;${ANDROID_BUILD_TOOLS}" \
        "extras;android;m2repository" \
        "extras;google;m2repository"

RUN chown -R worker:worker /builds/worker/android-sdk

# Android NDK

ENV ANDROID_NDK_VERSION "r21"

# $ANDROID_NDK_ROOT is the preferred name, but the android gradle plugin uses $ANDROID_NDK_HOME.
ENV ANDROID_NDK_ROOT /builds/worker/android-ndk
ENV ANDROID_NDK_HOME /builds/worker/android-ndk

RUN curl -sfSL --retry 5 --retry-delay 10 https://dl.google.com/android/repository/android-ndk-${ANDROID_NDK_VERSION}-linux-x86_64.zip > ndk.zip \
    && unzip -q ndk.zip -d /builds/worker \
    && rm ndk.zip \
    && mv /builds/worker/android-ndk-${ANDROID_NDK_VERSION} ${ANDROID_NDK_ROOT}

ENV ANDROID_NDK_TOOLCHAIN_DIR /builds/worker/.android-ndk-r21-toolchain
ENV ANDROID_NDK_API_VERSION 21

# sccache
RUN \
    curl -sfSL --retry 5 --retry-delay 10 \
        https://github.com/mozilla/sccache/releases/download/0.2.13/sccache-0.2.13-x86_64-unknown-linux-musl.tar.gz \
        | tar -xz --strip-components=1 -C /usr/local/bin/ \
            sccache-0.2.13-x86_64-unknown-linux-musl/sccache

# tooltool
RUN \
    curl -sfSL --retry 10 --retry-delay 10 \
         -o /usr/local/bin/tooltool.py \
         https://raw.githubusercontent.com/mozilla/build-tooltool/36511dae0ead6848017e2d569b1f6f1b36984d40/tooltool.py && \
         chmod +x /usr/local/bin/tooltool.py


# %include-run-task

ENV SHELL=/bin/bash \
    HOME=/builds/worker \
    PATH=/builds/worker/.local/bin:$PATH


VOLUME /builds/worker/checkouts
VOLUME /builds/worker/.cache


# run-task expects to run as root
USER root
