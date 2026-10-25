# Pactlane TLSNotary

A Chrome extension for testing Pactlane's payment proofs, based on [TLSNotary](https://github.com/tlsnotary/tlsn-extension).

This version gives proof setup up to 60 seconds. We made that change after the official extension's 30-second limit stopped both a transfer check and a public check. The longer limit gives setup more time; it does not make it faster.

[Download the release](https://github.com/vmichalik/pactlane-tlsnotary/releases/tag/v0.1.0.1501-pactlane.2) and follow the [install guide](pactlane/INSTALL.md). Use the public check first. A successful public proof does not verify a payment.

## What changed

The fork starts at upstream extension `0.1.0.1501`, commit `68bbd380d6e1a89d79748e5294661c752f5d1205`. The fork changes the setup deadline in `ProveManager/worker.ts` and the extension’s name, description and version label. Pactlane.2 also matches the Pactlane website’s typography, colours, icons, permission screens and disclosure overlays.

The download is a reproducible repack of the official release ZIP. The packaging script checks the upstream checksum, makes the documented worker, manifest and presentation edits, and copies all other extension files unchanged. All JavaScript bundles and WASM files are identical to Pactlane.1; the UI update changes styles, page titles, icons and font assets only. It preserves the WASM files, cryptographic checks, permissions and other deadlines. It does not rebuild WASM or include Pactlane's private application code.

The browser API version stays at `0.1.0.1501` so it works with the pinned verifier. Chrome shows the Pactlane name and version label `0.1.0.1501-pactlane.2`.

## Build the download

You need Python 3, Node.js 22 or later, Git and the [official release ZIP](https://github.com/tlsnotary/tlsn-extension/releases/download/0.1.0.1501/extension-0.1.0.1501.zip). These steps do not install dependencies or start a proof.

```sh
mkdir -p downloads
curl --fail --location \
  https://github.com/tlsnotary/tlsn-extension/releases/download/0.1.0.1501/extension-0.1.0.1501.zip \
  --output downloads/extension-0.1.0.1501.zip
python3 pactlane/package.py
node --test pactlane/watchdog.test.mjs
```

The files appear in `dist/0.1.0.1501-pactlane.2/`. The script stops if that directory already exists. For another build, give it a new directory with `--output`.

Each release includes the ZIP, `SHA256SUMS` and `audit.json`. The audit lists the upstream checksum, source commit and hashes of every extension file. To compare builds, use the same clean source commit, upstream ZIP and Python/zlib versions.

## What has been checked

The tests execute the released worker code with a controlled clock and a simulated prover. They check that the official build stops setup at 30 seconds, this build allows 36.2- and 45-second setups, and a stalled setup stops at 60 seconds. The HTTP request deadline remains 60 seconds.

These tests check the timeout change and package contents. Pactlane.1 completed an owner-run public proof and an authenticated seven-field transfer proof on 25 October 2026; those results do not establish order payment or authorize release. Pactlane.2 changes presentation only. Its browser checks use synthetic UI data, without a bank request.

## Known limits

The longer deadline may still be too short. The current test verifier also has a separate 120-second overall limit, which includes later proof work.

Upstream cleanup can fail when a timed-out setup still holds the prover. If a test fails or the extension gets stuck, stop and fully quit Chrome before opening it again. This release also retains upstream's finite QuickJS callback-ID limit. Neither issue is fixed by the deadline or presentation changes.

Start with the public check in the install guide. Review the request and disclosure before approving. Use authenticated account data only with the account owner's approval. Payment verification and release remain unproven.

## Upstream and licence

TLSNotary provides the protocol, extension and runtime. Pactlane maintains this fork; it is not an official TLSNotary release. The upstream package declares the MIT licence. Manrope is bundled under the SIL Open Font License in `pactlane/branding/OFL.pactlane.txt`. Original source headers and dependency notices are retained, and Pactlane's additions are covered by [LICENSE.pactlane](LICENSE.pactlane).

The original project README is preserved in [README.upstream.md](README.upstream.md).
