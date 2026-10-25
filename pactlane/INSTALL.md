# Install Pactlane TLSNotary

Use Pactlane TLSNotary to review and prove a transfer from Chrome. [Download the current release](https://github.com/vmichalik/pactlane-tlsnotary/releases/tag/v0.1.0.1501-pactlane.2).

## Update an existing Pactlane installation

This update matches Pactlane’s website: typography, colours, icons, permission screens and disclosure overlays. It changes no proof code or permissions from Pactlane.1.

1. Open `chrome://extensions` and find Pactlane TLSNotary. Note its existing extension-folder location.
2. Close any active proof window. Unzip the new download.
3. Copy the files **inside** the new `extension` folder into the existing installed extension folder, replacing the old files. Keep the existing folder path.
4. Click **Reload** on Pactlane TLSNotary in `chrome://extensions`. Check the version label below and refresh any proof page already open.

Keeping the folder path preserves the unpacked extension ID that the verifier allows. Do not use Load unpacked on a second folder for this update.

## First installation in Chrome

1. Quit Chrome with Cmd+Q, then open it again.
2. Unzip the download. Keep the `Pactlane TLSNotary` folder somewhere permanent, such as Documents. Chrome needs those files while the extension is installed.
3. Open `chrome://extensions` and turn off the existing TLSNotary extension. You can leave it installed.
4. Turn on **Developer mode** at the top right.
5. Click **Load unpacked**. Inside the `Pactlane TLSNotary` folder, choose the `extension` folder. It contains `manifest.json`.
6. Check that **Pactlane TLSNotary** is enabled. Leave the original TLSNotary extension turned off while using Pactlane.

The version label is `0.1.0.1501-pactlane.2`. The underlying API version remains `0.1.0.1501`.

## Run the public check

Open https://stellar-p2p-proof-vijay.fly.dev/extension-check/ and click **Check extension only**.

In the window that opens, click **Run public connection check** once. Keep the window visible. When the disclosure preview appears, approve only the public `GET /robots.txt` request line and HTTP status.

This check uses the same 4 KiB sent / 16 KiB received limits as the transfer check. It uses no bank login, cookies or payment data.

Copy the final `Extension check:` line from the original tab. If it fails, stop rather than running another attempt. If it is still stuck after two minutes, keep only the displayed status message and quit Chrome. The timeout cleanup issue in the upstream runtime is still present.

A public pass confirms the proof connection. For a trade, Pactlane then checks the authenticated transfer against the locked order.

## Return to the official extension

Open `chrome://extensions`, remove or turn off Pactlane TLSNotary, and turn the original TLSNotary extension back on. Quit and reopen Chrome.

Source and release files: https://github.com/vmichalik/pactlane-tlsnotary
