# Pactlane TLSNotary 2

Pactlane TLSNotary now matches the Pactlane website, including its typography, colours, icons and disclosure screens. Setup keeps the 60-second deadline introduced in Pactlane.1. The proof runtime, JavaScript bundles and permissions are unchanged from that release.

[Download Pactlane.2](https://github.com/vmichalik/pactlane-tlsnotary/releases/tag/v0.1.0.1501-pactlane.2) and follow the [Chrome installation guide](INSTALL.md). Existing users should replace files in the same installed folder, then click Reload in `chrome://extensions` to preserve their extension ID.

The release includes the ZIP, `SHA256SUMS` and `audit.json`. Its source commit is `4fbdb5809d6377af7e6d7c50c5cb1a2cb9896780`. ZIP SHA-256:

```text
9a27e54c24a2a80a64661f47bac6eeb2d7876c08ea89126f33f5e67da3d80be2
```

Pactlane.1 completed owner-run public and authenticated transfer checks. This release changes presentation only. Its UI review used synthetic data; the 11 watchdog checks cover the underlying setup deadline.

Review each disclosure before approving. If timeout cleanup leaves a proof stuck, fully quit Chrome before opening it again. See [troubleshooting](../README.md#troubleshooting) for connection and runtime details.
