# Unreleased changes

[Full changelog](https://github.com/mozilla/glean/compare/v22.0.0...master)

# v22.0.0 (2019-12-05)

[Full changelog](https://github.com/mozilla/glean/compare/v21.3.0...22.0.0)

* Add option to defer ping lifetime metric persistence ([#530](https://github.com/mozilla/glean/pull/530))
* Add a crate for the nice control API ([#542](https://github.com/mozilla/glean/pull/542))
* Pending `deletion_request` pings are resent on start ([#545](https://github.com/mozilla/glean/pull/545))

# v21.3.0 (2019-12-03)

[Full changelog](https://github.com/mozilla/glean/compare/v21.2.0...21.3.0)

* Timers are reset when disabled. That avoids recording timespans across disabled/enabled toggling ([#495](https://github.com/mozilla/glean/pull/495)).
* Add a new flag to pings: `send_if_empty` ([#528](https://github.com/mozilla/glean/pull/528))
* Upgrade `glean_parser` to v1.12.0
* Implement the deletion request ping in Glean ([#526](https://github.com/mozilla/glean/pull/526))

# v21.2.0 (2019-11-21)

[Full changelog](https://github.com/mozilla/glean/compare/v21.1.1...21.2.0)

* All platforms

  * The experiments API is no longer ignored before the Glean SDK initialized. Calls are
    recorded and played back once the Glean SDK is initialized.

  * String list items were being truncated to 20, rather than 50, bytes when using
    `.set()` (rather than `.add()`). This has been corrected, but it may result
    in changes in the sent data if using string list items longer than 20 bytes.

# v21.1.1 (2019-11-20)

[Full changelog](https://github.com/mozilla/glean/compare/v21.1.0...v21.1.1)

* Android:

  * Use the `LifecycleEventObserver` interface, rather than the `DefaultLifecycleObserver`
    interface, since the latter isn't compatible with old SDK targets.

# v21.1.0 (2019-11-20)

[Full changelog](https://github.com/mozilla/glean/compare/v21.0.0...v21.1.0)

* Android:

  * Two new metrics were added to investigate sending of metrics and baseline pings.
    See [bug 1597980](https://bugzilla.mozilla.org/show_bug.cgi?id=1597980) for more information.

  * Glean's two lifecycle observers were refactored to avoid the use of reflection.

* All platforms:

  * Timespans will now not record an error if stopping after setting upload enabled to false.

# v21.0.0 (2019-11-18)

[Full changelog](https://github.com/mozilla/glean/compare/v20.2.0...v21.0.0)

* Android:

  * The `GleanTimerId` can now be accessed in Java and is no longer a `typealias`.

  * Fixed a bug where the metrics ping was getting scheduled twice on startup.
* All platforms

  * Bumped `glean_parser` to version 1.11.0.

# v20.2.0 (2019-11-11)

[Full changelog](https://github.com/mozilla/glean/compare/v20.1.0...v20.2.0)

* In earlier 20.x.x releases, the version of glean-ffi was incorrectly built
  against the wrong version of glean-core.

# v20.1.0 (2019-11-11)

[Full changelog](https://github.com/mozilla/glean/compare/v20.0.0...v20.1.0)

* The version of Glean is included in the Glean Gradle plugin.

* When constructing a ping, events are now sorted by their timestamp. In practice,
  it rarely happens that event timestamps are unsorted to begin with, but this
  guards against a potential race condition and incorrect usage of the lower-level
  API.

# v20.0.0 (2019-11-11)

[Full changelog](https://github.com/mozilla/glean/compare/v19.1.0...v20.0.0)

* Glean users should now use a Gradle plugin rather than a Gradle script. (#421)
  See [integrating with the build system docs](https://mozilla.github.io/glean/book/user/adding-glean-to-your-project.html#integrating-with-the-build-system) for more information.

* In Kotlin, metrics that can record errors now have a new testing method,
  `testGetNumRecordedErrors`. (#401)

# v19.1.0 (2019-10-29)

[Full changelog](https://github.com/mozilla/glean/compare/v19.0.0...v19.1.0)

* Fixed a crash calling `start` on a timing distribution metric before Glean is initialized.
  Timings are always measured, but only recorded when upload is enabled ([#400](https://github.com/mozilla/glean/pull/400))
* BUGFIX: When the Debug Activity is used to log pings, each ping is now logged only once ([#407](https://github.com/mozilla/glean/pull/407))
* New `invalid state` error, used in timespan recording ([#230](https://github.com/mozilla/glean/pull/230))
* Add an Android crash instrumentation walkthrough ([#399](https://github.com/mozilla/glean/pull/399))
* Fix crashing bug by avoiding assert-printing in lmdb ([#422](https://github.com/mozilla/glean/pull/422))
* Upgrade dependencies, including rkv ([#416](https://github.com/mozilla/glean/pull/416))

# v19.0.0 (2019-10-22)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING6...v19.0.0)

First stable release of Glean in Rust (aka glean-core).
This is a major milestone in using a cross-platform implementation of Glean on the Android platform.

* Fix roundtripping of timezone offsets in dates ([#392](https://github.com/mozilla/glean/pull/392))
* Handle dynamic labels in coroutine tasks ([#394](https://github.com/mozilla/glean/pull/384))

# v0.0.1-TESTING6 (2019-10-18)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING5...v0.0.1-TESTING6)

* Ignore dynamically stored labels if Glean is not initialized ([#374](https://github.com/mozilla/glean/pull/374))
* Make sure ProGuard doesn't remove Glean classes from the app ([#380](https://github.com/mozilla/glean/pull/380))
* Keep track of pings in all modes ([#378](https://github.com/mozilla/glean/pull/378))
* Add 'jnaTest' dependencies to the 'forUnitTest' JAR ([#382](https://github.com/mozilla/glean/pull/382))

# v0.0.1-TESTING5 (2019-10-10)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING4...v0.0.1-TESTING5)

* Upgrade to NDK r20 ([#365](https://github.com/mozilla/glean/pull/365))

# v0.0.1-TESTING4 (2019-10-09)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING3...v0.0.1-TESTING4)

* Take DST into account when converting a calendar into its items ([#359](https://github.com/mozilla/glean/pull/359))
* Include a macOS library in the `forUnitTests` builds ([#358](https://github.com/mozilla/glean/pull/358))
* Keep track of all registered pings in test mode ([#363](https://github.com/mozilla/glean/pull/363))

# v0.0.1-TESTING3 (2019-10-08)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING2...v0.0.1-TESTING3)

* Allow configuration of Glean through the GleanTestRule
* Bump `glean_parser` version to 1.9.2

# v0.0.1-TESTING2 (2019-10-07)

[Full changelog](https://github.com/mozilla/glean/compare/v0.0.1-TESTING1...v0.0.1-TESTING2)

* Include a Windows library in the `forUnitTests` builds

# v0.0.1-TESTING1 (2019-10-02)

[Full changelog](https://github.com/mozilla/glean/compare/95b6bcc03616c8d7c3e3e64e99ee9953aa06a474...v0.0.1-TESTING1)

### General

First testing release.