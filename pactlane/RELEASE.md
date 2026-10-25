Pactlane TLSNotary gives proof setup up to 60 seconds instead of 30. It is based on TLSNotary 0.1.0.1501 and uses the same cryptographic runtime and permissions.

Download the ZIP, unzip it, and load its `extension` folder through Chrome's **Load unpacked** button. Turn off the official TLSNotary extension while using this one. The ZIP includes the install guide and provenance; `SHA256SUMS` and `audit.json` are also attached to this release.

Start with the [public connection check](https://stellar-p2p-proof-vijay.fly.dev/extension-check/). It uses no bank login or payment data. Stop after the first result and share only the `Extension check:` line.

The package passes 11 offline watchdog tests. Those tests use the released worker code with a simulated prover. A real MacBook proof with this package is still pending.

The existing timeout-cleanup issue and QuickJS callback limit remain. If the extension gets stuck, fully quit Chrome before reopening it. Payment verification and release remain unproven.
