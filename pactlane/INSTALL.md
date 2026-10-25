# Install Pactlane TLSNotary

This package gives TLSNotary proof setup up to 60 seconds. It is Pactlane's fork of TLSNotary 0.1.0.1501.

## Install in Chrome

1. Quit Chrome with Cmd+Q, then open it again.
2. Unzip the download. Keep the `Pactlane TLSNotary` folder somewhere permanent, such as Documents. Chrome needs those files while the extension is installed.
3. Open `chrome://extensions` and turn off the existing TLSNotary extension. You can leave it installed.
4. Turn on **Developer mode** at the top right.
5. Click **Load unpacked**. Inside the `Pactlane TLSNotary` folder, choose the `extension` folder. It contains `manifest.json`.
6. Check that **Pactlane TLSNotary** is enabled. Leave the original TLSNotary extension turned off while testing.

The version label is `0.1.0.1501-pactlane.1`. The underlying API version remains `0.1.0.1501`.

## Run the public check

Open https://stellar-p2p-proof-vijay.fly.dev/extension-check/ and click **Check extension only**.

In the window that opens, click **Run public connection check** once. Keep the window visible. When the disclosure preview appears, approve only the public `GET /robots.txt` request line and HTTP status.

This check uses the same 4 KiB sent / 16 KiB received limits as the transfer check. It uses no bank login, cookies or payment data.

Copy the final `Extension check:` line from the original tab. If it fails, stop rather than running another attempt. If it is still stuck after two minutes, keep only the displayed status message and quit Chrome. The timeout cleanup issue in the upstream runtime is still present.

A public pass confirms that this connection worked. Payment proof remains unverified. Wait for the verifier result to be checked before testing an account transfer.

## Return to the official extension

Open `chrome://extensions`, remove or turn off Pactlane TLSNotary, and turn the original TLSNotary extension back on. Quit and reopen Chrome.

Source and release files: https://github.com/vmichalik/pactlane-tlsnotary
