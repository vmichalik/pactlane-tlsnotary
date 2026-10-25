# Pactlane TLSNotary

Prove a bank payment from your browser. Pactlane TLSNotary connects the payment you see in your bank app to the verifier that checks an exchange order.

[Download Pactlane TLSNotary](https://github.com/vmichalik/pactlane-tlsnotary/releases/tag/v0.1.0.1501-pactlane.2) · [Install in Chrome](pactlane/INSTALL.md) · [Pactlane](https://pactlane.io/)

## How it works

1. Open a proof request from Pactlane.
2. Choose the transfer in your bank window.
3. Review exactly what the extension will disclose and approve it.
4. The verifier authenticates the record; the order policy checks the recipient, amount, timing and reuse before settlement.

The disclosure preview is the source of truth for what you share. The current complete-record check includes the full transfer response, so review it before approving.

## What's in this release

Pactlane.2 matches the website's typography, colours, icons and disclosure screens. Proof setup has up to 60 seconds, compared with 30 seconds in the upstream release. This gives slower setups more time without changing the cryptographic checks or permissions.

The package is based on TLSNotary 0.1.0.1501, commit `68bbd380d6e1a89d79748e5294661c752f5d1205`. Its browser API remains `0.1.0.1501`; Chrome shows the Pactlane version label `0.1.0.1501-pactlane.2`.

The packaging script verifies the official ZIP, applies the documented deadline and presentation edits, and copies the remaining files unchanged. Pactlane.2 preserves every JavaScript bundle and WASM file from Pactlane.1. Each release includes `SHA256SUMS` and an `audit.json` listing source and file hashes.

## Reproduce the package

Use Python 3, Node.js 22 or later, Git and the official release ZIP:

```sh
mkdir -p downloads
curl --fail --location \
  https://github.com/tlsnotary/tlsn-extension/releases/download/0.1.0.1501/extension-0.1.0.1501.zip \
  --output downloads/extension-0.1.0.1501.zip
python3 pactlane/package.py
node --test pactlane/watchdog.test.mjs
```

Output goes to `dist/0.1.0.1501-pactlane.2/`. For another build, select a fresh directory with `--output`. To compare byte-for-byte, use the release's clean source commit, upstream ZIP and recorded Python/zlib versions.

The 11 watchdog tests exercise the released worker with a controlled clock: upstream setup stops at 30 seconds, Pactlane permits a 36-second setup and stops a stalled setup at 60 seconds. The HTTP-request deadline remains 60 seconds. Owner-run checks also completed a public proof and an authenticated transfer proof using Pactlane.1; Pactlane.2 changes presentation only.

## Troubleshooting

If the verifier rejects the connection, check that it allows the installed extension ID. Keep the same installation folder when updating an unpacked extension.

If a proof becomes stuck after a timeout, fully quit Chrome before reopening it. The upstream cleanup behavior and finite QuickJS callback-ID limit still apply. The verifier also has its own overall deadline. A public connection check can isolate setup without a bank login; follow the [install guide](pactlane/INSTALL.md).

## Credits and licence

[TLSNotary](https://github.com/tlsnotary/tlsn-extension) provides the protocol, extension and runtime. Pactlane maintains this independently branded distribution; it is not an official TLSNotary release.

The upstream package declares the MIT licence. Original source headers and dependency notices are retained. Pactlane additions use [LICENSE.pactlane](LICENSE.pactlane); Manrope uses the [SIL Open Font License](pactlane/branding/OFL.pactlane.txt). The [upstream README](README.upstream.md) is preserved.
